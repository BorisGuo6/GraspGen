import json
import yaml
import re

from utils.file_utils import *

# read result and write to yaml
def parse_results(result_name, yaml_name):
    result_text = read_txt_file(result_name)

    # get first "{"
    index_of_brace = result_text.find("{")
    dict_string = result_text[index_of_brace:]

    # convert string to dict
    result_dict = convert_str_to_json(dict_string)

    # save to yaml
    write_yaml_file(yaml_name, result_dict)

def split_in_star(text):
    pattern = r'\*\*\*(.+?)\*\*\*'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        code_string = match.group(1)
        return code_string
    else:
        print("No match")
        return ""

'''
Data structure

'Task'
'Sub tasks':[{'Sub task': "", "Steps": [{  xx  }] }]

"Perception": ["Detect"],
"Actionable": ["drawer handle"],
"Constraint": [],
"Target": ["drawer handle"],
"Controller": ["Move"]


'''