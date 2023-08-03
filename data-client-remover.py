import json
import datetime
import xml.etree.ElementTree as ET

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


try:
    # open clients data list
    with open ('clients_data.json','r')as f:
        data=json.load(f)
    #save today (current) time
    current_datetime = datetime.datetime.now()

    for client in data:
        # check for test server clients (24 h)
        if client.get('product_id') =='975':
            added_datetime = datetime.datetime.strptime(client.get('date_added'), '%Y-%m-%d %H:%M:%S')
            time_spent = current_datetime - added_datetime

            if time_spent.total_seconds() >= 24 * 60 * 60: # for 24 hour
                remove_user_from_whitelist(client.get('steam_id'))
        else:
            added_datetime = datetime.datetime.strptime(client.get('date_added'), '%Y-%m-%d %H:%M:%S')
            time_spent = current_datetime - added_datetime

            if time_spent.total_seconds() >= 30 * 24 * 60 * 60: # for 30 days
                remove_user_from_whitelist(client.get('steam_id'))






except FileNotFoundError:
    print("clients_data file not found near py app")
