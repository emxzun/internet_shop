from django.core.mail import send_mail

from main.celery import app


@app.task
def send_confirmation_link(email, confirm_code):
    full_link = f'http://localhost:8000/api/v1/order/confirmation/{confirm_code}'
    send_mail(
        'Подтверждение заказа',
        full_link,
        'e352709@gmail.com',
        [email]
    )
