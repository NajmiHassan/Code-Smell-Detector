import streamlit as st
import ast
import hashlib
import io

st.title("🐍 Code Smell Detector")
st.write("Upload a Python file to detect basic code smells like long functions, too many parameters, and duplicate code blocks.")

# Upload section
uploaded_file = st.file_uploader("Choose a Python file", type=["py"])

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language="python")

    # Block size slider
    st.sidebar.title("🔧 Detection Settings")
    block_size = st.sidebar.slider("Block size for duplicate detection", 3, 10, value=5)

    # === AST-BASED DETECTOR ===
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

    tree = ast.parse(code)
    detector = CodeSmellDetector()
    detector.visit(tree)

    # === DUPLICATE BLOCK DETECTOR ===
    def detect_duplicate_blocks(code_string, block_size):
        lines = [line.rstrip() for line in code_string.splitlines() if line.strip()]
        hashes = {}
        duplicates = []

        for i in range(len(lines) - block_size + 1):
            block = "\n".join(lines[i:i + block_size]).strip()
            block_hash = hashlib.md5(block.encode()).hexdigest()

            if block_hash in hashes:
                original = hashes[block_hash]
                duplicates.append(
                    f"🟡 Duplicate code block detected between lines {original + 1} and {i + 1}"
                )
            else:
                hashes[block_hash] = i

        return duplicates

    duplicate_smells = detect_duplicate_blocks(code, block_size)

    # === COMBINE AND DISPLAY RESULTS ===
    st.subheader("🚨 Code Smells Detected:")

    all_smells = detector.smells + duplicate_smells

    if all_smells:
        for smell in all_smells:
            st.write(smell)
    else:
        st.success("✅ No code smells detected!")

    # === DOWNLOAD REPORT ===
    report_text = "\n".join(all_smells) if all_smells else "No code smells detected."
    report_bytes = io.BytesIO(report_text.encode("utf-8"))

    st.download_button(
        label="📄 Download Report",
        data=report_bytes,
        file_name="code_smell_report.txt",
        mime="text/plain"
    )
