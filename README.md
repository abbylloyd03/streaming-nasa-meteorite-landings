# Streaming NASA Meteorite Landings
Abby Lloyd  
21 Feb 2023

## Overview:
- The purpose of this code is to simulate the streaming of meteorite landings.
- Data is collected from a dataset of historical meteorite landings curated by NASA using an API. 
- The data is streamed using RabbitMQ. 
- Messages are sent with the name of the meteorite, the landing location of the meteorite, and the distance between the landing location and the user's location.

## Before You Begin:
Create a conda environment with the following packages installed:
- pika
- sys
- webbrowser
- pandas
- haversine
- time
- sodapy

Download and install RabbitMQ
- Instructions here: https://www.rabbitmq.com/download.html

## Files You Will Be Using:
meteorite_producer.py
- This script imports data from NASA's Meteorite Landings dataset using a NASA API, powered by Socrata.
- The data collected from the API is added to a Pandas dataset.
- After asking for the user's latitude and longitude, the distance from the user's location and the meteorite landing is calculated.
- Messages are streamed from a RabbitMQ producer.
- The messages contain the name of the meteorite, the landing location of the meteorite, and the distance between the landing and the user's location.
- The RabbitMQ admin website will open automatically when this script is run. If you want to change this feature so that you are asked whether to open the admin website, change show_offer to True.

meteorite_consumer.py
- Using RabbitMQ, this program listens for messages continuously.

## How to Run the Project:
- After environment and RabbitMQ has been set up, open a terminal and activate the environment
- Within the terminal run meteorite_producer.py
- Open a new terminal and activate the environment
- Within the second terminal run meteorite_consumer.py
- Use Ctrl+C in the terminals to interrupt the steaming process

## The Data Source:
- The data is sourced from NASA's Meteorite Landings dataset: https://dev.socrata.com/foundry/data.nasa.gov/gh4g-9sfh
- You do not need to register to access this data via the API

About the Data:
- Dataset Identifier: gh4g-9sfh
- Total Rows: 45716
- Source Domain: data.nasa.gov
- Created: 4/2/2015, 11:55:11 AM
- Last Updated: 7/20/2015, 1:49:25 PM
- Category: Space Science
- Owner: NASA Public Data

## Screenshots:


