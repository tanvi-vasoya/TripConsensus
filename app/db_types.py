from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID



UUIDType = UUID(as_uuid=True)
ShortText = String(255)
LongText = String(2000)
Timestamp = DateTime(timezone=True)