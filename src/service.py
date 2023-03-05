from httpx import AsyncClient
from src.config import env

class ChatGPTService:
    """ChatGPT service."""
    def __init__(self):
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
                "Authorization": f"Bearer {env.API_KEY}",
                "Content-Type": "application/json"
        }
        
    async def complete(self, prompt: str, tokens:int=128, temperature:float=0.9)->str:
        async with AsyncClient() as client:
            response = await client.post(
                self.url,
                headers=self.headers,
                json={
                    "model": "text-davinci-003",
                    "prompt": prompt,
                    "max_tokens": tokens,
                    "temperature": temperature,
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            )
            return response.json()["choices"][0]["text"]
    
        
class AuthService:
    """Auth service."""
    def __init__(self):
        self.url = f"https://{env.AUTH0_DOMAIN}/userinfo"
        
    async def get_user(self, token: str)->dict:
        async with AsyncClient() as client:
            response = await client.get(
                self.url,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
            return response.json()