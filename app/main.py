from fastapi import FastAPI,HTTPException
from uuid import uuid4
from pydantic import BaseModel,Field

app = FastAPI()

# 接受用户数据
class UserCreate(BaseModel):
    username : str = Field(min_length = 3,max_length = 20)
    email : str
    age : int = Field(ge = 0,le = 120)
    password : str = Field(min_length = 8)
    nickname : str | None = Field(default = None,min_length = 2,max_length = 20)

# 返回给前端的数据
class UserResponse(BaseModel):
    username : str
    email : str
    age : int
    nickname : str | None = None

# 创建文档时，客户端需要提交的数据。
class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=20000)


# 接口返回的文档数据，比输入多一个服务器生成的 ID。
class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str


# 本轮使用的临时存储：文档 ID -> 文档对象，字典类型
documents: dict[str, DocumentResponse] = {}

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

# 注册逻辑
@app.post(
    "/users",
    response_model = UserResponse
)
def create_user(user : UserCreate):
    print("已进入create_user函数")
    return user

# 创建文档
@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201,
)
def create_document(document: DocumentCreate) -> DocumentResponse:
    saved_document = DocumentResponse(
        id=uuid4().hex,
        title=document.title,
        content=document.content,
    )

    documents[saved_document.id] = saved_document

    return saved_document

# 查询文档
@app.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(document_id: str) -> DocumentResponse:
    document = documents.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document

if __name__ == "__main__":
    print(root())

