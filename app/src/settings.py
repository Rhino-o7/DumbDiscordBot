import os
import json
import shutil


def load_settings(guild_id):
    path = 'data/' + str(guild_id) + '/settings.json'

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.copy('data/default_settings.json', path)
        with open(path, 'r') as f:
            return json.load(f)
   

def save_settings(settings, guild_id):
    with open('data/' + str(guild_id) + '/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

        

def toggle_channel(guild_id, channel_id, active) -> str:
    settings = load_settings(guild_id)
    returnStr = None
    if active:
        for ch in settings["enabled_channels"]:
            if ch == str(channel_id):
                return f"<#{channel_id}> is already active"
    
        settings["enabled_channels"].append(str(channel_id))
        returnStr = f"Enabled <#{channel_id}>"
    elif active == False:
        try :
            settings["enabled_channels"].remove(str(channel_id))
            returnStr = f"Disabled <#{channel_id}>"
        except:
            returnStr = f"<#{channel_id}> is already Disabled"
    save_settings(settings, guild_id)
    return returnStr

def is_channel_enabled(guild_id, channel_id) -> bool:
    settings = load_settings(guild_id)
    for channel in settings["enabled_channels"]:
        if channel == str(channel_id):
            return True
    return False

