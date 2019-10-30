import apiai
import json
import requests
from msg import *
from dbconn import *
from flask import Flask, request, render_template

app = Flask(__name__)
dbcnn = Dbconn()

# Facebook Messenger Configuration
recipient_id = None
VTK = 'huayrabot_prueba_ngrok'
PAT = 'EAAIDG5XlCi0BAErvhlpccLsEk7vbQ76qwjhwW6BHIBLubBd4DX7FgEfZBOyo0QKatWD7xWv0X2osvOK7W1sGOnUbObwZAc9VYR629EBjsVz1ity2VzvMw2ZBIEBGfi1cb9rtoMu2qx5cfdr56uSIgJCnZABHVDvvoTU9GM6APDK4xOrdydMOgCgaGGHgL7UZD'

# Dialogflow Configuration
CAT = 'f5fceddd39b64721ae2e6b390381c694'


# images
IMG_URL = 'https://i.giphy.com/xT0GqrJNbZkRcr2Jgc.gif'

def nlp_fallback(input_text, session_id):
    #dbwrite = False
    ai = apiai.ApiAI(CAT)
    req = ai.text_request()
    req.lang = 'sp'  # 'sp' para español-en inglés
    req.session_id = session_id
    req.query = input_text
    response = req.getresponse()
    raw = json.loads(response.read())
    if raw['status']['code'] == 200:
        booking=raw['result']['parameters']
        if 'cursos' in booking.keys():
            if booking['cursos'] != "":
                curso=booking['cursos']
                print(curso)
        if 'email' and 'given-name' and 'last-name' in booking.keys():
            
            if booking['email'] and booking['given-name'] and booking['last-name'] != "":
                print(curso)
                print(booking['email'])
                print(booking['given-name']+" "+booking['last-name'])
            
        response_text = raw['result']['fulfillment']['messages'][0]['speech']
    else:
        raise Exception('Dialogflow Exception:' + raw['status']['errorType'])
    return response_text


@app.route('/', methods=['GET'])
def verify():

    # Cuando el endpoint esta registrado como webhook, debe responder el echo de vuelta
    # El valor del 'hub.challenge' se recibe en los argumentos de la consulta
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VTK:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return render_template("index.html"), 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                # the facebook ID of the person sending you the message
                sender_id = messaging_event["sender"]["id"]
                # the recipient's ID, which should be your page's facebook ID
                recipient_id = messaging_event["recipient"]["id"]
                if messaging_event.get("message"):  # someone sent us a message
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]
                        if message_text == "quick":
                            send_quick_reply(sender_id, PAT)
                        response = nlp_fallback(message_text, sender_id)
                        #send_mobile_number(sender_id,PAT,"Bríndeme su número de celular")
                        send_message(sender_id, str(response),PAT)
                    if "attachments" in messaging_event["message"]:  # contains an image, location or other
                        attachment = messaging_event["message"]["attachments"][0]
                        if attachment['type'] == 'image':
                            message_image = attachment["payload"]["url"]
                            send_location_message(sender_id, "Please let me know where can we pick the bike up", PAT)
    return "ok", 200



if __name__ == '__main__':
    dbcnn.get_collection("reservaciones")
    app.run(debug = True, port=5500)