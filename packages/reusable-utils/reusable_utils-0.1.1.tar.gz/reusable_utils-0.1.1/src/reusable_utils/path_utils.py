import sys
import os

def get_project_source_path(source_name: str = 'Algotrading') -> None:
    """
    Adds the source path to the system path dynamically based on the provided source name.

    This function determines the directory of the current notebook, splits the path into parts,
    and constructs a relative path to the specified source folder. If the constructed path is
    not already in `sys.path`, it appends it.

    Args:
        source_name (str): The name of the source folder to locate in the path. Defaults to 'Algotrading'.

    Returns:
        None
    """
    # Dynamically determine the notebook's directory
    path = os.path.dirname(os.path.abspath('__file__'))
    path_parts = path.split(os.sep)
    i = path_parts.index(source_name)

    for j in range(i + 1, len(path_parts)):
        path_parts.remove(path_parts[j])
    path_parts.insert(1, '\\')

    # Join the parts to create a relative path
    source_path = os.path.join(*path_parts)

    if source_path not in sys.path:
        sys.path.append(source_path)
    
    return source_path