from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Enum

from app.database.session import Base
from app.types.application_status import ApplicationStatus
from app.types.country_region import CountryRegion
from app.types.program_season import PS_ProgramSeason


class ApplicationModel(Base):
    """
    Representa uma inscrição para uma temporada de programa.
    """
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    program_season = Column(Enum(PS_ProgramSeason), nullable=False, index=True)
    country_region = Column(Enum(CountryRegion), nullable=False, index=True)
    video_url = Column(String(255), nullable=False)
    photo1_url = Column(String(255), nullable=False)
    photo2_url = Column(String(255))
    photo3_url = Column(String(255))
    status = Column(Enum(ApplicationStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
