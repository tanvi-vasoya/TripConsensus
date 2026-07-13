from app.gateway.gateway import Gateway
from app.config import settings

gateway = Gateway()

response = gateway.generate(
    system_prompt="""
You are a travel assistant.

Return ONLY valid JSON in this format:

{
  "recommendations": [
    {
      "destination": "Goa",
      "recommended_start_date": "2026-08-01",
      "recommended_end_date": "2026-08-05",
      "reason": "Beautiful beaches",
      "estimated_cost": 12000,
      "confidence": 0.95
    }
  ]
}

Do not write any explanation.
""",
    user_prompt="Recommend one destination for two college friends with a budget of 12000 INR."
)

print("\n" + "=" * 80)
print("RAW RESPONSE")
print("=" * 80)
print(response.content)
print("=" * 80)