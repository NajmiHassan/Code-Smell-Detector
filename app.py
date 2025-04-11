import streamlit as st
import ast
import hashlib
from io import StringIO

st.title("🐍 Code Smell Detector")
st.write("Upload a Python file to detect basic code smells like long functions, too many parameters, and duplicate code blocks.")

# Upload section
uploaded_file = st.file_uploader("Choose a Python file", type=["py"])

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language="python")

    st.subheader("⚙️ Duplicate Detection Settings")
    block_size = st.slider("Block size for duplicate detection (lines)", min_value=2, max_value=10, value=3)

    # ---------- Code Smell Detector Class ----------
    class CodeSmellDetector(ast.NodeVisitor):
        def __init__(self):
            self.smells = []

        def visit_FunctionDef(self, node):
            start_line = node.lineno
            end_line = node.body[-1].lineno
            length = end_line - start_line + 1

            if length > 10:
                self.smells.append(
                    f"🔴 Long function '{node.name}' ({length} lines) at line {start_line}"
                )

            if len(node.args.args) > 5:
                self.smells.append(
                    f"🟠 Function '{node.name}' has too many parameters ({len(node.args.args)}) at line {start_line}"
                )

            self.generic_visit(node)

    # ---------- Duplicate Code Block Detector ----------
    def find_duplicate_blocks(source_code, block_size):
        lines = [line.strip() for line in source_code.splitlines()]
        hashes = {}
        duplicates = []

        for i in range(len(lines) - block_size + 1):
            block = "\n".join(lines[i:i+block_size])
            h = hashlib.md5(block.encode()).hexdigest()

            if h in hashes:
                duplicates.append((i + 1, hashes[h] + 1, block))
            else:
                hashes[h] = i

        return duplicates

    # ---------- Run Analyzers ----------
    tree = ast.parse(code)
    detector = CodeSmellDetector()
    detector.visit(tree)

    duplicate_blocks = find_duplicate_blocks(code, block_size)

    # ---------- Results ----------
    st.subheader("🚨 Code Smells Detected:")
    if detector.smells:
        for smell in detector.smells:
            st.write(smell)
    else:
        st.success("✅ No function-level code smells detected!")

    st.subheader("📦 Duplicate Code Blocks:")
    if duplicate_blocks:
        for dup in duplicate_blocks:
            st.error(f"🔁 Duplicate block found at lines {dup[0]} and {dup[1]}")
            with st.expander("Show Duplicate Block"):
                st.code(dup[2])
    else:
        st.success("✅ No duplicate blocks detected!")
