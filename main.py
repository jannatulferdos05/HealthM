from fastapi import FastAPI, HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional


app = FastAPI()

class User(BaseModel):
    id: Annotated[str,Field(...,description="ID of user",examples=['1'])]
    name: str
    age: int
    roll: int
    gender: Annotated[Literal['male','female'],Field(...,description="Gender of user")]
    @computed_field
    @property
    def dif(self) -> int:
        ar=self.age-self.roll
        return ar


with open("data.json", "r") as f:
    data = json.load(f)

print(data)
@app.get("/")
async def root():
    return {"message": "Hello World"}


#Path Parameter
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

#Query Parameter
@app.get("/health")
def health(id1: str):
    for k in data:
        print("value of k is ",k)
        if k == id1:
            return data[k]
    else:
        return {"message": f"ID {id1} Not Found"}

def load_data():
    with open("data.json", "r") as f:
        data1 = json.load(f)
        return data1

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)
@app.post("/create")
def create_user(user: User):
    data1=load_data()

    if user.id in data1:
        return HTTPException(status_code=400,detail="User already exists")
    data1[user.id]=user.model_dump(exclude={'id'})

    save_data(data1)
    return JSONResponse(status_code=201,content={"message": "User created successfully"})



class UserUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None,description="Name of user")]
    age: int
    roll: int
    gender: Annotated[Literal['male','female'],Field(...,description="Gender of user")]
    @computed_field
    @property
    def dif(self) -> int:
        ar=self.age-self.roll
        return ar

@app.put("/edit{id}")
def edit_user(id:str, User):
    pass

