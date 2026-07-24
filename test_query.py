from database import SessionLocal
import models

db = SessionLocal()
try:
    result = db.query(models.Trial).limit(1).all()
    print(f"Query successful! Found {len(result)} trials")
except Exception as e:
    print(f"Query failed: {type(e).__name__}: {e}")
finally:
    db.close()
