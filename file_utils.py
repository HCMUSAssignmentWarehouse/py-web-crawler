import os


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url, True)
    if not os.path.isfile(crawled):
        write_file(crawled, '', True)


# Create a new file or Add data onto an existing file
def write_file(path, data, is_overwrite):
    if is_overwrite:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(data + '\n')


def write_file_to_folder(folder, file_name, data, is_overwrite):
    path = os.path.join(folder, file_name)
    write_file(path, data, is_overwrite)


# Delete the contents of a file
def clear_file_contents(path):
    with open(path, 'w') as f:
        f.close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")
