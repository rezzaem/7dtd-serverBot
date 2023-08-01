import json
from flask import Flask, request,jsonify, abort

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    """This function will be called when a WooCommerce webhook is received.

    Args:
        request (flask.Request): The HTTP request object.
    """
    data = request.data
    print(f"Received data: {data}")
    # webhook_data = json.loads(request.data)
    # print(f"Received webhook event: {webhook_data['type']}")
    # print(f"Webhook data: {webhook_data}")
    try:
        json_data = json.loads(data)
        with open ('client_id.json','w') as file:
            json.dump(json_data,file)
    except json.JSONDecodeError as e:
        return abort(400, f'Invalid JSON: {e}')
    json_data[]
    return "Webhook received!"

if __name__ == "__main__":
    app.run(debug=True)
