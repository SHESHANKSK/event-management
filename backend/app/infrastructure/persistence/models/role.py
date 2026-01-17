from sqlalchemy import Column, String
from ..database import Base

class RolePermission(Base):
    __tablename__ = "t_role_permissions"

    role = Column(String, primary_key=True)
    permission = Column(String, primary_key=True)
