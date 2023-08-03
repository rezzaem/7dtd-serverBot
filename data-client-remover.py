import json
import datetime
import xml.etree.ElementTree as ET


try:
    # open clients data list
    with open ('clients_data','r')as f:
        data=json.load(f)
    #save today (current) time
    current_datetime = datetime.datetime.now()

    for client in data:
        # check for test server clients (24 h)
        if client.get('product_id') =='975':
            added_datetime = datetime.datetime.strptime(client.get('date_added'), '%Y-%m-%d %H:%M:%S')
            time_spent = current_datetime - added_datetime

            if time_spent.total_seconds() >= 24 * 60 * 60: # for 24 hour





except FileNotFoundError:
    print("clients_data file not found near py app")
