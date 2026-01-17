from app.database import SessionLocal
from app.infrastructure.persistence.models.user import User

def check_users():
    db = SessionLocal()
    users = db.query(User).all()
    print(f"Users found: {len(users)}")
    for u in users:
        print(f"User: {u.username}, Roles: {u.roles}, Type: {type(u.roles)}")
    db.close()

if __name__ == "__main__":
    check_users()
