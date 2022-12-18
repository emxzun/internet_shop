from django.core.mail import send_mail

from applications.account.models import CustomUser
from main.celery import app


@app.task
def spam_message():
    emails = CustomUser.objects.all()
    list_emails = [i.email for i in emails]
    send_mail(
        'привет, мы из internet_shop',
        'загляни на наш сайт, у нас много интересного http://localhost:8000/api/v1/product/',
        'e352709@gmail.com',
        list_emails
    )
