from django.core.mail import send_mail

from coffeeshop.celery import app


@app.task
def send_modified_status_mail(recipient_list):
    send_mail('سفارش کافی شاپ', 'وضعیت سفارش شما تغییر کرد', 'info@coffeeshop.ir', recipient_list)


@app.task
def send_cancel_order_mail(recipient_list):
    send_mail('سفارش کافی شاپ', 'سفارش شما لغو گردید', 'info@coffeeshop.ir', recipient_list)
