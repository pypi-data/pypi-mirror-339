import re
from pathlib import Path


class TreeParser:
    """Parse a tree structure string into a list of files and directories."""

    def __init__(self, tree_content):
        """
        Initialize the parser with tree content.

        Args:
            tree_content (str): The string content of the tree structure
        """
        self.tree_content = tree_content
        self.structure = []
        self.root_dir = None

    def parse(self):
        """
        Parse the tree content into a list of paths.

        Returns:
            tuple: (root_dir, list_of_paths_and_types)
        """
        lines = self.tree_content.strip().split('\n')

        # Initialize data structures
        if not lines:
            raise ValueError("Empty tree structure")

        # Extract root directory
        root_match = re.match(r"^(?:[\s│├└]*)*(?:[├└─]*\s)*(?:\s*\/*\s*)"
                              r"(.*?[^\s])(?:\s*\/*\s*)(?:#\s*.*)?$", lines[0])
        if not root_match:
            raise ValueError(
                "Invalid tree structure format: root directory not found")

        self.root_dir = re.sub(r"[\/\"\\*?<>|:]",
                               "", root_match.group(1)).strip()
        current_path = Path(
            self.root_dir) if self.root_dir != "" else Path(".")
        # Store (path, is_directory) pairs
        self.structure = [(current_path, True)]  # Root is always a directory

        # Process the remaining lines to build the structure
        path_stack = [current_path]
        indent_stack = [0]

        for line in lines[1:]:
            # Skip empty lines
            if not line.strip():
                continue

            # Calculate the indent level
            indent_match = re.match(
                r'^([\s│├└]*)([├└]─+\s*)([^\s].*?[^\s])(?:\s*)(?:#\s*.*)?$',
                line)
            if not indent_match:
                continue

            prefix, connector, item = indent_match.groups()
            # Each level is 4 characters (either "│   " or "    ")
            indent_level = len(prefix) // 4

            # Determine if it's a directory based on trailing slash
            is_dir = item.endswith('/')
            item_name = re.sub(r"[\/\"\\*?<>|:]", "", item).strip()

            # Adjust the stack based on indent level
            while len(indent_stack) > indent_level + 1:
                path_stack.pop()
                indent_stack.pop()

            # Create the new path
            new_path = path_stack[-1] / item_name
            self.structure.append((new_path, is_dir))

            # If it's a directory, add it to the stack for potential children
            if is_dir:
                path_stack.append(new_path)
                indent_stack.append(indent_level + 1)

        return self.root_dir, self.structure
