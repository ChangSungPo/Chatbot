import json
import os
import requests
from enum import Enum
from requests_toolbelt import MultipartEncoder

from pymessenger.graph_api import FacebookGraphApi

class ContentType(Enum):
    TEXT = "text"
    LOCATION = "location"

class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"

class QuickReply:
    def __init__(self, title, payload,
                 image_url=None,
                 content_type="text"):
        self.title = title
        self.payload = payload
        self.image_url = image_url
        self.content_type = content_type

    def to_dict(self):
        reply_dict = {"content_type": str(self.content_type),
                      "payload": self.payload}
        if self.title:
            reply_dict["title"] = self.title
        if self.image_url:
            reply_dict["image_url"] = self.image_url
        return reply_dict

class Bot(FacebookGraphApi):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)

    def send_getstarted(self):
        payload = {
            "get_started": {
                "payload": "Get Started"
            }
        }
        return self.send_raw(payload)

    def send_attachment(self, recipient_id, attachment_type, attachment_path,
                        notification_type=NotificationType.regular):
        tmp = {"is_reusable":str(True)}
        payload = {
            'recipient': f'{{"id": {str(recipient_id)}}}',
            'notification_type': str(notification_type),
            'message': f'{{"attachment": {{"type": {attachment_type},"payload": {tmp}}}}}',
            'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'))
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        return requests.post(self.graph_url, data=multipart_data,
                             params=self.auth_args, headers=multipart_header).json()

    def send_text_message(self, recipient_id, message):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message
            }
        }
        return self.send_raw(payload)

    def send_message(self, recipient_id, message):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': message
        }
        return self.send_raw(payload)

    def send_generic_message(self, recipient_id, elements):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
            }
        }
        return self.send_raw(payload)

    def send_button_message(self, recipient_id, text, buttons):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }
        }
        return self.send_raw(payload)

    def send_image(self, recipient_id, image_path, notification_type=NotificationType.regular):
        return self.send_attachment(recipient_id, "image", image_path, notification_type)

    def send_image_url(self, recipient_id, image_url):
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'image',
                        'payload': {
                            'url': image_url
                        }
                    }
                }
            )
        }
        return self.send_raw(payload)

    def send_quick_replies(self, user_id, title, reply_list):
        replies = list(dict())
        for r in reply_list:
            replies.append(r.to_dict())
        message = {'test':title, 'quick_replies': replies}
        tmp = {
            'recipient': json.dumps(
                {
                    'id': user_id
                }
            ),
            'message': json.dumps(
                message
            )                        
        }      
        return self.send_raw(tmp)       

    def send_action(self, recipient_id, action):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': action
        }
        return self.send_raw(payload)
        
    def _send_payload(self, payload):
        ''' Deprecated, use send_raw instead '''
        return self.send_raw(payload)
        
    def send_raw(self, payload):
        request_endpoint = '{0}/me/messages'.format(self.graph_url)
        response = requests.post(
            request_endpoint,
            params=self.auth_args,
            json=payload
        )
        result = response.json()
        return result

    def send_audio_url(self, recipient_id, audio_url):
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'audio',
                        'payload': {
                            'url': audio_url
                        }
                    }
                }
            )
        }
        return self.send_raw(payload)

    def send_video_url(self, recipient_id, video_url):
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'audio',
                        'payload': {
                            'url': video_url
                        }
                    }
                }
            )
        }
        return self.send_raw(payload)

    def send_file_url(self, recipient_id, file_url):
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'file',
                        'payload': {
                            'url': file_url
                        }
                    }
                }
            )
        }
        return self.send_raw(payload)
