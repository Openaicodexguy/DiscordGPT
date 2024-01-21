import discord
import openai
import os
import time
from discord.ext import commands

client = discord.Client()


# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")

# Define the necessary intents
intents = discord.Intents.all()

# Create a bot instance with specified intents
bot = commands.Bot(command_prefix='', intents=intents)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Event triggered on each received message
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Reply when mentioned
    if bot.user.mentioned_in(message):
        # Extract the user's query from the message content
        user_query = message.content.replace(f'<@!{bot.user.id}>', '').strip()

        # Make a request to OpenAI's Davinci engine
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_query,
                max_tokens=150
            )

            # Extract the generated response from OpenAI and send it to the user
            bot_response = response['choices'][0]['text'].strip()
            await message.channel.send(bot_response)

        except openai.error.OpenAIError as e:
            if "Rate limit exceeded" in str(e):
                print("Rate limit exceeded. Waiting for 20 seconds...")
                time.sleep(20)
                await message.channel.send("Sorry, we're experiencing high demand. Please try again in 20 seconds.")
            else:
                print(f"An error occurred: {e}")
                await message.channel.send("An error occurred while processing your request.")

    # Let the bot process commands as well
    await bot.process_commands(message)

# Run the bot with your Discord bot token
client.run('TOKEN')
