from django.contrib import admin

from ordering.models import Latte, Cappuccino, Espresso, Tea, Chocolate, Cookie


@admin.register(Latte)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost', 'milk',)


@admin.register(Cappuccino)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost', 'size',)


@admin.register(Espresso)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost', 'shots',)


@admin.register(Tea)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost',)


@admin.register(Chocolate)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost', 'size',)


@admin.register(Cookie)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cost', 'kind',)
