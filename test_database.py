from app.database import engine, SessionLocal

print("Engine:", engine)

db = SessionLocal()

print("Session Created Successfully!")

db.close()

print("Session Closed Successfully!")