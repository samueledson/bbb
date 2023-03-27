from pydantic import BaseModel


class ApplicationBaseSchema(BaseModel):
    candidate_id: int
    program_season: str
    country_region: str
    video_uuid: str
    photo1_uuid: str
    photo2_uuid: str = None
    photo3_uuid: str = None


class ApplicationCreateSchema(ApplicationBaseSchema):
    pass


class ApplicationUpdateSchema(ApplicationBaseSchema):
    pass


class ApplicationSchema(ApplicationBaseSchema):
    id: int

    class Config:
        orm_mode = True
