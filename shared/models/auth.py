from sqlalchemy import Column, Integer, String
from shared.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)  # 'admin', 'auditor', 'engineer'
    tenant_id = Column(String, index=True)
