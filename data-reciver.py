import json
from flask import Flask, request, jsonify, abort
import time
import xml.etree.ElementTree as ET
import datetime

#--------------------------
def save_client(j_data):
    # Define variables
    steam_id = None
    product_id = None
    order_number = None
    add_time = None

    # Find items in received JSON from WordPress
    for item in j_data["meta_data"]:
        if item["key"] == "billing_steamid":
            steam_id = item["value"]
            break
    for item in j_data["line_items"]:
        product_id = item["product_id"]
        break
    order_number = j_data['id']
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_time= current_datetime

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

    # Make client
    person_info = {
        "steam_id": steam_id,
        "product_id": product_id,
        "order_number": order_number,
        "add_time": add_time
    }
    check_for_rejister_before=False
    # check if client has buyed free plan it hsould can not save 24 h again
    if order_number==809: #0rder number 809 in our wordpress beking to 24h free plan
        for person in person_info_list:
            if person.get("steam_id")==person_info.get("steam_id"):
                check_for_rejister_before=True
    if check_for_rejister_before==False:
        person_info_list.append(person_info)
        add_to_server(steam_id)
    # Save
        with open("clients_data.json", "w") as file:
            json.dump(person_info_list, file,indent=4)
    else:
        print("person is already buyed server test")


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

if __name__ == "__main__":
    app.run(debug=True)
