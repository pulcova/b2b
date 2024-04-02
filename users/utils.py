from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
import random

from django.conf import settings


def send_otp_to_phone(phone, request):
    otp = random.randint(100000, 999999)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_FROM_NUMBER

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=twilio_number,
            to=phone
        )
        request.session['otp'] = otp
    except TwilioRestException as e:
        print(f"Error sending OTP: {e}")