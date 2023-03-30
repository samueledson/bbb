from pydantic import BaseModel

from app.types.application_status import ApplicationStatus
from app.types.country_region import CountryRegion
from app.types.program_season import PS_ProgramSeason


class ApplicationBaseSchema(BaseModel):
    program_season: PS_ProgramSeason
    country_region: CountryRegion
    video_url: str = None
    photo1_url: str = None
    photo2_url: str = None
    photo3_url: str = None
    status: ApplicationStatus


class ApplicationCreateSchema(ApplicationBaseSchema):
    candidate_id: int


class ApplicationUpdateSchema(ApplicationBaseSchema):
    program_season: PS_ProgramSeason = None
    country_region: CountryRegion = None


class ApplicationSchema(ApplicationBaseSchema):
    id: int
    candidate_id: int

    class Config:
        orm_mode = True
