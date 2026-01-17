import uuid
from sqlalchemy import Column, String, DateTime, JSON, Uuid, Boolean
from sqlalchemy.sql import func
from ..database import Base

# Note: Boolean is not strictly in the spec, but usually needed. 
# Spec allows: uid, username, first_name, last_name, email, country_code, roles, created_at, updated_at
# Using generic UUID for compatibility, but mapped to Postgres UUID.

class SqlUser(Base):
    __tablename__ = "t_users"

    uid = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    country_code = Column(String, nullable=False)
    roles = Column(JSON, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
