import os
import sys
# Determine the current directory and project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Add the project root, tools, and files directories to sys.path
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'sql'))


def load_query(query_to_read):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory level
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    query_dir = os.path.join(parent_dir, 'sql')
    query_file = os.path.join(os.path.join(query_dir, query_to_read))
    query = ""
    with open(query_file, 'r') as file:
        query = file.read()
    return query

