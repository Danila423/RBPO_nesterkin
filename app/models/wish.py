from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Wish(Base):
    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(100), nullable=False)
    link = Column(String(255))
    price_estimate = Column(Numeric(10, 2))
    notes = Column(String(255))

    owner = relationship("User", backref="wishes")
