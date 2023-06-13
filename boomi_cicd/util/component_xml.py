import os


def get_file_refs(location):
    # Read .componentRef file to get component id of folder/files
    file_refs = {}
    if os.path.exists(os.path.join(location, ".componentRef")):
        with open(os.path.join(location, ".componentRef"), "r") as f:
            folder_refs = f.read()
        for folder_ref in folder_refs.split("\n"):
            if folder_ref != "":
                folder_ref_split = folder_ref.split("=")
                folder_ref_id = folder_ref_split[0]
                folder_ref_name = folder_ref_split[1]
                file_refs[folder_ref_id] = folder_ref_name
    else:
        open(os.path.join(location, ".componentRef"), "w").close()
    return file_refs


def set_file_refs(location, file_refs):
    # Write .componentRef file to get component id of folder/files
    with open(os.path.join(location, ".componentRef"), "w") as f:
        for file_ref in file_refs:
            f.write("{}={}\n".format(file_ref, file_refs[file_ref]))
