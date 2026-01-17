from app.database import SessionLocal
from app.infrastructure.persistence.models.user import User
from app.infrastructure.persistence.models.role import RolePermission
import uuid

def seed_data():
    db = SessionLocal()
    
    # 0. Seed Permissions
    permissions = [
        # Admin Role - Full Access
        ("admin", "admin_access"),
        ("admin", "user_create"),
        ("admin", "user_read"), 
        ("admin", "user_update"),
        ("admin", "user_delete"),
        
        # Support Role - Limited Admin Access
        ("support", "admin_access"), 
        ("support", "user_read"),
        ("support", "user_update"),
        
        # Editor - No admin access
        ("editor", "event_create"),
    ]
    
    for role, perm in permissions:
        exists = db.query(RolePermission).filter_by(role=role, permission=perm).first()
        if not exists:
            db.add(RolePermission(role=role, permission=perm))
    
    db.commit()

    # 1. Check if mock user exists
    mock_uid = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
    user = db.query(User).filter(User.uid == mock_uid).first()
    
    if not user:
        print("Creating mock user...")
        mock_user = User(
            uid=mock_uid,
            username="testadmin",
            first_name="Test",
            last_name="Admin",
            email="admin@internal.com",
            country_code="US",
            roles=["admin"]
        )
        db.add(mock_user)
        
        # Add a few more users
        user2 = User(
            username="alice",
            first_name="Alice",
            last_name="Wonderland",
            email="alice@internal.com",
            country_code="UK",
            roles=["viewer"]
        )
        db.add(user2)
        
        db.commit()
        print("Seed data created successfully.")
    else:
        print("Seed data already exists.")
    
    db.close()

if __name__ == "__main__":
    seed_data()
