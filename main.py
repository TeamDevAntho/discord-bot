from flask import Flask
import threading
import discord
import os
import requests
import time

# === Flask Server ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Ton bot est en ligne !"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    while True:
        try:
            # Remplace cette URL avec l'URL de ton projet Railway
            requests.get("https://discord-bot-production-5572.up.railway.app/")
            print("[KEEP ALIVE] Ping envoyé.")
        except Exception as e:
            print("[KEEP ALIVE] Erreur de ping :", e)
        time.sleep(120)

# === Discord Bot ===
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

initial_nicks = {}

def get_role_emoji(member):
    role_names = [role.name.lower() for role in member.roles]
    if "il/he/him" in role_names:
        return "🟢 "
    elif "elle/she/her" in role_names:
        return "🔴 "
    elif "iel/they" in role_names or "iel/them" in role_names:
        return "🔵 "
    return ""

async def restore_nickname(member):
    if member.id in initial_nicks:
        try:
            await member.edit(nick=initial_nicks[member.id])
        except Exception as e:
            print(f"[ERREUR] Impossible de restaurer le pseudo de {member.name} : {e}")
        del initial_nicks[member.id]

async def update_member_nick(member):
    if member.id not in initial_nicks:
        initial_nicks[member.id] = member.display_name

    emoji = get_role_emoji(member)
    new_nick = emoji + initial_nicks[member.id]

    if member.display_name != new_nick:
        try:
            await member.edit(nick=new_nick)
            print(f"[INFO] Pseudo de {member.name} mis à jour : {new_nick}")
        except Exception as e:
            print(f"[ERREUR] Impossible de modifier le pseudo de {member.name} : {e}")
    else:
        print(f"[INFO] Pseudo de {member.name} déjà à jour.")

@client.event
async def on_ready():
    print(f"[✅] Bot connecté en tant que {client.user}")

@client.event
async def on_member_update(before, after):
    before_roles = set([role.name.lower() for role in before.roles])
    after_roles = set([role.name.lower() for role in after.roles])

    if before_roles != after_roles:
        emoji_roles = {"il/he/him", "elle/she/her", "iel/they", "iel/them"}
        if emoji_roles & after_roles:
            await update_member_nick(after)
        else:
            await restore_nickname(after)

# === Démarrage ===
if __name__ == "__main__":
    threading.Thread(target=run).start()  # Lance le serveur Flask
    threading.Thread(target=keep_alive).start()  # Envoie des pings pour maintenir en ligne

    try:
        token = os.environ["TOKEN"]  # Le token est récupéré via une variable d'environnement
        client.run(token)  # Lance le bot Discord
    except Exception as e:
        print("[ERREUR] Le bot a crashé :", e)
