from fastapi import FastAPI

app = FastAPI()

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

if __name__ == "__main__":
    print(hello())
