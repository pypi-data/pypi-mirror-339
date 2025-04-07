from pydantic import BaseModel, ConfigDict, TypeAdapter


class User(BaseModel):
    login: str

    model_config = ConfigDict(extra="allow")


class Repository(BaseModel):
    default_branch: str
    name: str
    owner: User

    model_config = ConfigDict(extra="allow")


RepositoryList = TypeAdapter(list[Repository])
