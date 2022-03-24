#!/usr/bin/python
# -*- coding: utf-8 -*-

import bothandlerEngMark1 as bot_handler

import json
import os
from flask import Flask, request
from messenger.bot import Bot

app = Flask(__name__)
WEBHOOK = '/webhook'
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
# client = Bot(os.environ['ACCESS_TOKEN'])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route(WEBHOOK, methods=["GET"])
def fb_webhook():
    verify_token = request.args.get('hub.verify_token')
    if VERIFY_TOKEN == verify_token:
        return request.args.get('hub.challenge')
    else:
        return '', 403


@app.route(WEBHOOK, methods=['POST'])
def fb_receive_message():
    return ""
    data = json.loads(request.data.decode('utf8'))
    message_entries = data['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                # debug
                # sender_id = message.get('sender').get('id')
                # client.send_text_message(sender_id, "收到訊息")
                # handle message
            #     print('message')
                bot_handler.handle_message(message)
            elif message.get('postback'):
            #     print('postback')
                bot_handler.handle_message(message)
    return "Hi"


if __name__ == '__main__':
    app.run()
