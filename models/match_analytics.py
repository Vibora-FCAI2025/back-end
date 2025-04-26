from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class MatchAnalytics(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    annotated_video_url = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="matches")
