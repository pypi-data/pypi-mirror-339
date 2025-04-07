from pydantic import BaseModel, ConfigDict, TypeAdapter


class Project(BaseModel):
    id: int
    name: str
    default_branch: str

    model_config = ConfigDict(extra="allow")


Projects = TypeAdapter(list[Project])
