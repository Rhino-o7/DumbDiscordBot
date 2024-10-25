
import markovify
import json
import os


def gen_message(guild_id, channel_id) -> str:
    try:
        with open('src/guild_data/' + str(guild_id) + '/messages.json', 'r') as f:
            data = json.load(f)
        
        channel_id_str = str(channel_id)

        if channel_id_str not in data:
            raise ValueError(f"Channel ID {channel_id} not found in the data.")

        channel_messages = data[channel_id_str]
        messages = " ".join([entry["content"] for entry in channel_messages])
        text_model = markovify.Text(messages, state_size=1)
        text_model.compile()
        generated_message = text_model.make_sentence(tries=100)
       
        if generated_message == None:
            return None
         
        return generated_message

    except Exception as e:
        return None
    

def gen_message_all(guild_id):
    try:
        with open('src/guild_data/' + str(guild_id) + '/messages.json', 'r') as f:
            data = json.load(f)
        messages = ""
        for channel in data:
            channel_messages = data[channel]
            messages += " ".join([entry["content"] for entry in channel_messages])
        text_model = markovify.Text(messages, state_size=1)
        text_model.compile()
        generated_message = text_model.make_sentence(tries=100)
       
        if generated_message == None:
            return None
         
        return generated_message

    except Exception as e:
        return None
