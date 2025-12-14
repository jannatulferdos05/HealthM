from fastapi import FastAPI, HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional


app = FastAPI()

class User(BaseModel):
    id: Annotated[str,Field(...,description="ID of user",examples=['1'])]
    name: str
    roll: int
    b_year: int
    c_year: int
    gender: Annotated[Literal['male','female'],Field(...,description="Gender of user")]
    @computed_field
    @property
    def age(self) -> int:
        ar=self.c_year-self.b_year
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
    with open("data.json", "r") as fl:
        data1 = json.load(fl)
        return data1

def save_data(data2):
    with open("data.json", "w") as fs:
        json.dump(data2, fs)
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
    roll: Annotated[Optional[int],Field(default=None,description="Roll of user")]
    gender: Annotated[Optional[Literal['male','female']],Field(...,description="Gender of user")]
    b_year: Annotated[Optional[int],Field(default=None,description="Birth Year of user")]
    c_year: Annotated[Optional[int],Field(default=None,description="Current Year ")]

@app.put("/edit{id1}")
def edit_user(uid:str, user_update:UserUpdate):
    data1=load_data()
    if uid not in data1:
        raise HTTPException(status_code=400,detail="User does not exist")

    existing_user = data1[uid] #Don't need all the key's value rather need specific one user value

    updated_user=user_update.model_dump(exclude_unset=True) #Converting pydantic object into dictionary

    for key,value in updated_user.items(): #loop is from updated but changes is done in existing user
        existing_user[key]=value

    #existing_user to pydantic object then age
    existing_user['id'] = uid
    user_obj=User(**existing_user)

    #Pydantic object to dictionary
    existing_user=user_obj.model_dump(exclude={'id'})

    #Add this dictionary to data1
    data1[uid]=existing_user

    save_data(data1)
    return JSONResponse(status_code=200,content={"message": "User updated successfully"})


@app.delete("/delete{id1}")
def delete_user(id1:str):
    data1=load_data()
    if id1 in data1:
        del data1[id1]
        save_data(data1)
        return JSONResponse(status_code=200,content={"message": "User deleted successfully"})
    else:
        raise HTTPException(status_code=400,detail="User does not exist")

