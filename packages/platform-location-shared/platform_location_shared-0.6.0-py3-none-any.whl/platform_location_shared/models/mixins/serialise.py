from pydantic import BaseModel


class Serialisable(BaseModel):
    def serialise(self):
        return self.model_dump(mode="json")
