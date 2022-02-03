import json
import requests
import sys
import pandas as pd
import csv
import os
from threading import Thread
from queue import Queue
import datetime as datetime

queue = Queue(150)
dict_list = []
counter = 1


def to_string(s):
    """

    :param s:
    :return:
    """
    try:
        return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')

def travel_element_json(row_dict, key, value):
    """

    :param row_dict:
    :param key:
    :param value:
    :return:
    """
    # Reduction Condition 1
    if type(value) is list:
        # i=0
        for sub_item in value:
            
            travel_element_json(row_dict, key, sub_item)
    # Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            travel_element_json(row_dict, key + '##' + to_string(sub_key), value[sub_key])
            
    # Base Condition
    else:
        if key not in row_dict.keys():
            row_dict[to_string(key)] = to_string(value)
        else:
            row_dict[to_string(key)] = row_dict[to_string(key)] + '||' + to_string(value)

    return row_dict


def parse_from_root(each_item, total_element, input_file_type, element):
    """

    :param each_item:
    :param total_element:
    :return:
    """
    row_dict = {}
    global dict_list, counter
    if input_file_type == 'json':
        row_dict = travel_element_json(row_dict, element, each_item)

    print(">>>  Progress:  {} %   ".format(int((counter/total_element)*100)), end='\r')
    sys.stdout.flush()
    counter += 1
    dict_list.append(row_dict)

class ProducerThread(Thread):

    def __init__(self, element_list):
        """

        :param element_list:
        """
        super(ProducerThread, self).__init__()
        self.element_list = element_list

    def run(self):
        """

        :return:
        """
        global queue
        while self.element_list:
            each_item = self.element_list.pop()
            queue.put(each_item)


class ConsumerThread(Thread):

    def __init__(self, total_element, input_file_type, element):
        """

        :param total_element:
        """
        super(ConsumerThread, self).__init__()
        self.total_element = total_element
        self.input_file_type = input_file_type
        self.element = element

    def run(self):
        """

        :return:
        """
        global queue
        while not queue.empty():
            each_item = queue.get()
            parse_from_root(each_item, self.total_element, self.input_file_type, self.element)
            queue.task_done()

class Parse:
    
    def __init__(self,jsonData):
        self.url=''
        self.jsonData = jsonData

    def parseJson(self,data, nodeName):
        element_list = data[nodeName]
        total_element = len(element_list)
        p1 = ProducerThread(element_list)
        producer_thread_list = list()
        producer_thread_list.append(p1)
        consumer_thread_list = [ConsumerThread(total_element, 'json', nodeName) for x in range(100)]
        for each_producer in producer_thread_list:
            each_producer.start()
        for each_consumer in consumer_thread_list:
            each_consumer.start()
        for each_producer in producer_thread_list:
            each_producer.join()
        for each_consumer in consumer_thread_list:
            each_consumer.join()
        main_df = pd.DataFrame(dict_list)
        totalDistList = len(dict_list)
        return main_df,totalDistList


    def parseJsonRequest(self):
        startTime = datetime.datetime.now()
        main_df,totalDistList =self.parseJson(data=self.jsonData,nodeName='entities')
        finalTime = datetime.datetime.now()
        time_taken_minutes = ((finalTime - startTime).seconds) / 60
       
        main_df.drop(main_df.columns[[0, 3, 4]], axis = 1, inplace = True)
        main_df.drop(main_df.iloc[:, 5:], inplace = True, axis = 1)
        print(list(main_df.columns))
        main_df.rename(columns = {'entities##name':'TableName',\
        'entities##description':'Description','entities##attributes##name':'ColumnName',\
        'entities##attributes##dataType':'DataType','entities##attributes##maxLength':'DatatypeLength'}, inplace = True)
        main_df.to_csv("test.csv",index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
        # print(time_taken_minutes)
        js = main_df.to_json(orient = 'columns')
        return js
        