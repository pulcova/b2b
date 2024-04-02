# tasks.py
from django.contrib.sessions.models import Session
from celery import shared_task
from twilio.rest import Client
from django.conf import settings
import random
import os

@shared_task
def send_otp_to_phone(phone, session_key):
    otp = random.randint(100000, 999999)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_FROM_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=twilio_number,
        to=phone
    )

    session = Session.objects.get(session_key=session_key)
    session['otp'] = otp
    session.save()