import ast
import os


class CodeParser:
    """
    Parses Python code to extract classes, functions, and their dependencies along with code snippets and keywords.
    """

    def __init__(self, root_dir, keywords=None):
        """
        Initializes the CodeParser.

        Args:
            root_dir (str): Root directory of the codebase.
            keywords (list): List of keywords to search for in code, comments, and docstrings.
        """
        self.root_dir = root_dir
        self.context = []
        self.keywords = (
            keywords or []
        ) 

    def parse_file(self, file_path):
        """Parses a Python file to extract classes, functions, and code."""
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_data = {
                        "type": "class",
                        "name": node.name,
                        "file": file_path,
                        "docstring": ast.get_docstring(node),
                        "methods": [],
                        "keywords": self._extract_keywords(
                            node, file_path
                        ), 
                    }
                    for func in node.body:
                        if isinstance(func, ast.FunctionDef):
                            class_data["methods"].append(
                                {
                                    "name": func.name,
                                    "docstring": ast.get_docstring(func),
                                    "code": self._get_function_code(func, file_path),
                                    "keywords": self._extract_keywords(func, file_path),
                                }
                            )
                    self.context.append(class_data)
                elif isinstance(node, ast.FunctionDef):
                    self.context.append(
                        {
                            "type": "function",
                            "name": node.name,
                            "file": file_path,
                            "docstring": ast.get_docstring(node),
                            "code": self._get_function_code(node, file_path),
                            "calls": self._extract_function_calls(node),
                            "keywords": self._extract_keywords(node, file_path),
                        }
                    )

    def _get_function_code(self, node, file_path):
        """
        Extracts the code of a function from the source file.

        Args:
            node (ast.FunctionDef): The function node to analyze.
            file_path (str): Path to the Python file.

        Returns:
            str: The code of the function.
        """
        
        with open(file_path, "r") as f:
            lines = f.readlines()

        start_line = node.lineno - 1
        end_line = node.end_lineno
        if file_path == 'farmer_management/app/validation_service.py':
            print(start_line, '..... ', end_line)
  
        return "".join(lines[start_line:end_line])

    def _extract_function_calls(self, node):
        """
        Extracts function calls from a function node.

        Args:
            node (ast.FunctionDef): The function node to analyze.

        Returns:
            list: A list of function names being called.
        """
        calls = []
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Call):
                if isinstance(subnode.func, ast.Name):
                    calls.append(subnode.func.id)
                elif isinstance(subnode.func, ast.Attribute):
                    calls.append(subnode.func.attr)
        return calls

    def _extract_keywords(self, node, file_path):
        """
        Extracts keywords from the node's code, comments, and docstrings.

        Args:
            node (ast.AST): The node to analyze.
            file_path (str): Path to the Python file.

        Returns:
            list: A list of matched keywords.
        """
        matched_keywords = []


        docstring = ast.get_docstring(node) or ""

        with open(file_path, "r") as f:
            lines = f.readlines()
        comments = [
            line.strip()
            for line in lines[node.lineno - 1 : node.end_lineno or node.lineno]
            if line.strip().startswith("#")
        ]

        content_to_search = (
            docstring + " " + " ".join(comments) + " " + ast.unparse(node)
        )

        # Match keywords
        for keyword in self.keywords:
            if keyword.lower() in content_to_search.lower():
                matched_keywords.append(keyword)

        return matched_keywords

    def parse_codebase(self):
        """Traverses the codebase and parses all Python files."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    self.parse_file(os.path.join(root, file))
        return self.context
