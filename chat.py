import aiohttp
import asyncio
import json

API_URL = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

payload = {
  "max_tokens": 512,
  "messages": []
}

async def main():
    while True:
        prompt = input("User: ")
        message = {
          "content": f"{prompt} ### Response: ",
          "role": "user"
        }
        payload["messages"].append(message)

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, data = json.dumps(payload), headers=headers) as resp:
                reply = await resp.json()
                reply_content = reply["choices"][0]["message"]["content"]
                print(f"BOT: {reply_content}")

        msg_idx = payload["messages"].index(message)
        payload["messages"][msg_idx]["content"] += reply_content

asyncio.run(main())
