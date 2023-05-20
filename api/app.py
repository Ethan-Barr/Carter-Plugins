from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def online():
    return "Operational"


@app.route('/webhook', methods=["POST"])
def webhook():  
    data = request.get_json()
    print(data)


    return {'output': "Hello from Vercel"}

# app.run(host='0.0.0.0', port=81)