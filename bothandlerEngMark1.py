#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os
import time
import datetime
import boto3
import json

import vision as vision
import email_reply as email_reply
import visionAddress as visionAddress

from boto3.dynamodb.conditions import Attr
from messenger.bot import Bot
from pymessager.message import ActionButton, ButtonType

def get_btn_dict(btn_list):
    return [button.to_dict() for button in btn_list]

client = Bot(os.environ['ACCESS_TOKEN'])

# we use dynamodb in AWS to record the status of every user so  that the ChatBot is able to contiue the chat with them from time to time
session = boto3.Session(aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
                        region_name = os.environ['REGION_NAME'])
mydb = session.resource('dynamodb')
tablevoiceone = mydb.Table('voiceone') # we use a table named 'voiceone' to do above works. sender id as the unique key.
tablereport = mydb.Table('bikereport') # this table is to save all report data from users.
tablereportbackup = mydb.Table('bikereportbackup') # this table is to save all report data from users.

google_API_Key = os.environ["GoogleAPIKey"]
img_great = os.environ["GREAT"]
img_sorry = os.environ["SORRY"]
img_cry = os.environ["CRY"]
img_heihei = os.environ["HEIHEI"]
img_letsgo = os.environ["LETSGO"]
img_stop = os.environ["STOP"]
img_doorplate = os.environ["DOORPLATE"]
img_OMG = os.environ["OMG"]
img_recycline = os.environ["Recyicline"]

title0 = "Welcome to BikeR's project menu, I am Cyclone, your digital assistant."

buttons0 = [
    ActionButton(ButtonType.POSTBACK, "Start Recycling", payload = "Start Recycling"),
    ActionButton(ButtonType.POSTBACK, "Project info", payload = "Project info"),
    ActionButton(ButtonType.POSTBACK, "My Stats", payload = "My Stats"),
]
buttons0 = [button.to_dict() for button in buttons0]

buttons1 = [
    ActionButton(ButtonType.POSTBACK, "To Menu", payload = "To Menu"),
]
buttons1 = [button.to_dict() for button in buttons1]

title2 = "BikeR is a pubic service project founded by a group of students in 2016, the our goal is to make the streets cleaner by reporting unused and broken bikes to the government's cleaning team. "

buttons2 = [
    ActionButton(ButtonType.POSTBACK, "To Menu", payload = "To Menu"),
    ActionButton(ButtonType.POSTBACK, "Broken Bikes?", payload = "Broken Bikes?"),
    ActionButton(ButtonType.POSTBACK, "Recycling Process", payload = "Recycling Process")
]
buttons2 = [button.to_dict() for button in buttons2]

buttons3 = [
    ActionButton(ButtonType.POSTBACK, "Change Name", payload = "Change Name"),
    ActionButton(ButtonType.POSTBACK, "Change Phone Number", payload = "Change Phone Number"),
]
buttons3 = [button.to_dict() for button in buttons3]

buttons3a = [
    ActionButton(ButtonType.POSTBACK, "Upload Photos", payload = "Upload Photos"),
    ActionButton(ButtonType.POSTBACK, "Change Name", payload = "Change Name"),
    ActionButton(ButtonType.POSTBACK, "Change Phone Number", payload = "Change Phone Number"),
]
buttons3a = [button.to_dict() for button in buttons3a]

buttons3b = [
    ActionButton(ButtonType.POSTBACK, "Upload Photos", payload = "Upload Photos"),
]
buttons3b = [button.to_dict() for button in buttons3b]

buttons4 = [
    ActionButton(ButtonType.POSTBACK,"Confirm Upload", payload = "Confirm Upload"),
    ActionButton(ButtonType.POSTBACK,"To Menu", payload = "To Menu")
]
buttons4 = [button.to_dict() for button in buttons4]

buttons5 = [
    ActionButton(ButtonType.POSTBACK,"Manual", payload = "Manual"),
    ActionButton(ButtonType.POSTBACK,"To Menu", payload = "To Menu")
]
buttons5 = [button.to_dict() for button in buttons5]

buttons6 = [
    ActionButton(ButtonType.POSTBACK,"detail", payload = "detail"),
    ActionButton(ButtonType.POSTBACK,"abandon", payload = "abandon")
]
buttons6 = [button.to_dict() for button in buttons6]

buttons7 = [
    ActionButton(ButtonType.POSTBACK, "Feedback", payload = "Feedback"),
    ActionButton(ButtonType.POSTBACK,"To Menu", payload = "To Menu")
]
buttons7 = [button.to_dict() for button in buttons7]

levelname = ["rookie", "slightly advanced rookie", "level 3 apprentice", "level 2 apprentice", "level 1 apprentice", "rank 9 priest", "rank 8 priest", "rank 7 priest", "rank 6 priest", "rank 5 priest", "rank 4 priest", "rank 3 mentor", "rank 2 mentor", "Chosen Priest", "elder", "High Priest", "legendary bard", "legendary mage", "illuminati follower", "illuminati priest", "illuminati"]

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def handle_message(messaging_event):  # the entrance of the chatbot. this function will be excuted for every message the user send to chatbot.
    print("messaging_event:")
    print(messaging_event)
    talkuser(messaging_event)  # call the function name 'talkuser' in below

def talkuser(messaging_event):
    recipient_id = messaging_event["sender"]["id"] #get user's unique ID to response to 
    resp = tablevoiceone.get_item(Key={'sender_idz':recipient_id}) #get the item values from dynamodb with the user's ID
    print(resp)
    if (len(resp)<2):  #if there is no any item matchs the user's ID, means this is a new user for the fanpage messenger 
        tablevoiceone.put_item(Item=
        {
            'sender_idz':recipient_id, 
            'namez':"<empty>",
            'pnum':"<empty>",
            'switch':0,
            'picture':0,
            'correct':-1,
            'newclient':1,
            'credit':"0.0", 
            'totalz':0,
            'consecution':0,
            'localz':0,
            'score':0
        })  #create a new item with default value
    resp = tablevoiceone.get_item(Key={'sender_idz':recipient_id}) #get user info by id from the cloud database
    item = resp['Item'] #arange the list 'item' with the data in database for this user
    switch = item["switch"] #get 'switch' value. It descript the status of the user, for example switch=7 means the user is giving feedback to us
    if "postback" in messaging_event:   #In the case that the user send a postback, a special type of message. Postback is button clicked.
        payloadtx = messaging_event["postback"]["title"] #recognize response and arrange it to the valiable 'payloadtx'
        if payloadtx== "Get Started" or payloadtx == "To Menu" or payloadtx =="To Menu": # in case that the user go to the entrance of the conversation
            client.send_image_url(recipient_id, img_letsgo)
            client.send_button_message(recipient_id, title0, buttons0) #send text and buttons to welcome new user
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #update user status to entrance         
        
        elif payloadtx == "Project info": #if the user wants to know more about the initiative
            client.send_button_message(recipient_id, title2, buttons2) #send event info and more buttons to link to other info
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #update user status to entrance        
        
        elif payloadtx == "Broken Bikes?": #if the user wants to know more about the criteria of broken bike to be recycled.
            client.send_button_message(recipient_id, "If a bike has lost parts or is extremely rusted or in other ways unusible, it is ready to be recycled", buttons2) #send info and buttons
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #update user status to entrance        
        
        elif payloadtx == "Recycling Process": # wants to know the process of recycling broken bike.
            client.send_image_url(recipient_id, img_recycline) #send an image 
            client.send_button_message(recipient_id, "Bike recycling process:after the cleaning team gets a report, they will investigate the report in three days, if it is acceptible for recycling, they will stick an note on the bike, if the note is still there after a week, the bike will be put in a shed, the picture of the bike will be put on a website, if the owner does not claim it, the bike will then be recycled.", buttons2) #send info and buttons
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #update status to entrance        
        
        elif payloadtx == "Feedback": # to send feedback to us
            client.send_button_message(recipient_id, "we respect your opinion, please wirte down your ideas or problems here. \n\n If you don't want to write anything, you can click the button below to go to menu.", buttons1) #send message and button
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 7}) #set status to typing        
        
        elif payloadtx == "Change Name": # to change user's name
            client.send_button_message(recipient_id, "Please write the name you want us to know you by below. \n\nIf you don't want to change your ID, you can press the button below to go to menu", buttons1) #send message and button
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 1}) #set status to typing        
        
        elif payloadtx == "Change Phone Number": # to change user's phone number
            client.send_button_message(recipient_id, "Please write down your phone number. \n\nIf you don't want to change your number, press the button below to go to menu", buttons1) #send message to typing
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 2}) #set status to typing        
        
        elif payloadtx == "My Stats": # to show user's achievements
            ilv = round(float(item['credit']))+min(int(item['totalz']),50)//5 
            client.send_button_message(recipient_id,"User ID: "+item['namez']+"\nContact Number: "+item['pnum']+"\nCredit: "+str(round(float(item['credit'])) )+"\nYour level is: ["+ levelname[ilv]+"]\nYou have reported "+str(item['totalz'])+" bikes.\nYou have recycled 0 bikes.\nNot recyled bikes: "+str(item['totalz'])+"\nFollowing are your reports: ", buttons1) #give status report
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #set status to entrance and update the total report number        
            resp1 = tablereport.scan(FilterExpression=Attr('sender_idz').eq(recipient_id)) #get the reported item values from dynamodb 'bikereport' with the user's ID
            print('resp1')
            print(resp1)
            for i in resp1['Items']:
                btn_tmp = [ActionButton(ButtonType.POSTBACK, "Detail", payload = i['timestampz']),ActionButton(ButtonType.POSTBACK, "Abandon", payload = i['timestampz'])]
                client.send_button_message(recipient_id, "Report Date: "+i['timestampz'][0:10]+"\nLocation:"+i['address']+"\nStatus: "+i['status'], get_btn_dict(btn_tmp))
        
        elif payloadtx == "Detail":
            resp1 = tablereport.scan(FilterExpression=Attr('sender_idz').eq(recipient_id) & Attr('timestampz').eq(messaging_event["postback"]["payload"])) #get the reported item values from dynamodb 'bikereport' with the item ID matching with timestampz field
            print(resp1)
            for i in resp1['Items']:
                client.send_image_url(recipient_id, i['bikephoto']) #send an image 
                btn_tmp = [ActionButton(ButtonType.POSTBACK, "Abandon", payload = i['timestampz']), ActionButton(ButtonType.POSTBACK, "To Menu", payload = "To Menu")]
                client.send_button_message(recipient_id,"User ID: "+i['namez']+"\nContact: "+i['pnum']+"\nReport Date: "+i['timestampz'][0:10]+"\nLocation: "+i['address']+"(detail:"+str(i['details'])+")"+"\nStatus: "+i['status']+"\nUpdate Date: "+i['updatedate'][0:10],get_btn_dict(btn_tmp))
        
        elif payloadtx == "Abandon":
            resp1 = tablereport.scan(FilterExpression=Attr('sender_idz').eq(recipient_id) & Attr('timestampz').eq(messaging_event["postback"]["payload"])) #get the reported item values from dynamodb 'bikereport' with the item ID matching with timestampz field
            for i in resp1['Items']:
                client.send_image_url(recipient_id, img_cry)
                btn_tmp = [ActionButton(ButtonType.POSTBACK, "Confirm Abandon", payload = i['timestampz']), ActionButton(ButtonType.POSTBACK, "To Menu", payload = "To Menu")]
                client.send_button_message(recipient_id,"Abandon report?", get_btn_dict(btn_tmp))
        
        elif payloadtx == "Confirm Abandon":
            resp1 = tablereport.scan(FilterExpression=Attr('sender_idz').eq(recipient_id) & Attr('timestampz').eq(messaging_event["postback"]["payload"])) #get the reported item values from dynamodb 'bikereport' with the item ID matching with timestampz field
            print('\n\n\n\n\nresp1')
            print(resp1)
            for i in resp1['Items']:
                tablereportbackup.put_item(Item=i)  #copy a record from bikereport table to bikereportbackup table for backup purpose before deleting it 
            tablereport.delete_item(Key={'rid': resp1['Items'][0]['rid']})  # delete it from bikereport table
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, totalz = :b",ExpressionAttributeValues={':a': 0, ':b': int(item['totalz'])-1}) #set status to entrance and update the total report number        
            client.send_button_message(recipient_id,"Report deleted successfully", buttons1) 
        
        elif payloadtx == "Start Recycling": # to start to report a broken bike
            if item['namez']=='<empty>' or item['pnum']=='<empty>': #if either usermane or phone number is not provided
                # client.send_image_url(recipient_id, img_OMG)
                client.send_button_message(recipient_id, "The cleaning team requires you to provide your real name and number. \n\n User ID:"+item['namez']+"\n contact number:"+item['pnum'], buttons3) #ask for name and number
            else: #existing number and name
                client.send_button_message(recipient_id, "Please upload a photo of the bike/bikes you wish to report. \n\n user ID:"+item['namez']+"\n contact:"+item['pnum'], buttons3a) # ask user to send image of broken bike 
                tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 3}) #send photo        
        
        elif payloadtx == "Upload Photos": # to upload an image of broken bike
            # client.send_image_url(recipient_id, img_letsgo)
            client.send_text_message(recipient_id,"Please upload a photo of the bike/bikes you wish to report.") #ask for photo
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 4}) #send photo        
        
        elif switch==6 and (payloadtx == "Confirm Upload" or payloadtx == "Manual"): # to confirm reporting
            final = float(int(item['score']) + float(item['credit'])*int(item["totalz"]))/(int(item["totalz"])+1) #recalculate credit score including the score of new report
            if payloadtx == "Confirm Upload": # if the report was recognized by AI as a high score one and the user confirmed to sumbit.
                email_reply.send_email("bicyclerecycleorg@gmail.com","<BikeR> User report:", "Dear sir/madam, \n\n This is a report from one of <BikeR>'s users. The report has already been authenticated and is likely correct. Please send workers to the address. \n\n report info: \n User ID: "+item['namez']+"\n contact number: "+item['pnum']+"\n address: "+item['email']+item['address']+"\n photo: "+item['urlz']+"\n\n AI score:  "+str(item['score'])+" points(out of 10)\n\n Thank you for your cooperation. \n\n from, \n <BikeR> volenteers") #send email
                client.send_text_message(recipient_id,"The report has been sent, in about a week, the cleaning team will come to check on the bike. ") #respond confirmation
            else:  # payloadtx == "manual"  # if this is a report with low score and the user is still keen to sumbit it.
                email_reply.send_email("bicyclerecycleorg@gmail.com","Manual processing request: BikeR's User report", "Dear sir/madam, \n\n This is a project report from <BikeR>'s Users, our AI thought the report was invalid, however, the user insists that it is correct and requests manual processing. \n\n repot info: \n User ID: "+item['namez']+"\n contact number: "+item['pnum']+"\naddress: "+item['email']+item['address']+"\n photo: "+item['urlz']+"\n\n AI score: "+str(item['score'])+" points(out of 10)\n\n Thank you for your cooperation. \n\n from, \n <BikeR> volenteers") #send email
                client.send_text_message(recipient_id,"The report has been sent to BikeR's volemteers, if it is valid, the report will still be sent. In about a week, the clean team will go and check on it.")                
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, score = :b, credit = :c, totalz = :d, picture = :e, correct = :f, newclient = :g, consecution = :h, localz = :i",ExpressionAttributeValues={':a': 0, ':b':0, ':c':str(final), ':d':int(item["totalz"])+1, ':e':0, ':f':-1, ':g':0, ':h':0, ':i':0 }) #reset status        
            tablereport.put_item(Item=
                {
                    'rid':int(time.mktime(datetime.datetime.now().timetuple())),
                    'timestampz':str(datetime.datetime.now()), 
                    'sender_idz':recipient_id,
                    'namez':item['namez'],
                    'pnum':item['pnum'],
                    'bikephoto':item['urlz'], 
                    'cityz':item['email'], 
                    'address':item['address'], 
                    'score': item['score'], 
                    'latz': item['latz'], 
                    'longz': item['longz'], 
                    'status':"reported", 
                    'handler':"unsigned", 
                    'updatedate':str(datetime.datetime.now()),
                    'details':item['details']
                })  #create a new item with default value
            client.send_button_message(recipient_id, "Your opinion is very important to use, please give us some feedback so we can continue to improve!", buttons7) #send entrance buttons
        
        elif switch==5 and payloadtx == "Add Detail": # to add more details for the address
            btn_tmp = [ActionButton(ButtonType.POSTBACK, "address_correct", payload = messaging_event["postback"]["payload"])]
            client.send_button_message(recipient_id, "Address:"+messaging_event["postback"]["payload"]+"\n\nPlease input your details in text.\nIf not, please click 【address_correct】 button.", get_btn_dict(btn_tmp)) #send message and button
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 8}) #set status to typing        
        
        elif switch==8 and payloadtx == "Re-Detail": # to add more details for the address
            btn_tmp = [ActionButton(ButtonType.POSTBACK, "address_correct", payload = messaging_event["postback"]["payload"])]
            client.send_button_message(recipient_id, "Location: "+messaging_event["postback"]["payload"]+"(Detail: "+item['details']+")\n\nPlease input your details in text.\nTo use old details, please click 【address_correct】 button.", get_btn_dict(btn_tmp)) #send message and button            
        
        elif (switch==5 or switch==8) and payloadtx == "address_correct": # to confirm the address
            georesult = requests.get(url = "https://maps.googleapis.com/maps/api/geocode/json?language=en&address=" + messaging_event["postback"]["payload"] + "&key=" + google_API_Key)
            # georesult = requests.get(url = "http://api.opencube.tw/location/address", params = {'keyword':messaging_event["postback"]["payload"], 'key':google_API_Key}) 
            geojson = georesult.json()
            # if geojson['results'][0]['address_components'][5]['short_name']=="TW": # if it is a location within Taiwan
            #     intaiwan = 1
            # else:
            #     intaiwan = 0    
            name = item['namez']
            phone = item['pnum']
            addr = geojson['results'][0]['formatted_address']
            client.send_text_message(recipient_id,"Thanks！Cyclone will use AI to review your report, please hold...")
            score = 10
            if (len(addr)<5 or len(addr)>30):  # to discount the score if the address is too short or too long, this is a turn around be we re-train the AI
                score = round(score * 0.7)
            # if ("路" not in addr) and ("街" not in addr): # as above, discount if the address doesn't contain any important keyword
            if (geojson['results'][0]['address_components'][1]['types'][0] != 'route'):
                score = round(score * 0.8) 
            # if ("號" not in addr): # as above, discount if the address doesn't contain any important keyword
            if (geojson['results'][0]['address_components'][0]['types'][0] != 'street_number'):
                score = round(score * 0.6) 
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, score=:b, address=:c, email=:d, localz=:e, latz=:f, longz=:g",ExpressionAttributeValues={':a': 6, ':b':int(score), ':c':addr, ':d':geojson['results'][0]['address_components'][4]['long_name'], ':e':int(2), ':f':str(geojson['results'][0]['geometry']['location']['lat']), ':g':str(geojson['results'][0]['geometry']['location']['lng'])})         
            if score >= 7:
                client.send_image_url(recipient_id, img_great)
                client.send_button_message(recipient_id, "Great, you will receive "+str(score)+" points by this report！\n\nUser ID: "+str(name)+"\nContact Number: "+str(phone)+"\nLocation: "+addr+"(detail:"+str(item['details'])+")", buttons4) #send if enough points
            else:
                client.send_image_url(recipient_id, img_cry)
                client.send_button_message(recipient_id, "I'm sorry, this report only receive "+str(score)+" points! \nIt requires manual processing before sends to cleaning team. Do you still want to send this report？", buttons5) #ask to send if not enough points
        else:
            client.send_image_url(recipient_id, img_sorry)
            client.send_button_message(recipient_id, "I do not understand your message.\n\n"+title0, buttons0) #send response to those postback button that is not pre-designed.
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #set status to entrance        
    
    elif "message" in messaging_event and "quick_reply" in messaging_event["message"]:
        text = messaging_event["message"]["quick_reply"]["payload"]
        if switch == 5 and text=="textaddress":
            client.send_text_message(recipient_id,"Ok, please tell me the broke bike's location")
        if switch == 5 and text=="doorplate":
            client.send_image_url(recipient_id, img_doorplate)
            client.send_text_message(recipient_id,"Please upload the closest doorplate image, I will use AI to recognize!")
        else:
            client.send_image_url(recipient_id, img_sorry)
            client.send_button_message(recipient_id, "You have sent an unknown button!\n\n"+title0, buttons0) #send response to those postback button that is not pre-designed.
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #set status to entrance   
    
    elif "message" in messaging_event and "text" in messaging_event["message"]:   #In the case that the user send a text message
        text = messaging_event["message"]["text"] #put sent text into the valiable 'text'
        if switch == 7: #if user is sending feedbacks to us
            email_reply.send_email("bicyclerecycleorg@gmail.com","<BikeR> user feedback", "dear sir/madam\n\n this is one of <BikeR>'s user's feedback report.please foward this to the volenteers to be analyzed and discussed\n\n user ID:"+str(item['namez'])+"\n contact number:"+str(item['pnum'])+"\n feedback:\n-----------\n"+text+"\n-----------\n\n from, \n Cyclone  \n\n P.S. do not respond") #send an email with proper content to the operation team
            client.send_image_url(recipient_id, img_great)
            client.send_text_message(recipient_id,"good! the message is sent.") #send text response to user
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #status:　entrance        
            client.send_button_message(recipient_id, title0, buttons0) #send entrance buttons
        
        elif switch == 1: #change name
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, namez=:b",ExpressionAttributeValues={':a': 0, ':b':text})         
            item['namez'] = text
            if item['namez']=='<empty>' or item['pnum']=='<empty>':
                client.send_button_message(recipient_id, "you need to give your name and number to the cleaning team in order to report bikes.\n\nUser ID: "+item['namez']+"\nContact Number: "+item['pnum'], buttons3)
            else:
                client.send_button_message(recipient_id, "please send a photo of the bike/bikes you want to report.\n\nUser ID: "+item['namez']+"\nContact Number: "+item['pnum'], buttons3a)
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 3})         
        
        elif switch == 2: #change phone
            if (len(text) != 10) or (text[0:2] != "09"):
                client.send_button_message(recipient_id, "Please input correct phone number.\nCorrect phone number is able to increase your credit!\nIf don't want to change number, please click【To Menu】button。", buttons1) #send message to typing
            else:
                tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, pnum = :b",ExpressionAttributeValues={':a': 0, ':b':text})         
                item['pnum'] = text
                if item['namez']=='<empty>' or item['pnum']=='<empty>':
                    client.send_button_message(recipient_id, "you need to give your name and number to the cleaning team in order to report bikes.\n\nUser ID: "+item['namez']+"\nContact Number: "+item['pnum'], buttons3)
                else:
                    client.send_button_message(recipient_id, "Please send a photo of the bike/bikes you want to report.\n\nName: "+item['namez']+"\nContact Number: "+item['pnum'], buttons3a)
                    tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 3})                 
        
        elif switch == 5: #send address in text message
            client.send_text_message(recipient_id,"Thanks！Cyclone will use AI to organize, please hold...")
            georesult = requests.get(url = "https://maps.googleapis.com/maps/api/geocode/json?language=en&address=" + text + "&key=" + google_API_Key)
            # georesult = requests.get(url = "http://api.opencube.tw/location/address", params = {'keyword':text, 'key':google_API_Key}) 
            geojson = georesult.json()
            if geojson['status'] == 'OK':  # if the api return OK status
                client.send_text_message(recipient_id, geojson['results'][0]['formatted_address'])
                btm_tmp = [ActionButton(ButtonType.POSTBACK, "address_correct", payload = geojson['results'][0]['formatted_address']), ActionButton(ButtonType.POSTBACK, "Add Detail", payload = geojson['results'][0]['formatted_address'])]
                client.send_button_message(recipient_id, "If address is correct, please click button. Or you could upload the closest doorplate. Or you could re-input the address! Or you could add some detail about the location", get_btn_dict(btm_tmp))
                tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set address = :a, email = :b, latz = :c, longz = :d, details = :e",ExpressionAttributeValues={':a': geojson['results'][0]['formatted_address'], ':b':geojson['results'][0]['address_components'][4]['long_name'], ':c': str(geojson['results'][0]['geometry']['location']['lat']), ':d':str(geojson['results'][0]['geometry']['location']['lng']), ':e':"-"})         
            else:
                client.send_image_url(recipient_id, img_sorry)
                client.send_text_message(recipient_id, "Cyclone counldn't understand your address, you could upload the closest doorplate. Or you could re-input the address!")

        elif switch == 8: #send more details about address in text message
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a, details = :b",ExpressionAttributeValues={':a': 8, ':b':str(text)})         
            btn_tmp = [ActionButton(ButtonType.POSTBACK, "address_correct", payload = item['address']), ActionButton(ButtonType.POSTBACK, "Re-Detail", payload = item['address'])]
            client.send_button_message(recipient_id, "Detail has added!\nLocation: "+item['address']+"(Detail: "+str(text)+")", get_btn_dict(btn_tmp)) #send message and button
        
        else:
            client.send_image_url(recipient_id, img_letsgo)
            client.send_button_message(recipient_id, title0, buttons0)
            tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0}) #status: entrance        
    
    else:
        for attachment in messaging_event["message"]["attachments"]: #if message has attatchments
            if (attachment["type"] == "image") and (switch==4 or switch==0 or switch==3): #if attachment is image
                if item['namez']=='<empty>' or item['pnum']=='<empty>': #if either usermane or phone number is not provided 
                    client.send_image_url(recipient_id, img_stop)
                    client.send_button_message(recipient_id, "The cleaning team requires you to provide your real name and number!\n\nUser ID::"+item['namez']+"\ncontact number:"+item['pnum'], buttons3) #ask for name and number
                else:
                    tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set picture = :a",ExpressionAttributeValues={':a': 1}) #status: photo
                    client.send_text_message(recipient_id,"photo received, identifying...")
                    url = attachment["payload"]["url"] #initualize url
                    ans = vision.detect_labels_uri(url,"bicycle") #send to google vision api for diagnosis
                    tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set urlz = :a",ExpressionAttributeValues={':a': url})
                    if ans:
                        tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set correct = :a, switch=:b",ExpressionAttributeValues={':a': 1, ':b':5}) #set status to sending photo
                        client.send_image_url(recipient_id, img_great)
                        client.send_text_message(recipient_id,"bike identified.") #send message to tell that AI has recognized a bike in the photo
                    else:
                        tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set correct = :a, switch=:b",ExpressionAttributeValues={':a': 0, ':b':5}) #set status to sending photo
                        client.send_image_url(recipient_id, img_sorry)
                        client.send_button_message(recipient_id, "Oops! Cyclone couldn't recognize the bike, please re-upload your image!", buttons3b) # ask user to resend image of broken bike 
                        client.send_text_message(recipient_id,"If your are confident your image is correct, please provide it's location!")#send message to tell that AI can not find any bike in the photo.
                    client.send_text_message(recipient_id,"Please upload the closest doorplate image or input bike's location in text")
            
            elif (attachment["type"] == "image") and (switch==5): #if attachment is a door plate
                url = attachment["payload"]["url"] #initualize url
                addr = visionAddress.doorplate_recognition(url) # detect house number plate
                client.send_text_message(recipient_id,"Got it！Cyclone will use AI to recognize the door plate, please hold...")
                if addr:
                    client.send_text_message(recipient_id,"I have recognized some text fragments:\n"+addr)
                    client.send_text_message(recipient_id,"then try to combine....")
                    georesult = requests.get(url = "https://maps.googleapis.com/maps/api/geocode/json?language=en&address=" + addr + "&key=" + google_API_Key)
                    # georesult = requests.get(url = "http://api.opencube.tw/location/address", params = {'keyword':addr, 'key':google_API_Key})
                    geojson = georesult.json()
                    print("\n\n\n")
                    print(geojson)
                    print("\n\n\n")
                    if geojson['status'] == 'OK':  # if the api return OK status
                        client.send_text_message(recipient_id, geojson['results'][0]['formatted_address'])
                        btn_tmp = [ActionButton(ButtonType.POSTBACK,"address_correct", payload = geojson['results'][0]['formatted_address']), ActionButton(ButtonType.POSTBACK, "Add Detail", payload = geojson['results'][0]['formatted_address'])]
                        client.send_button_message(recipient_id, "If address is correct, please click button. Or you could re-upload one more time. Or you could input the address in text! Or you could add some detail about the location", get_btn_dict(btn_tmp))
                        tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set address = :a, email = :b, latz = :c, longz = :d, details = :e",ExpressionAttributeValues={':a': geojson['results'][0]['formatted_address'], ':b':geojson['results'][0]['address_components'][4]['long_name'], ':c': str(geojson['results'][0]['geometry']['location']['lat']), ':d':str(geojson['results'][0]['geometry']['location']['lng']), ':e':"-"})         
                    else:
                        client.send_image_url(recipient_id, img_sorry)
                        client.send_text_message(recipient_id, "The information is not enough.\n\nYou could re-upload one more time or input the address in text!")
                else:
                    client.send_text_message(recipient_id, "Oops! It seems not like a doorplate. You could re-upload one more time or input the address in text!")

            else: #if don't understand response. It means that the user sent a unexpected response to Chatbot.
                tablevoiceone.update_item(Key={'sender_idz': recipient_id},UpdateExpression="set switch = :a",ExpressionAttributeValues={':a': 0})
                client.send_image_url(recipient_id, img_stop)
                client.send_button_message(recipient_id, "Cyclone couldn't understand your response...\n\n"+title0, buttons0) #send message

