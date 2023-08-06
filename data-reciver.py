import json
from flask import Flask, request, jsonify, abort
import time
import xml.etree.ElementTree as ET
import datetime
import schedule
import threading
import signal

#--------------------------
def save_client(j_data):
    # Define variables
    steam_id = None
    product_id = None
    order_number = None
    exp_time = None

    # Find items in received JSON from WordPress
    for item in j_data["meta_data"]:
        if item["key"] == "billing_steamid":
            steam_id = item["value"]
            break
    for item in j_data["line_items"]:
        product_id = item["product_id"]
        break
    order_number = j_data['id']
    

    # Open client list data JSON
    try:
        with open("clients_data.json", "r") as file:
            data = file.read()
            if data:
                person_info_list = json.loads(data)
            else:
                person_info_list = []
    except FileNotFoundError:
        person_info_list = []

    try: #opeen limit list
        with open ('809-limit-list.json','r') as f:
            limits=f.read()
            if limits:
                limit = json.loads(limits)
            else:
                limit = []
    except FileNotFoundError:
            limit=[]

    # Make client
    person_info = {
        "steam_id": steam_id,
        "product_id": product_id,
        "order_number": order_number,
        "exp_time": exp_time,
        "status":"active"
    }


    # check if client has buyed free plan it hsould can not save 24 h again-every 809 products should save in 809 blok list
    if product_id==809 and steam_id not in limit: # for 24 h clients
        for person in person_info_list: # has rejistered before but not 809
             if steam_id==person.get("steam_id"):
                old_exp_time= datetime.datetime.strptime(person.get('exp_time'),'%Y-%m-%d %H:%M:%S')
                new_exp_time=(old_exp_time+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S") # add 24 hour to client if not buy free test yet
                person['exp_time']=new_exp_time
                if person.get["status"]=="deactive":
                    person["status"]=="active"
                break
        else: # has not rejistered yet
            new_exp_time = (datetime.datetime.now()+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            person_info["exp_time"]=new_exp_time
            person_info_list.append(person_info)
            add_to_server(steam_id)

        limit.append(steam_id)
        print(f'client with steam id {steam_id} for 24h has been saved')

    # only posible for save is that the product is not free

    elif product_id!=809 : # paid products (30 days time)
        for person in person_info_list: # has rejistered before but not 809
             if steam_id==person.get("steam_id"):
                old_exp_time= datetime.datetime.strptime(person.get('exp_time'),'%Y-%m-%d %H:%M:%S')
                new_exp_time=(old_exp_time+datetime.timedelta(days=24)).strftime("%Y-%m-%d %H:%M:%S") # add 30 days  to client
                person['exp_time']=new_exp_time
                if person.get["status"]=="deactive":
                    person["status"]=="active"
                break
        else: #has not rejistered
            new_exp_time = (datetime.datetime.now()+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            person_info["exp_time"]=new_exp_time
            person_info_list.append(person_info)
            add_to_server(steam_id)
        print(f'client with steam id {steam_id} for 30 days has been saved')

                      
    with open("clients_data.json", "w") as file:
            json.dump(person_info_list, file,indent=4)

    with open ('809-limit-list.json','w') as f:
        json.dump(limit,f,indent=1)

    # elif order_number!=809: #for others
    #     person_info_list.append(person_info)

    # if order_number==809 : #0rder number 809 in our wordpress beking to 24h free plan
    #     for person in person_info_list:
    #         if person.get("steam_id")==person_info.get("steam_id"):
    #             check_for_rejister_before=True
    # if check_for_rejister_before==False:
    #     person_info_list.append(person_info)
    #     add_to_server(steam_id)
    # Save
        


def add_to_server(steam_id):
    # Parse the XML file
    server_admin_location='serveradmin.xml' # edit to location of serveradmin
    tree = ET.parse(server_admin_location)
    root = tree.getroot()

    # Create a new user element
    new_user = ET.Element("user")
    new_user.set("platform", "Steam")
    new_user.set("userid", str(steam_id))  # Replace with the actual SteamID64 of the user
    new_user.set("name", "")  # Optional: Replace with the name of the user

    whitelist_section = root.find(".//whitelist")

    # Find the last user element in the <whitelist> section
    last_user = whitelist_section.find("user[last()]")

    # Check if the last user element exists and insert the new user after it
    if last_user is not None:
        index = list(whitelist_section).index(last_user) + 1
        whitelist_section.insert(index, new_user)
    else:
        # If no user element exists in the <whitelist> section, append the new user
        whitelist_section.append(new_user)

    # Save the updated XML tree to the file with proper indentation
    ET.indent(root)
    tree.write("serveradmin.xml", encoding="utf-8", xml_declaration=True)
    print(f'client with steam id {steam_id} now can join to Server')

def remove_user_from_whitelist(user_id):
    # Parse the serveradmin.xml file and get the root element
    serveradmin='serveradmin.xml' # server admin location
    tree = ET.parse(serveradmin)
    root = tree.getroot()

    # Find the <whitelist> element
    whitelist_element = root.find('.//whitelist')
    if whitelist_element is not None:
        # Find the specific user element with the matching userid
        user_element = whitelist_element.find(f".//user[@userid='{user_id}']")
        if user_element is not None:
            # Remove the user element from the <whitelist> section
            whitelist_element.remove(user_element)
            print(f"Removed user with userid='{user_id}' from the whitelist.")

            # Save the modified XML back to the serveradmin.xml file
            tree.write('serveradmin.xml', encoding='utf-8', xml_declaration=True)
        else:
            print(f"User with userid='{user_id}' not found in the whitelist.")
    else:
        print("The <whitelist> section not found in serveradmin.xml.")

def client_remover():
    print('start client checker for remove')
    try:
    # open clients data list
        with open ('clients_data.json','r')as f:
            data=json.load(f)
        #save today (current) time
        current_datetime = datetime.datetime.now()

        for client in data:
            # check for test server clients (24 h)
            if client.get('product_id') ==809 and client.get("status")=="active":
                expire = datetime.datetime.strptime(client.get('exp_time'), '%Y-%m-%d %H:%M:%S')

                if current_datetime > expire:
                    remove_user_from_whitelist(client.get('steam_id'))
                    client["status"]="deactive"
                    
            elif client.get("status")=="active": # else default is 30 days 
                expire = datetime.datetime.strptime(client.get('exp_time'), '%Y-%m-%d %H:%M:%S')
                
                if current_datetime > expire: # for 30 days
                    remove_user_from_whitelist(client.get('steam_id'))
                    client["status"]="deactive"

        with open ('clients_data.json','w')as f:
            json.dump(data,f,indent=4)

    except FileNotFoundError:
        print("clients_data file not found near py app")


#-------------------------

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    """This function will be called when a WooCommerce webhook is received.

    Args:
        request (flask.Request): The HTTP request object.
    """
    json_data = request.get_json()

    save_client(json_data)

    return "Webhook received!"

# def run_flask():
#     # Ignore the SIGTERM signal
#     signal.signal(signal.SIGTERM, signal.SIG_IGN)
    

if __name__ == "__main__":
    # Ignore the SIGTERM signal
    import signal
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    def job_thread():
        while True:
            schedule.run_pending()
            time.sleep(60)
    threading.Thread(target=job_thread).start()

    schedule.every(30).minutes.do(client_remover)

    app.run(debug=True)

   
    