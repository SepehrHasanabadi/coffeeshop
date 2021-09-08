from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from ordering.models import Latte, Tea, Cookie, Order, GenericMenuItem


def remove_keys(d, keys):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_keys(v, keys) for v in d]
    return {k: remove_keys(v, keys) for k, v in d.items()
            if k not in keys}


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class TestOrderingViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_menu_list(self):
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        Latte.objects.create(price=2000, milk=Latte.WHOLE)
        Tea.objects.create(price=500)
        Cookie.objects.create(price=3000, kind=Cookie.GINGER)
        actual_result_resposne = self.client.get("/ordering/menu/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        expected_result = [
            {
                'name': 'latte',
                'options': [
                    {
                        'price': 1000,
                        'milk': Latte.SKIM
                    },
                    {
                        'price': 2000,
                        'milk': Latte.WHOLE
                    }
                ]
            },
            {
                'name': 'cookie',
                'options': [
                    {
                        'price': 3000,
                        'kind': Cookie.GINGER
                    }
                ]
            },
            {
                'name': 'tea',
                'options': [{
                    'price': 500
                }]
            }
        ]
        self.assertEqual(ordered(remove_keys(actual_result_resposne.data, 'id')), ordered(expected_result))

    def test_order(self):
        actual_result_resposne = self.client.get("/ordering/order/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        valid_data = {
            "consume_location": Order.IN_SHOP,
            "menu_item": menu_item.id
        }
        actual_result_resposne = self.client.post("/ordering/order/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        self.client.force_login(user=user)
        actual_result_resposne = self.client.post("/ordering/order/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 201)
        expected_result = {
            "status": Order.WAITING,
            "consume_location": Order.IN_SHOP,
            "menu_item": menu_item.id,
            "order": {
                "price": menu_item.content_object.price,
                "milk": Latte.SKIM,
                "name": "لاته"
            }
        }
        self.assertEqual(ordered(remove_keys(actual_result_resposne.data, 'id')), ordered(expected_result))

    def test_status_order(self):
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        staff, _ = User.objects.get_or_create(username='staff', is_staff=True)
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        order_user = Order.objects.create(menu_item=menu_item, user=user)
        valid_data = {
            "status": Order.PREPARATION
        }
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        self.client.force_login(user=user)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        self.client.force_login(user=staff)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        expected_result = {
            "status": Order.PREPARATION
        }
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))

    def test_cancel_order(self):
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        staff, _ = User.objects.get_or_create(username='staff', is_staff=True)
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        order_user = Order.objects.create(menu_item=menu_item, user=user)
        order_staff = Order.objects.create(menu_item=menu_item, user=staff)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_staff.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        self.client.force_login(user=user)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_staff.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        expected_result = {
            "status": Order.CANCELED
        }
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))
        order_user.status = Order.WAITING
        order_user.save()
        self.client.force_login(user=staff)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))
