import json
import os
import random
from dotenv import load_dotenv
from typing import Final
import settings

load_dotenv()
PREFIX: Final[str] = os.getenv('PREFIX')

# Load messages from JSON file
def load_messages(guild):
    path = 'data/' + str(guild) + '/messages.json'

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'x')
        with open(path, 'r') as f:
            return {}
    except json.JSONDecodeError:
        return {}

# Save messages to JSON file
def save_messages(messages, guild):
    with open('data/' + str(guild) + '/messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

# Function to log a new message
def log_message(message):
    if settings.is_channel_enabled(message.guild.id, message.channel.id) == False:
        return
    
    message_data = {
        "author": str(message.author),
        "guild" : message.guild.id,
        "content": message.content,
        "timestamp": str(message.created_at),
        "attachments": []
    }
    for attachment in message.attachments:
        message_data["attachments"].append(attachment.url)

    if  message_data["content"][0] == str(PREFIX) or message_data["attachments"] == [] and message_data["content"] == "":
        return
    
    messages = load_messages(message.guild.id)
    
    # Add message to the list under the correct channel
    if str(message.channel.id) not in messages:
        messages[str(message.channel.id)] = []
    
    messages[str(message.channel.id)].append(message_data)
    save_messages(messages, message.guild.id)

def get_random_msg(guild, channel_id):
    messages = load_messages(guild)
    if str(channel_id) in messages and messages[str(channel_id)]:
        random_message = random.choice(messages[str(channel_id)])
        return random_message
    else:
        return None
    
def clear_all(guild):
    try :
        open('data/' + str(guild) + '/messages.json', 'w').close()
    except:
        return

def clear_channel(guild, channel):
    messages = load_messages(guild)
    if channel not in messages:
        return
    messages[str(channel)].clear()
    save_messages(messages,guild)
