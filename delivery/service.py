from django.core.mail import send_mail


def send_order(user_email):
    send_mail(
        "Информирование",
        "С вашего устройства создали заказ",
        'cy4ok2006@gmail.com',
        [user_email],
    )


def send_report(user_email):
    send_mail(
        "Информирование",
        "С вашего устройства создали жалобу",
        'cy4ok2006@gmail.com',
        [user_email],
    )


def send_change_status(user_email):
    send_mail(
        "Заказ",
        "Статус вашего заказа изменён",
        'cy4ok2006@gmail.com',
        [user_email],
    )


def send_take(user_email):
    send_mail(
        "Заказ",
        "Курьер принял ваш заказ",
        'cy4ok2006@gmail.com',
        [user_email],
    )


def send_delivered(user_email):
    send_mail(
        "Заказ",
        "Курьер доставил ваш заказ",
        'cy4ok2006@gmail.com',
        [user_email],
    )


def send_restaurant(user_email):
    send_mail(
        "Заказ",
        "Из вашего ресторана создали заказ",
        'cy4ok2006@gmail.com',
        [user_email],
    )
