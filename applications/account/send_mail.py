from django.core.mail import send_mail


def send_confirmation_code(email, code):
    send_mail(
        'Восстановление пароля',
        code,
        'e352709@gmail.com',
        [email]
    )
