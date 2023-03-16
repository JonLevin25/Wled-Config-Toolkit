from os import path


def path_forced_root(root_dir: str, filepath: str):
    return filepath if filepath.startswith(root_dir) else path.join(root_dir, filepath)
