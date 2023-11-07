import json
import aiohttp
import asyncio
import discord
import os

from dotenv import load_dotenv 
load_dotenv()
TOKEN = os.getenv("TOKEN")

API_URL = 'http://localhost:8000/v1/chat/completions'
headers = {"Content-Type":"application/json"}

payload = {
    "max_tokens":512,
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

        if message.content.startswith('!bot'):
            stripped_msg = str(message.content).replace('!bot','').strip()
            msg = {
                "content": f"{stripped_msg} ### response: ",
                "role": "user"
            }
            payload["messages"].append(msg)
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, data = json.dumps(payload), headers = headers) as resp:
                    reply = await resp.json()
                    reply_content = reply["choices"][0]["message"]["content"]
                    await message.reply(reply_content, mention_author=True)
            msg_idx = payload["messages"].index(msg)
            payload["messages"][msg_idx]["content"] += reply_content 


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
