from datetime import datetime, timedelta

from django.core.mail import send_mass_mail
from orders.models import Order
from django.conf import settings
from celery import shared_task


@shared_task
def send_mail_one_day_before():
    time_now = datetime.now()
    start_time = time_now + +timedelta(days=1)
    end_time = time_now + +timedelta(days=2)

    orders = Order.objects.filter(date_of_payment__range=[start_time, end_time])

    messages_list = []
    from_email = settings.EMAIL_HOST_USER
    content = [time_now, []]
    for order in orders:
        messages_list.append(
            (
                "Date of payment",
                f"Your order nr: {order.pk} has a the deadline of payment: {order.date_of_payment}",
                from_email,
                [order.client.email],
            )
        )
        content[1].append(order.pk)

    send_mass_mail(tuple(messages_list), fail_silently=False)

    return content
