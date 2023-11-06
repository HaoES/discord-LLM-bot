
import json
import aiohttp
import asyncio

API_URL = 'http://localhost:8000/v1/chat/completions'
headers = {"Content-Type":"application/json"}

async def main():
    prompt = input("User: ")
    payload = {
        "max_tokens":512,
        "messages": [
            {
                "content": f"{prompt} ### response: ",
                "role": "user"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data = json.dumps(payload), headers = headers) as resp:
            reply = await resp.json()
            reply_content = reply["choices"][0]["message"]["content"]
            print(reply_content)

asyncio.run(main())
