from main.celery import app
from django.core.mail import send_mail


@app.task
def send_confirmation_email_celery(email, code):
    import time
    time.sleep(5)
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'Активация пользователя',
        full_link,
        'e352709@gmail.com',
        [email]
    )
