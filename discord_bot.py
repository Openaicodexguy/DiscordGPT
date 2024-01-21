# bot.py
import os
import discord
import openai  # Import the OpenAI library
from langchain.chat_models import ChatOpenAI
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain

# Fetch OpenAI API key and Discord token from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")

if not (openai.api_key and TOKEN):
    print("Please set the OPENAI_API_KEY and DISCORD_TOKEN environment variables.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        llm = ChatOpenAI(temperature=1.0)
        
        # Get a response from OpenAI's text generation API
        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message.clean_content,
            temperature=1.0,
            max_tokens=150,
        )

        # Extract the generated response from OpenAI's API response
        output = openai_response["choices"][0]["text"]

        await message.reply(output)

client.run(TOKEN)
