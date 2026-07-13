from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/sms",
    tags=["SMS"],
)


@router.post(
    "/webhook",
)
async def sms_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...),
    db: Session = Depends(get_db),
) -> dict:
    """
    Receive incoming SMS messages from Twilio.

    Twilio sends data as application/x-www-form-urlencoded.
    """

    print("=" * 60)
    print("Incoming SMS")
    print(f"Message SID : {MessageSid}")
    print(f"From        : {From}")
    print(f"Body        : {Body}")
    print("=" * 60)

    # TODO:
    # 1. Find participant by phone number.
    # 2. Pass the message to SurveyService.
    # 3. Save survey responses.
    # 4. Send the next survey question (if applicable).

    return {
        "status": "received",
    }