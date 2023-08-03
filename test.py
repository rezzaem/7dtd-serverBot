import json
import datetime

def add_client(client_data):
    # Load existing data from the file if it exists
    try:
        with open('clients_data.json', 'r') as f:
            clients_data = json.load(f)
    except FileNotFoundError:
        clients_data = []

    # Add the new client with the current date and time
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client_data['date_added'] = current_datetime
    clients_data.append(client_data)

    # Save the updated data back to the file
    with open('clients_data.json', 'w') as f:
        json.dump(clients_data, f, indent=4)

new_client = {
    'client_id': 1,
    'product_id': 809,
    'name': 'John Doe2',
    # Add other client data as needed
}

add_client(new_client)

def check_clients_data():
    with open('clients_data.json', 'r') as f:
        clients_data = json.load(f)

    product_id_to_check = 809
    current_datetime = datetime.datetime.now()

    for client in clients_data:
        if client.get('product_id') == product_id_to_check:
            added_datetime = datetime.datetime.strptime(client.get('date_added'), '%Y-%m-%d %H:%M:%S')
            time_spent = current_datetime - added_datetime

            if time_spent.total_seconds() >= 24 * 60 * 60:  # 24 hours in seconds
                # Call the function you want to run here
                # For example, you can call your_function(client)
                print ("yes")  # Replace "pass" with your function call
            else:
                print("no")
check_clients_data()