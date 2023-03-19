import os.path


def get_source_file_paths(root_path, file_suffix=".java") -> str:
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        file_paths += [os.path.join(root, file) for file in files if file.endswith(file_suffix)]

    return "\n".join(file_paths)
