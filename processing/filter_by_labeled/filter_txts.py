def update_file(reference_file_path, target_file_path):
    # Read reference file
    with open(reference_file_path, 'r') as ref_file:
        reference_lines = set(ref_file.read().splitlines())

    # Read target file
    with open(target_file_path, 'r') as target_file:
        target_lines = target_file.read().splitlines()

    # Filter target lines to only include those in reference lines
    updated_lines = [line for line in target_lines if line in reference_lines]

    # Write updated lines back to the target file
    with open(target_file_path, 'w') as target_file:
        target_file.write('\n'.join(updated_lines))

# Example usage
reference_file_path = '/Volumes/My Passport for Mac/ty_saguaro_project/processing/default_removed.txt'
target_file_path = '/Volumes/My Passport for Mac/ty_saguaro_project/labels/old_all_annotations_raw/ImageSets/Segmentation/default.txt'
update_file(reference_file_path, target_file_path)
