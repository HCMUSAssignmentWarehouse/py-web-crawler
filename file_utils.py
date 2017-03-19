import os


# Create a new file or Add data onto an existing file
def write_to_file(file_path, str_data, is_overwrite):
    if is_overwrite:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str_data)
    else:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(str_data + '\n')


def write_file_in_folder(folder, file_name, data, is_overwrite):
    path = os.path.join(folder, file_name)
    write_to_file(path, data, is_overwrite)


# Each website is a separate folder
def create_project_directory(dir):
    if not os.path.exists(dir):
        print('Creating directory ' + dir + " to save fetched data!")
        os.makedirs(dir)


# Create frontier and fetched files (if not created)
def create_data_files(folder_name, base_url):
    frontier = os.path.join(folder_name, 'frontier.txt')
    fetched = os.path.join(folder_name, "fetched.txt")
    if not os.path.isfile(frontier):
        write_to_file(frontier, base_url, True)
    if not os.path.isfile(fetched):
        write_to_file(fetched, '', True)


# Delete the contents of a file
def clear_file_contents(file_path):
    with open(file_path, 'w') as f:
        f.close()


# Read a file and convert each line to set items
# set items can only contain unique item so we choose it for make a distinct list of page to start_crawl
def file_to_set(file_path):
    results = set()
    with open(file_path, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_path):
    with open(file_path, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")
