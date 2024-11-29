import json


def get_a_jsonfile_structure(jsonfile):
    with open(jsonfile, 'r') as f:
        data = json.load(f)
    extra_fields_groups = data['elabftw']['extra_fields_groups']
    extrat_fields = data['extra_fields']

    return extra_fields_groups, extrat_fields


def get_indices(extra_fields_groups):
    indice = 1
    for group in extra_fields_groups:
        if group['id'] >= indice:
            indice = group['id']
    return indice+1


def replace_id(extra_fields_groups, extrat_fields, indice):
    """
    Replace the 'id' of each group in 'extra_fields_groups' and update 'group_id'
    in 'extrat_fields' to match the new 'id'.

    Args:
    extra_fields_groups (list): List of dictionaries representing group fields.
    extrat_fields (dict): Dictionary of extra fields where each value contains 'group_id'.
    indice (int): Starting index for replacing 'id'.

    Returns:
    tuple: Updated 'extrat_fields' and 'extra_fields_groups'.
    """
    # Sort the fields based on 'group_id' and 'id'
    sorted_extrat_fields = sorted(extrat_fields.items(), key=lambda x: x[1]['group_id'])
    sorted_extrat_fields_groups = sorted(extra_fields_groups, key=lambda x: x['id'])
    print(sorted_extrat_fields[0])
    print(sorted_extrat_fields[1])
    # Create a mapping of old_id to new_id and update 'id' in extra_fields_groups
    matched_indice = {}
    list_old_indice = []
    for group in sorted_extrat_fields_groups:
        old_id = group['id']
        group['id'] = indice
        matched_indice[old_id] = indice
        list_old_indice.append(old_id)
        indice += 1

    # Update the 'group_id' in extrat_fields to match new 'id' in extra_fields_groups
    for k, v in sorted_extrat_fields:
        old_id = v.get('group_id')
        if old_id in matched_indice:
            v['group_id'] = matched_indice[old_id]

    return sorted_extrat_fields_groups, sorted_extrat_fields


def merge_jsonfiles(jsonfile_list_sorted, json_output):
    """
    Merge multiple json files, updating 'extra_fields_groups' and 'extra_fields' and renaming 'id' and 'group_id' sequentially.

    Args:
    jsonfile_list_sorted (list): List of sorted json files to merge.
    json_output (str): Path to the output json file.

    Returns:
    None
    """
    # Load the first file to use as the base structure
    with open(jsonfile_list_sorted[0], 'r') as f:
        data = json.load(f)

    main_extra_fields_groups = data['elabftw']['extra_fields_groups']
    main_extrat_fields = data['extra_fields']

    # Get the starting 'indice' for renaming the ids
    indice = get_indices(main_extra_fields_groups)
    jsonfile_list_sorted = jsonfile_list_sorted[1:]  # Skip the first file

    # Process each additional json file
    for jsonfile in jsonfile_list_sorted:
        # Extract the structure of extra fields from the json file
        extra_fields_groups, extrat_fields = get_a_jsonfile_structure(jsonfile)

        # Replace the ids and group_ids and get the updated indice
        sorted_extrat_fields_groups, sorted_extrat_fields = replace_id(extra_fields_groups,
                                                                       extrat_fields, indice)

        # Append groups to main list
        main_extra_fields_groups.extend(sorted_extrat_fields_groups)

        # Update the dictionary of extra fields
        main_extrat_fields.update(sorted_extrat_fields)

        # Update the indice after processing each file
        indice = max([group['id'] for group in main_extra_fields_groups]) + 1

    # Save the final merged data to the output json file
    with open(json_output, 'w') as f:
        json.dump(data, f, indent=4)


import json


def main():

    jsonfile_list_sorted = [
        'basic1.json',
        'Ephys1.json',
        'ephys2.json',
        'bas.json'
    ]

    jsonfile_list_sorted_eye_laure = [
        'Basicf.json',
        'ephys.json',     #eyetrackingspecific
        'RUNten.json',    #   10 run for laure
        'tms.json'  # her project specific



    ]

    jsonfile_list_sorted_eye3 = [
        'Basic1.json',
        'Run.json',
        'ephys2.json'

    ]
    print("done ")
    # Output json file path
    ##json_output = ' visuolaminar.json'

    #json_output = ' visuolaminar.json'

    json_output= 'Laure.json'
    json_output_eye = ' eyeform.json'
    # Call the merge function
    #merge_jsonfiles(jsonfile_list_sorted, json_output)
    #merge_jsonfiles(jsonfile_list_sorted_eye, json_output_eye)
    merge_jsonfiles(jsonfile_list_sorted_eye_laure, json_output)

    print(f'Merging completed! Output saved to {json_output}')


if __name__ == "__main__":
    main()
