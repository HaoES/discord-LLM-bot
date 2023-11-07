import json
import aiohttp
import asyncio

API_URL = 'http://localhost:8000/v1/chat/completions'
headers = {"Content-Type":"application/json"}

payload = {
    "max_tokens":512,
    "messages": []
}
async def main():
    while True:
        prompt = input("User: ")
        msg = {
            "content": f"{prompt} ### response: ",
            "role": "user"
        }
        payload["messages"].append(msg)
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, data = json.dumps(payload), headers = headers) as resp:
                reply = await resp.json()
                reply_content = reply["choices"][0]["message"]["content"]
                print(f"Bot: {reply_content}")
        msg_idx = payload["messages"].index(msg)
        payload["messages"][msg_idx]["content"] += reply_content 


asyncio.run(main())
