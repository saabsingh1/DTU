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
    
    tree = ET.parse(log)  # Replace with your actual file path
    root = tree.getroot()

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


