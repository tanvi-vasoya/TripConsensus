from app.config import settings

print("=" * 50)
print("ENABLE_SMS        :", settings.enable_sms)
print("ACCOUNT SID       :", settings.twilio_account_sid)
print("PHONE NUMBER      :", settings.twilio_phone_number)
print("=" * 50)