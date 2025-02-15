from parser.project_parser import CodeParser
from train_embeddings import  embed_code

parser = CodeParser(root_dir="farmer_management/", keywords=["validation", "USA", "enrichment", "API", "farmer", "India", "France"],)
parsed_code = parser.parse_codebase()
# print("priject......", parsed_code)
embed_code(parsed_code)
