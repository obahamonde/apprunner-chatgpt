from typing import Optional
from pydantic import BaseModel, Field
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from src.config import env
from faunadb.objects import Query

class FaunaModel(BaseModel):
    """Base model for FaunaDB models."""
    id: Optional[str] = Field(default=None, alias="id") 
    ts: Optional[int] = Field(default=None, alias="ts")  
     
    @classmethod
    def client(cls)->FaunaClient:
        """Return a FaunaDB client."""
        return FaunaClient(secret=env.FAUNA_SECRET)
    
    @classmethod
    def q(cls)->Query:
        """Return the FaunaDB query object."""
        return cls.client().query
    
    @classmethod
    def provision(cls):
        """Create the collection and indexes."""
        if not cls.q()(q.exists(q.collection(cls.__name__.lower()))):
            cls.q()(q.create_collection({"name": cls.__name__.lower()}))
        for field in cls.__fields__.values():
            if field.field_info.extra.get("index"):
                data = {
                    "name": f"{cls.__name__.lower()}_by_{field.name}".lower(),
                    "source": q.collection(cls.__name__.lower()),
                    "terms": [{
                        "field": ["data", field.name]
                    }]
                }
                if cls.q()(q.exists(q.index(data["name"]))):
                    continue
                cls.q()(q.create_index(data))
        return True
    
    def create(self):
        """Create a new document in the collection."""
        response =  self.q()(q.create(q.collection(self.__class__.__name__.lower()), {"data": self.dict()}))     
        self.id = response["ref"].id()
        self.ts = response["ts"]
        return self.dict()

    
    def update(self):
        """Update a document."""
        response =  self.q()(q.update(q.ref(q.collection(self.__class__.__name__.lower()), self.id), {"data": self.dict()}))
        self.ts = response["ts"]
        return self.dict()