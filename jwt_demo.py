import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()


SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"

payload = {
    "sub": "6",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print("JWT:", token)

decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"]
)

print("Decoded payload:", decoded)