import json
import requests

graph_url = "https://graph.facebook.com/v4.0/me/messages"


def send_message(recipient_id, message_text,PAT):
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post(graph_url, params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def send_quick_reply(recipient_id, PAT, message_text):
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": message_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Mountain Bike",
                    "payload": "MOUNTAIN_SELECTED",
                    "image_url": "https://cdn4.vectorstock.com/i/1000x1000/95/53/mountain-bike-climbing-round-icon-vector-16679553.jpg"
                }, {
                    "content_type": "text",
                    "title": "Speed bike",
                    "payload": "SPEED_SELECTED",
                    "image_url": "https://i.pinimg.com/originals/74/4b/20/744b20a7d6444555867de6a16ecfc4bc.png"
                }
            ]
        }
    })
    r = requests.post(graph_url, params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def send_mobile_number(recipient_id,PAT,message_text):
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": message_text,
            "quick_replies": [
                {
                    "content_type": "user_phone_number"
                }
            ]
        }
    })
    r = requests.post(graph_url, params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def send_image_message(recipient_id, image_path, PAT):
    if image_path is None:
        print("Invalid Image Path")
        raise Exception

    params = {
        "access_token": PAT,
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {"id": str(recipient_id)},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_path
                }
            }
        }
    })

    files = {
        'filename': "rendered_image.png",
        'media': open(image_path, 'rb')
    }

    r = requests.post(graph_url, params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def send_image_url_message(recipient_id, image, PAT):
    if image is None:
        print("Gif not found Exception")
        raise Exception

    # url = request.base_url + "/" + image.split("zinkybot")[1].replace("\\", "/")
    # url = url.replace("///", "/")

    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image,
                    "is_reusable": True
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)