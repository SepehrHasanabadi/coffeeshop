from django.contrib import admin

from ordering.models import Latte, Cappuccino, Espresso, Tea, Chocolate, Cookie


@admin.register(Latte)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'milk',)


@admin.register(Cappuccino)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'size',)


@admin.register(Espresso)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'shots',)


@admin.register(Tea)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price',)


@admin.register(Chocolate)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'size',)


@admin.register(Cookie)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'kind',)
