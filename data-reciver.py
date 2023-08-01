from flask import Flask, request, abort

app = Flask(__name__)

SECRET = "AzKosKhom1842"  # Replace with the secret key set in WooCommerce

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    secret = request.headers.get('X-WC-Webhook-Signature')
    if secret != SECRET:
        abort(403)  # Unauthorized request
    
    data = request.get_json()
    
    # Process the received webhook data
    # Replace the following print statement with your own logic
    print(data)
    
    return 'Webhook received successfully', 200

if __name__ == '__main__':
    app.run()
