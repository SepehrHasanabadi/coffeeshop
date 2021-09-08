from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from ordering.models import Latte, Tea, Cookie, Order, GenericMenuItem
from ordering.utils import ordered, remove_keys


class TestOrderingViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_menu_list(self):
        """
            evaluating the structure of a menu list
        """
        # Add some Menu items
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        Latte.objects.create(price=2000, milk=Latte.WHOLE)
        Tea.objects.create(price=500)
        Cookie.objects.create(price=3000, kind=Cookie.GINGER)
        # Request to get the menu
        actual_result_resposne = self.client.get("/ordering/menu/", format='json')
        # Assert status code
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
        # Assert actual and expected values
        self.assertEqual(ordered(remove_keys(actual_result_resposne.data, 'id')), ordered(expected_result))

    def test_order(self):
        """
        Check inserting and getting an order
        """
        # Add an item to menu list
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        valid_data = {
            "consume_location": Order.IN_SHOP,
            "menu_item": menu_item.id
        }
        # Request as an anonymous user to get orders
        actual_result_resposne = self.client.post("/ordering/order/", data=valid_data, format='json')
        self.assertEqual(actual_result_resposne.status_code, 403)
        # Create and login a sample user
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        self.client.force_login(user=user)
        # Request a user for a menu item
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
        # Assert expected and actual result
        self.assertEqual(ordered(remove_keys(actual_result_resposne.data, 'id')), ordered(expected_result))

    def test_status_order(self):
        """
        Staus changing is only possible by a staff user
        """
        # create a couple of staff and non-staff user
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        staff, _ = User.objects.get_or_create(username='staff', is_staff=True)
        # Create an item for the menu
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        # Create an order for the normal user
        order_user = Order.objects.create(menu_item=menu_item, user=user)
        valid_data = {
            "status": Order.PREPARATION
        }
        # Request the anonymous user for modifing the status
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        # Assert permission denied
        self.assertEqual(actual_result_resposne.status_code, 403)
        # login as a normal user
        self.client.force_login(user=user)
        # Request the normal user for modifing the status
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        # Assert permission denied
        self.assertEqual(actual_result_resposne.status_code, 403)
        # login as a staff user
        self.client.force_login(user=staff)
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/status/", data=valid_data, format='json')
        # The action is OK
        self.assertEqual(actual_result_resposne.status_code, 200)
        expected_result = {
            "status": Order.PREPARATION
        }
        # Assert expected and actual results
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))

    def test_cancel_order(self):
        """
        staff users can cancel all orders
        normal users can only cancel their own orders
        """
        # create a couple of staff and non-staff user
        user, _ = User.objects.get_or_create(username='user', is_staff=False)
        staff, _ = User.objects.get_or_create(username='staff', is_staff=True)
        # Create an item for the menu
        Latte.objects.create(price=1000, milk=Latte.SKIM)
        menu_item = GenericMenuItem.objects.first()
        # Creata a couple of orders as a staff and a normal user
        order_user = Order.objects.create(menu_item=menu_item, user=user)
        order_staff = Order.objects.create(menu_item=menu_item, user=staff)
        # Request the anonymous user for cancel the order
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_staff.id}/cancel/", format='json')
        # Assert permission denied
        self.assertEqual(actual_result_resposne.status_code, 403)
        # login as a normal user
        self.client.force_login(user=user)
        # Request to cancel another order
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_staff.id}/cancel/", format='json')
        # Assert Permission denied
        self.assertEqual(actual_result_resposne.status_code, 403)
        # Request to cancel his/her order
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        expected_result = {
            "status": Order.CANCELED
        }
        # Assert expected and actual results
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))
        # Revert the user's order status
        order_user.status = Order.WAITING
        order_user.save()
        # login as a staff
        self.client.force_login(user=staff)
        # Request to cancel the user order by staff
        actual_result_resposne = self.client.patch(f"/ordering/order/{order_user.id}/cancel/", format='json')
        self.assertEqual(actual_result_resposne.status_code, 200)
        self.assertEqual(ordered(actual_result_resposne.data), ordered(expected_result))
