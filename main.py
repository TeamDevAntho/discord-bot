import discord
from flask import Flask
import threading

# === Serveur Flask pour garder le bot en ligne ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Ton bot est en ligne !"

def run():
    app.run(host="0.0.0.0", port=8080)

thread = threading.Thread(target=run)
thread.start()

# === Code du Bot Discord ===
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

# Remplace 'TON_TOKEN_ICI' par ton token Discord réel
token = 'TON_TOKEN_ICI'
client.run(token)
