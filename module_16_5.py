from fastapi import FastAPI, Path, HTTPException,Body,Request
from fastapi.responses import HTMLResponse
from typing import List, Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI(debug=True)

users = []

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int
# users = [User(id=1, username='username_1', age=20), User(id=2, username='username_2', age=21), User(id=3, username='username_3', age=22), User(id=4, username='username_4', age=23), User(id=5, username='username_5', age=24)]
def find_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    return None

@app.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request) -> HTMLResponse:
    print("get запрос на всех юзеров",users)
    return templates.TemplateResponse("users.html",{"request":request,"messages":users})


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: Annotated[int, Path(ge=0, le=999, description='Enter your id', example=1)]) -> HTMLResponse:
    user = find_user(user_id)
    if user:
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def add_user(
        username: Annotated[str, Path(min_length=5,max_length=20, description= 'Enter username', example='UrbanUser' )],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age',example=24)]) -> User:
    user_id = users[-1].id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    print(users)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=0,le=999, description='Enter your id',example=1) ],
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    user = find_user(user_id)
    if user:
        user.username = username
        user.age = age
        return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=0,le=999, description='Enter your id',example=1) ]):
    user = find_user(user_id)
    if user:
        users.remove(user)
        return {"detail": f"User {user_id} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


