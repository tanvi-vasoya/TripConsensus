from app.config import settings

print("=" * 50)
print("Application Name :", settings.app_name)
print("Environment      :", settings.environment)
print("Database URL     :", settings.database_url)
print("Redis URL        :", settings.redis_url)
print("Model Provider   :", settings.model_provider)
print("Ollama Model     :", settings.ollama_model)
print("=" * 50)

print(settings.ollama_base_url)
print(settings.ollama_model)
print(settings.database_url)


from app.config import settings

print("=" * 50)
print("ENABLE_SMS =", settings.enable_sms)
print("ACCOUNT SID =", settings.twilio_account_sid)
print("PHONE =", settings.twilio_phone_number)
print("=" * 50)