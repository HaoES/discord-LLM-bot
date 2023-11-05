import aiohttp
import asyncio
import json
import discord

API_URL = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

payload = {
  "max_tokens": 512,
  "messages": []
}

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ai'):
            stripped_msg = str(message.content).replace('!ai','').strip()
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
                    await message.reply(reply_content, mention_author=True)

            msg_idx = payload["messages"].index(message)
            payload["messages"][msg_idx]["content"] += reply_content


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('token')
