import json

import json

import json


def extract_groupfield_detail(jsonfile, id, new_id):
    """
    Extract details of groupfield from a json file.

    :param jsonfile: The JSON file path.
    :param id: The groupfield id to match.
    :param new_id: The new id to replace for matching fields.
    :return: groupfield name and all child fields from the group as a list of dictionaries.
    """
    list_group_field = []
    group_name = ""

    # Open and load the JSON data
    with open(jsonfile, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

    # Extract the group name by matching the id
    if 'elabftw' in data and 'extra_fields_groups' in data['elabftw']:
        for group in data['elabftw']['extra_fields_groups']:
            if group.get('id') == id or group.get('id') == str(id):
                group_name = group.get('name', '')  # Ensure name exists
                break
    else:
        raise KeyError("Expected keys 'elabftw' and 'extra_fields_groups' not found in JSON")

    # Check if 'extra_fields' exists and is a dictionary
    extra_fields = data.get('extra_fields', {})

    if isinstance(extra_fields, dict):
        for k, v in extra_fields.items():
            if v.get('group_id') == str(id) or v.get('group_id') == id:
                v['group_id'] = new_id
                list_group_field.append({k: v})

    return group_name, list_group_field


import json

def construct_extracted_json(jsonfile, id, new_id, json_output):
    """
    Construct a new JSON file with the same layout but only the extracted information.

    :param jsonfile: The original JSON file path.
    :param id: The groupfield id to match.
    :param new_id: The new id to replace for matching fields.
    :return: A dictionary with the new JSON structure.
    """
    # Use extract_groupfield_detail to get the group name and list of fields
    group_name, list_group_field = extract_groupfield_detail(jsonfile, id, new_id)
    
    # Create the new JSON structure
    new_json_structure = {
        'elabftw': {
            'extra_fields_groups': [
                {
                    'id': new_id,
                    'name': group_name
                }
            ]
        },
        'extra_fields': {field_id: details for field in list_group_field for field_id, details in field.items()}
    }
    with open(json_output, 'w') as f:
        json.dump(new_json_structure, f, indent=4)
    return new_json_structure




def add_groupfield(jsonfile, indice, groupfield_dict_list, group_name, output_jsonfile):
    # Open the JSON file and load the data
    with open(jsonfile, 'r') as f:
        data = json.load(f)

    # Update existing group ids in extra_fields_groups
    for group in data['elabftw']['extra_fields_groups']:
        if group['id'] >= indice:
            group['id'] += 1

    # Add the new group field with the given id and name
    data['elabftw']['extra_fields_groups'].append({'id': indice, 'name': group_name})
    extrafield_groups = sorted(data['elabftw']['extra_fields_groups'], key=lambda x: x['id'])
    data['elabftw']['extra_fields_groups']=extrafield_groups

    # Get or create the 'extra_fields' dictionary
    extra_fields = data.get('extra_fields', {})

    # Update group_id in existing extra fields if they have group_id >= indice
    for k, v in extra_fields.items():
        if int(v.get('group_id')) >= indice:
            v['group_id'] += 1

    # Add new groupfield_dict_list to the extra_fields
    for a_dict in groupfield_dict_list:
        for k, v in a_dict.items():
            extra_fields[k] = v

    # Update the JSON data with the modified extra_fields
    data['extra_fields'] = extra_fields

    # Save the modified JSON structure to the output file
    with open(output_jsonfile, "w") as f:
        json.dump(data, f, indent=4)


def complete_groupfield_in_jsonfile(jsonfile, groupfield_name, groupfield_detail_list,
                                    json_completed):
    """
    This function updates the 'extra_fields' section of a JSON file by assigning a new 'group_id'
    to the fields listed in 'groupfield_detail_list' if a matching 'groupfield_name' is found
    in the 'extra_fields_groups'. The modified data is then saved into a new JSON file.

    Args:
    jsonfile: str - Path to the input JSON file that contains 'extra_fields_groups' and 'extra_fields'.
    groupfield_name: str - The name of the groupfield whose ID will be applied to the new fields.
    groupfield_detail_list: list - A list of dictionaries, each representing a field to be added to 'extra_fields'.
    json_completed: str - Path to save the updated JSON file.

    Raises:
    ValueError: If the specified 'groupfield_name' is not found in the JSON file.

    Returns:
    None - The updated JSON data is saved to 'json_completed'.
    """

    is_completed = False
    new_id = None

    with open(jsonfile, 'r') as f:
        data = json.load(f)

    for group in data['elabftw']['extra_fields_groups']:
        if groupfield_name == group['name']:
            is_completed = True
            new_id = group['id']
            break

    if is_completed and new_id:
        extra_fields = data['extra_fields']

        for a_dict in groupfield_detail_list:
            for k, v in a_dict.items():
                v['group_id'] = new_id
                extra_fields[k] = v

        data['extra_fields'] = extra_fields

        with open(json_completed, 'w') as f_out:
            json.dump(data, f_out, indent=4)

    else:
        raise ValueError(f"Groupfield name '{groupfield_name}' not found in the JSON file.")


""""""
# Example usage
if __name__ == '__main__':
    group_name, groupfield_detail_list = extract_groupfield_detail("bas.json", 14, 14)
    add_groupfield("eye.json", 2, groupfield_detail_list, group_name,
                   output_jsonfile="eyespec_out.json")
    
    
result = construct_extracted_json("bas.json", 3, 2, "Run.json")

print(json.dumps(result, indent=2))
    #print(groupfield_detail_list)
    #print(group_name)




"""
new_groupdetail = {
        "type": "text",
        "value": "",
        "group_id": 4,  # Set this to your desired group ID
        "position": "0",
        "description": "New group description"
    }

    a, b = extract_groupfield_detail("file.json", 1, 5)

    list_dic = []
    l = ["fatai " + str(i) for i in range(3)]
    new_groupdetail = {"example_key": "example_value"}
    for s in l:
        list_dic.append({s: new_groupdetail})

    complete_groupfield_in_jsonfile("file1.json", "new groupe", list_dic,
                                    "json_completed.json")
"""
