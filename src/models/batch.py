from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

batch_trainers = Table(
    "batch_trainers",
    Base.metadata,
    Column("batch_id", Integer, ForeignKey("batches.id", ondelete="CASCADE"), primary_key=True),
    Column("trainer_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

batch_students = Table(
    "batch_students",
    Base.metadata,
    Column("batch_id", Integer, ForeignKey("batches.id", ondelete="CASCADE"), primary_key=True),
    Column("student_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institution_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trainers = relationship("User", secondary=batch_trainers, backref="trainer_batches")
    students = relationship("User", secondary=batch_students, backref="student_batches")
    invites = relationship("BatchInvite", back_populates="batch", cascade="all, delete")

class BatchInvite(Base):
    __tablename__ = "batch_invites"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    batch = relationship("Batch", back_populates="invites")
