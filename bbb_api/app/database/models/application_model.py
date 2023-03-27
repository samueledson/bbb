from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Enum

from app.database.session import Base
from app.types.country_region import CountryRegion
from app.types.program_season import ProgramSeason


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    program_season = Column(Enum(ProgramSeason), nullable=False)
    country_region = Column(Enum(CountryRegion), nullable=False)
    video_uuid = Column(String(255), nullable=False)
    photo1_uuid = Column(String(255), nullable=False)
    photo2_uuid = Column(String(255))
    photo3_uuid = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
