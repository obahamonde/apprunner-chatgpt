from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from src.schemas import User, ChatGPT
from src.service import ChatGPTService, AuthService
from fastapi.middleware.cors import CORSMiddleware
from faunadb import query as q

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/completion")
async def completion(q:str,sub:str,tokens:int=256):
    service = ChatGPTService()  
    response = await service.complete(q,tokens)
    ChatGPT(sub=sub,sender="user",message=q).create()
    ChatGPT(sub=sub,sender="bot",message=response).create()
    return PlainTextResponse(response)

@app.get("/api/auth")
async def auth_endpoint(token:str):
    service = AuthService()
    user = await service.get_user(token)
    user = User(**user)
    return user.upsert(user.sub)
    
    
    
@app.get("/api/chats")
async def chats(sub:str):
    try:    
        response = ChatGPT.q()(q.map_(lambda x: q.get(x), q.paginate(q.match(q.index("chatgpt_by_sub"), sub))))["data"]
        return [r["data"] for r in response]
    except:
        return []


@app.on_event("startup")
async def startup():
    User.provision()
    ChatGPT.provision()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)