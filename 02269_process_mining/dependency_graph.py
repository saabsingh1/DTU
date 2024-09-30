import xml.etree.ElementTree as ET
from datetime import datetime

def log_as_dictionary(log): 
    log_dict = {}
    lines = log.split("\n")
    
    for line in lines: 
        attributes = line.split(";")
 
        if attributes != ['']:
            task_name = attributes[0]
            case_id = attributes[1]
            user_id = attributes[2]
            timestamp = attributes[3]

            if case_id not in log_dict:
                log_dict[case_id] = []
            
            log_dict[case_id].append({"task" : task_name, "user": user_id, "timestamp" : timestamp})

    return log_dict


def dependency_graph_inline(log): 
    dependency_dict = {}
    for k, v in log.items():
        for i in range(1,len(v)):
            prev_task = v[i-1]['task']
            curr_task = v[i]['task']

            if prev_task not in dependency_dict: 
                dependency_dict[prev_task] = {}

            if curr_task not in dependency_dict[prev_task]: 
                dependency_dict[prev_task][curr_task] = 0

            dependency_dict[prev_task][curr_task] += 1

    return dependency_dict
    

def read_from_file(log): 
    XES_log = {}
    try:
        tree = ET.parse("extension-log.xes")  # Replace with your actual file path
        root = tree.getroot()
        print("File loaded successfully.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except FileNotFoundError:
        print("The file was not found.")

    # Namespace used in the XML
    namespace = {'xes': 'http://www.xes-standard.org/'}

    # Function to convert string to proper type
    def convert_value(value, key):
        if key in ['cost', 'urgency']:  # Assuming these are integers
            return int(value)
        elif key == 'intervention':  # Assuming this is a boolean
            return value.lower() == 'true'
        elif key == 'time:timestamp':  # Assuming this is a datetime
            return datetime.fromisoformat(value[:-6])  # Remove timezone
        return value  # Default return as string

    # Iterate over each trace element
    for trace in root.findall('xes:trace', namespace):
        # Extract case_id
        case_id = trace.find("xes:string[@key='concept:name']", namespace).get('value')
        
        # List to hold events for the current case
        events = []
        
        # Iterate over each event in the trace
        for event in trace.findall('xes:event', namespace):
            event_attributes = {}
            
            # Get all attributes of the event
            for attribute in event:
                key = attribute.get('key')
                value = attribute.get('value')
                # Convert value to its proper type
                converted_value = convert_value(value, key)
                event_attributes[key] = converted_value
            
            # Append the event attributes dictionary to the events list
            events.append(event_attributes)
        
        # Add the case_id and events to the case_dict
        XES_log[case_id] = events

    return XES_log


    
def dependency_graph_file(log): 

    dependency_dict = {}
    for k, v in log.items():
        for i in range(1,len(v)):
            prev_task = v[i-1]['concept:name']
            curr_task = v[i]['concept:name']

            if prev_task not in dependency_dict: 
                dependency_dict[prev_task] = {}

            if curr_task not in dependency_dict[prev_task]: 
                dependency_dict[prev_task][curr_task] = 0

            dependency_dict[prev_task][curr_task] += 1

    return dependency_dict




f = """
Task_A;case_1;user_1;2019-09-09 17:36:47
Task_B;case_1;user_3;2019-09-11 09:11:13
Task_D;case_1;user_6;2019-09-12 10:00:12
Task_E;case_1;user_7;2019-09-12 18:21:32
Task_F;case_1;user_8;2019-09-13 13:27:41

Task_A;case_2;user_2;2019-09-14 08:56:09
Task_B;case_2;user_3;2019-09-14 09:36:02
Task_D;case_2;user_5;2019-09-15 10:16:40

Task_G;case_1;user_6;2019-09-18 19:14:14
Task_G;case_2;user_6;2019-09-19 15:39:15
Task_H;case_1;user_2;2019-09-19 16:48:16
Task_E;case_2;user_7;2019-09-20 14:39:45
Task_F;case_2;user_8;2019-09-22 09:16:16

Task_A;case_3;user_2;2019-09-25 08:39:24
Task_H;case_2;user_1;2019-09-26 12:19:46
Task_B;case_3;user_4;2019-09-29 10:56:14
Task_C;case_3;user_1;2019-09-30 15:41:22"""

'''
log = log_as_dictionary(f)
dg = dependency_graph_inline(log)

for ai in sorted(dg.keys()):
   for aj in sorted(dg[ai].keys()):
       print(ai, '->', aj, ':', dg[ai][aj])
'''



log = read_from_file("extension-log.xes")

for case_id in sorted(log):
    print((case_id, len(log[case_id])))

for k, v in sorted(log.items()): 
    print(k,v)

case_id = "case_123"
event_no = 0
print((log[case_id][event_no]["concept:name"], log[case_id][event_no]["org:resource"], log[case_id][event_no]["time:timestamp"],  log[case_id][event_no]["cost"]))


dg = dependency_graph_file(log)

for ai in sorted(dg.keys()):
   for aj in sorted(dg[ai].keys()):
       print(ai, '->', aj, ':', dg[ai][aj])
