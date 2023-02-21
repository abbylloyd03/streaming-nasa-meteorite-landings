"""
    This script imports data from NASA's Meteorite Landings dataset using
    a NASA API, powered by Socrata. The data is added to a Pandas dataset.
    After asking for the user's latitude and longitude, the distance from 
    the user's location and the meteorite landing is calculated.
    Messages are streamed from a RabbitMQ producer, containing the name of
    the meteorite, the landing location of the meteorite, and the distance 
    between the landing and the user's location.

    Use meteorite_consumer.py to continously listen for messages from this 
    producer.


    API Documentation: https://dev.socrata.com/foundry/data.nasa.gov/gh4g-9sfh

    Abby Lloyd, 21 Feb 2023

"""

#####################################################################################

# import packages
import pika
import sys
import webbrowser
import pandas as pd
import haversine as hs
import time
from sodapy import Socrata

#####################################################################################

# define variables
show_offer = False # False opens RabbitMQ admin site automatically, True gives option
import_limit = 200 # number of records to get from API
sleep_time = 4 # number of seconds to sleep before sending next message
name_of_qeueu = 'meteorite' # qeueu to send message


#####################################################################################

# import data from api and prepare data
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.nasa.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.nasa.gov,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First [x] results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("gh4g-9sfh", limit=import_limit)
# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
# Sort pandas DataFrame by year, ascending
sorted_df = results_df.sort_values(by=['year'])

#####################################################################################

def offer_rabbitmq_admin_site():
    """
    If show_offer is True, offer to open the RabbitMQ Admin website. 
    Otherwise, open automatically.
    """

    if show_offer == True:
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")

#####################################################################################

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """


    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

#####################################################################################


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()

    # ask the user's latitude and longitude
    input_lat = float(input('What is your latitude? '))
    input_lon = float(input('What is your longitude? '))

    
    # for each row in the sorted DataFrame
    for index in sorted_df.index:
        # access and store the meteorites name
        name = sorted_df.at[sorted_df.index[index],'name']
        # access and store the dictionary containing landing location
        geolocation = sorted_df.at[sorted_df.index[index],'geolocation']
        # store latitude of landing
        latitude = float(geolocation['latitude'])
        # store longitude of landing
        longitude = float(geolocation['longitude'])
        # store user's location
        your_loc = (input_lat, input_lon)
        # store landing location
        met_loc = (latitude, longitude)
        # calculate distance from user's location and landing location
        # round distance to 2 decimal places
        distance = round(hs.haversine(your_loc, met_loc), 2)
        # create message
        message = f'Meteorite {name} has fallen at {geolocation}. This is {distance} km from your location.'
        # send the messages to the queue 
        send_message('localhost',name_of_qeueu,message)
        # sleep for the sleep_time indicated above
        time.sleep(sleep_time)
