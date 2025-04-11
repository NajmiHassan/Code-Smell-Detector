import ast
import os
import hashlib

def detect_long_functions(tree, max_lines=50):
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, 'body') and len(node.body) > max_lines:
                smells.append(f"Function '{node.name}' is too long ({len(node.body)} lines) at line {node.lineno}")
    return smells

def detect_many_parameters(tree, max_params=5):
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > max_params:
                smells.append(f"Function '{node.name}' has too many parameters ({len(node.args.args)}) at line {node.lineno}")
    return smells

def hash_block(lines):
    block = "\n".join(lines).strip()
    return hashlib.md5(block.encode()).hexdigest()

def detect_duplicate_blocks(filepath, block_size=5):
    with open(filepath, 'r') as f:
        code_lines = [line.rstrip() for line in f if line.strip()]
    
    hashes = {}
    duplicates = []
    for i in range(len(code_lines) - block_size + 1):
        block = code_lines[i:i + block_size]
        block_hash = hash_block(block)

        if block_hash in hashes:
            duplicates.append(f"Duplicate code block between lines {hashes[block_hash]+1} and {i+1}")
        else:
            hashes[block_hash] = i
    return duplicates

def analyze_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    smells = []

    smells += detect_long_functions(tree)
    smells += detect_many_parameters(tree)
    smells += detect_duplicate_blocks(filepath)

    return smells

# For local CLI testing
if __name__ == "__main__":
    file = "example.py"
    results = analyze_file(file)
    print(f"Smells found in {file}:")
    for r in results:
        print(f" - {r}")
