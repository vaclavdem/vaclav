from django_delivery_7.celery import app
from .service import (
    send_order,
    send_report,
    send_change_status,
    send_take,
    send_delivered,
)

@app.task
def send_order_email(user_email):
    send_order(user_email)


@app.task
def send_report_email(user_email):
    send_report(user_email)


@app.task
def send_change_status_email(user_email):
    send_change_status(user_email)


@app.task
def send_take_email(user_email):
    send_take(user_email)


@app.task
def send_delivered_email(user_email):
    send_delivered(user_email)
