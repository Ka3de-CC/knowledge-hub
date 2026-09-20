from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 接受用户数据
class UserCreate(BaseModel):
    username : str
    email : str
    age : int
    password : str

# 返回给前端的数据
class UserResponse(BaseModel):
    username : str
    email : str
    age : int


@app.get("/")
def root():
    return{
        "message" : "Hello Knowledge Hub"
    }

@app.get("/hello/{name}")
def hello(name):
    return{
        # f-string （格式化字符串） 将花括号中的变量值插入字符串
        "message" : f"Hello {name}"
    }

@app.get("/search")
def search(keyword: str):
    return{
        "keyword" : keyword
    }

@app.get("/user/{username}")
def user(username):
    return{
        "username" : f"{username}"
    }

@app.get("/items")
# 声明变量的类型
def search(page : int,size : int):
    return{
        "page" : page,
        "size" : size
    }

@app.post("/register")
def register(user : UserCreate):
    return user

@app.post(
    "/users",
    response_model = UserResponse
)
def create_user(user : UserCreate):
    return user


if __name__ == "__main__":

