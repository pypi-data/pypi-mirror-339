import os

from robot.api.deco import keyword


@keyword("Get Files In Dir")
def to_file_path_pair(dir_path):
    files_list = []

    for root, dirs, files in os.walk(dir_path):
        if not files and not dirs:
            continue

        for file in files:
            full_path = os.path.join(root, file)
            files_list.append((file, full_path))

    return files_list

@keyword("Check For Uniqueness")
def is_unique(lst):
    return len(lst) == len(set(lst))

@keyword("Check For Constant Values For All Snaps")
def all_same_url(lst, expectedvalue):
    return all(item == expectedvalue for item in lst)


@keyword("Flatten_and_clean_list")
def flatten_and_clean_list(nested_list):
    flattened = []
    def flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                flatten(sub_item)
        elif item not in (None, ""):
            flattened.append(str(item))
    flatten(nested_list)
    return flattened

