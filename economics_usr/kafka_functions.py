"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

Desc: Apache Kafka producers - consumers
"""

from kafka import KafkaConsumer, KafkaProducer
import json
import time

DEBUG = False

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        if DEBUG:
            print('[-] Exception while connecting KAFKA')
        print(str(ex))
    finally:
        return _producer

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key)
        value_bytes = bytes(value)
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        if DEBUG:
            print('[+] Message to KAFKA published successfully.')
    except Exception as ex:
        if DEBUG:
            print('[-] Exception in publishing message to KAFKA')
        print(str(ex))

def consume_message(userID, topic):

    keys = []
    retries = 0
#    userID = 9999
    while True:
        consumer = KafkaConsumer(topic, auto_offset_reset='earliest',
            bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
        keys = [int(msg.key) for msg in consumer]
        if userID in keys:
            if DEBUG:
                print "[+] Kafka message with key: " + str(userID) + " Found"
            #print keys
            #print userID
            return True
        if retries > 5:
            if DEBUG:
                print "Failed to find the key - tries: ", retries
            return False
        retries += 1
        time.sleep(2)


def kafkasendmessage(topic, key, message):

    if DEBUG:
        print("[+] Ingesting to KAFKA... message: " + message + " into topic: " + topic)
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, topic, key, message)
    if kafka_producer is not None:
        kafka_producer.close()


def user_input_producer(userID, input_df):

    import csv
    import math
    import numpy as np
    import pandas as pd
    from parameters import parameters

    # creates input....csv in /tmp
    input_filename = '/tmp/input' + str(userID) + '.csv'
    with open(input_filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for index, row in input_df.iterrows():
            if str(index) != 'nan' and str(index) in parameters:
                writer.writerow([parameters[index]['value']])

    # sends message to kafka
    # topic_name, key, value
    topic_to_produce = "DATA_ALL_ECO_ECONOMETRIC_USERINPUT"
    kafkasendmessage(topic_to_produce, userID, "New session for econometric analysis with session ID: " + str(userID))

def user_input_consumer(userID, town):
    topic_to_consume = "DATA_ALL_ECO_ECONOMETRIC_USERINPUT"
    topic_to_produce = "ANLZ_ALL_ECO_ECONOMETRIC_USERINPUT"

    if consume_message(userID, topic_to_consume):
        if DEBUG:
            print "[+] Calling Matlab"
        #MAGIC STARTS - call matlab script
        import subprocess
        try:
            subprocess.check_call(['matlab_scripts/run_matlab_script.sh', town, str(userID)]) #town - selected town, use$
        except subprocess.CalledProcessError, e:
            print e.output
        #MAGIC ENDS

        # sends message to kafka
        # topic_name, key, value
        kafkasendmessage(topic_to_produce, userID, "Session with key: " + str(userID) + " is ready - results can be found at /tmp/Output" + str(userID) + ".csv")
        return True
    else:
        return False

def user_input_producer_SVR(userID):
    # sends message to kafka
    # topic_name, key, value
    topic_to_produce = "DATA_ALL_ECO_SVR_USERINPUT"
    kafkasendmessage(topic_to_produce, userID, "New session for SVR analysis with session ID: " + str(userID))

def user_input_consumer_SVR(userID, default_files_counter, town):
    topic_to_consume = "DATA_ALL_ECO_SVR_USERINPUT"
    topic_to_produce = "ANLZ_ALL_ECO_SVR_USERINPUT"

    if consume_message(userID, topic_to_consume):
        if DEBUG:
            print "[+] Calling Matlab"

        if default_files_counter == 2:
            from functions_svr import copy_template_result_files
            copy_template_result_files(town, userID)
        else:

            # if file is uploaded use it
            #MAGIC STARTS - call matlab script
            import subprocess
            subprocess.check_call(['matlab_scripts/run_matlab_script_svr.sh', town, str(userID)]) #town - selected town, userID 9digit unique session ID
            #MAGIC ENDS

        return True
    else:
        return False


