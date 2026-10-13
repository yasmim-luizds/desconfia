from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class RiskLevel(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class IndicatorCategory(str, Enum):
    URGENCY = 'urgency'
    FINANCIAL_REQUEST = 'financial_request'
    IMPERSONATION = 'impersonation'
    CREDENTIAL_REQUEST = 'credential_request'
    THREAT = 'threat'
    PRIZE_OR_BENEFIT = 'prize_or_benefit'
    SUSPICIOUS_LINK = 'suspicious_link'
    OTHER = 'other'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    analyses: Mapped[list['Analysis']] = relationship(back_populates='user', cascade='all, delete-orphan')
    feedbacks: Mapped[list['Feedback']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Analysis(Base):
    __tablename__ = 'analyses'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(String(10), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    ai_provider: Mapped[str] = mapped_column(String(40), default='local-demo', nullable=False)
    ai_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user: Mapped[User] = relationship(back_populates='analyses')
    indicators: Mapped[list['AnalysisIndicator']] = relationship(back_populates='analysis', cascade='all, delete-orphan')
    feedbacks: Mapped[list['Feedback']] = relationship(back_populates='analysis', cascade='all, delete-orphan')


class AnalysisIndicator(Base):
    __tablename__ = 'analysis_indicators'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    analysis_id: Mapped[str] = mapped_column(ForeignKey('analyses.id', ondelete='CASCADE'), index=True, nullable=False)
    category: Mapped[IndicatorCategory] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(240), nullable=False)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    analysis: Mapped[Analysis] = relationship(back_populates='indicators')


class Feedback(Base):
    __tablename__ = 'feedbacks'
    __table_args__ = (UniqueConstraint('analysis_id', 'user_id', name='ux_feedback_analysis_user'),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    analysis_id: Mapped[str] = mapped_column(ForeignKey('analyses.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_helpful: Mapped[bool] = mapped_column(Boolean, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    analysis: Mapped[Analysis] = relationship(back_populates='feedbacks')
    user: Mapped[User] = relationship(back_populates='feedbacks')
