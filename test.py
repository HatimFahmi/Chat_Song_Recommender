from random import choice
from click import prompt
from flask import Flask, request
from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
completion = openai.Completion()

start_sequence = "\nMarvin:"
restart_sequence = "\n\nYou:"
session_prompt = "The following is a conversation with an friendly AI named Marvin. Marvin is helpful, creative, clever, and very friendly. \n\nYou: What have you been up to?\nMarvin: Watching old movies.\nYou: Did you watch anything interesting?\nYou: Alright, have a great weekend, see you Monday.\nMarvin: Yup, you too… hey wait, what are you up to tonight, anyway?\nYou: Oh, not much, really. Maybe heading into the city with friends.\nMarvin: Cool, we’ll be down there too. Thinking dinner, maybe drinks.\nYou: Oh yeah? Here, add my number to your phone.\nMarvin: Perfect, I’ll text you later then… see where you’re at."


def bot(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.3,
        stop=[" You:", " Marvin:"]
    )

    json_response = json.dumps(response)
    rep = json.loads(json_response)

    bot_reply = rep['choices'][0]['text']

    return str(bot_reply)


def append_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


def chat_tone(chat):
    prompt = """Decide whether the chat sent by 'You' sentiment is positive, neutral, or negative.\n\nYou: """ + \
        chat + "\n\nSentiment:"

    Tone_reply = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    json_response = json.dumps(Tone_reply)
    rep = json.loads(json_response)

    bot_reply = rep['choices'][0]['text']

    return str(bot_reply)
