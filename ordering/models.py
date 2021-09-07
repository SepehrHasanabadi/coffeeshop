from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Order(models.Model):
    WAITING = 'waiting'
    PREPARATION = 'preparation'
    READY = 'ready'
    DELIVERED = 'delivered'
    ORDER_STATUS = [
        (WAITING, 'در انتظار'),
        (PREPARATION, 'آماده سازی'),
        (READY, 'آماده شده'),
        (DELIVERED, 'تحویل داده شده'),
    ]
    TAKE_AWAY = 'take_away'
    IN_SHOP = 'in_shop'
    CONSUME_LOCATION = [
        (TAKE_AWAY, 'بیرون بر'),
        (IN_SHOP, 'در محدوده'),
    ]
    status = models.CharField('وضعیت', max_length=20, choices=ORDER_STATUS, default=WAITING)
    consume_location = models.CharField('محل سرو', max_length=20, choices=CONSUME_LOCATION, default=IN_SHOP)
    menu_item = models.ForeignKey('GenericMenuItem', on_delete=models.CASCADE, null=False)


class GenericMenuItem(models.Model):
    """
    Only menu items must be defined in this model
    """
    object_id = models.PositiveIntegerField(null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False, blank=False)
    content_object = GenericForeignKey('content_type', 'object_id')


class MenuItem(models.Model):
    cost = models.PositiveIntegerField('قیمت')

    def save(self, *args, **kwargs):
        super(MenuItem, self).save(*args, **kwargs)
        generic_menu_item = GenericMenuItem(content_object=self)
        generic_menu_item.save()

    class Meta:
        abstract = True


class Latte(MenuItem):
    SKIM = 'skim'
    SEMI = 'semi'
    WHOLE = 'whole'
    MILK_CHOICES = [
        (SKIM, 'کم'),
        (SEMI, 'متوسط'),
        (WHOLE, 'کامل'),
    ]
    milk = models.CharField('شیر', max_length=20, choices=MILK_CHOICES)

    class Meta:
        verbose_name = 'لاته'
        verbose_name_plural = 'لاته ها'


class Cappuccino(MenuItem):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    SIZE_CHOICES = [
        (SMALL, 'کوچک'),
        (MEDIUM, 'متوسط'),
        (LARGE, 'بزرگ'),
    ]
    size = models.CharField('اندازه', max_length=20, choices=SIZE_CHOICES)

    class Meta:
        verbose_name = 'کاپوچینو'
        verbose_name_plural = 'کاپوچینو ها'


class Espresso(MenuItem):
    SINGLE = 'single'
    DOUBLE = 'double'
    TRIPLE = 'triple'
    SHOTS_CHOICES = [
        (SINGLE, 'یکی'),
        (DOUBLE, 'دوتا'),
        (TRIPLE, 'سه تا'),
    ]
    shots = models.CharField('شات', max_length=20, choices=SHOTS_CHOICES)

    class Meta:
        verbose_name = 'اسپرسو'
        verbose_name_plural = 'اسپرسو ها'


class Tea(MenuItem):
    class Meta:
        verbose_name = 'چای'
        verbose_name_plural = 'چای ها'


class Chocolate(MenuItem):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    SIZE_CHOICES = [
        (SMALL, 'کوچک'),
        (MEDIUM, 'متوسط'),
        (LARGE, 'بزرگ'),
    ]
    size = models.CharField('اندازه', max_length=20, choices=SIZE_CHOICES)

    class Meta:
        verbose_name = 'شکلات'
        verbose_name_plural = 'شکلات ها'


class Cookie(MenuItem):
    CHOCOLATE_CHIP = 'chocolate_chip'
    GINGER = 'ginger'
    KIND_CHOICES = [
        (CHOCOLATE_CHIP, 'شکلاتی'),
        (GINGER, 'زنجبیلی'),
    ]
    kind = models.CharField('نوع', max_length=20, choices=KIND_CHOICES)

    class Meta:
        verbose_name = 'کوکی'
        verbose_name_plural = 'کوکی ها'
