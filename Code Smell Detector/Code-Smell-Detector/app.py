import streamlit as st
import ast
import hashlib
from io import StringIO
import base64
import datetime

st.set_page_config(layout="wide")
st.title("🐍 Code Smell Detector")
st.write("Upload a Python file to detect basic code smells like long functions, too many parameters, and duplicate code blocks.")

# Move settings to sidebar
with st.sidebar:
    st.header("Settings")
    
    st.subheader("⚙️ Duplicate Detection Settings")
    block_size = st.slider("Block size for duplicate detection (lines)", 
                         min_value=2, max_value=10, value=3)
    
    function_length_limit = st.slider("Max function length (lines)", 
                                    min_value=5, max_value=50, value=10)
    
    param_limit = st.slider("Max parameters per function", 
                          min_value=2, max_value=10, value=5)

# Upload section
uploaded_file = st.file_uploader("Choose a Python file", type=["py"])

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language="python")
    
    # ---------- Code Smell Detector Class ----------
    class CodeSmellDetector(ast.NodeVisitor):
        def __init__(self):
            self.smells = []
        
        def visit_FunctionDef(self, node):
            start_line = node.lineno
            end_line = node.body[-1].lineno
            length = end_line - start_line + 1
            
            if length > function_length_limit:
                self.smells.append(
                    f"🔴 Long function '{node.name}' ({length} lines) at line {start_line}"
                )
            
            if len(node.args.args) > param_limit:
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Code Smells Detected:")
        if detector.smells:
            for smell in detector.smells:
                st.write(smell)
        else:
            st.success("✅ No function-level code smells detected!")
    
    with col2:
        st.subheader("📦 Duplicate Code Blocks:")
        if duplicate_blocks:
            for dup in duplicate_blocks:
                st.error(f"🔁 Duplicate block found at lines {dup[0]} and {dup[1]}")
                with st.expander("Show Duplicate Block"):
                    st.code(dup[2])
        else:
            st.success("✅ No duplicate blocks detected!")
    
    # ---------- Generate Report ----------
    def generate_report():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = uploaded_file.name
        
        report = f"""# Code Smell Analysis Report
Generated: {now}
File: {filename}

## Analysis Settings
- Function length limit: {function_length_limit} lines
- Parameter limit: {param_limit}
- Duplicate block size: {block_size} lines

## Function-level Code Smells
"""
        if detector.smells:
            for smell in detector.smells:
                report += f"- {smell}\n"
        else:
            report += "No function-level code smells detected.\n"
        
        report += "\n## Duplicate Code Blocks\n"
        if duplicate_blocks:
            for idx, dup in enumerate(duplicate_blocks):
                report += f"### Duplicate Block #{idx+1}\n"
                report += f"- Found at lines {dup[0]} and {dup[1]}\n"
                report += "```python\n"
                report += dup[2] + "\n"
                report += "```\n\n"
        else:
            report += "No duplicate blocks detected.\n"
            
        return report
    
    # Add download button to sidebar
    with st.sidebar:
        st.subheader("📊 Report")
        
        if st.button("Generate Download Report"):
            report_content = generate_report()
            b64 = base64.b64encode(report_content.encode()).decode()
            filename = f"code_smell_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            href = f'<a href="data:text/markdown;base64,{b64}" download="{filename}">Download Report (Markdown)</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Report generated! Click the link above to download.")
else:
    with st.sidebar:
        st.info("Upload a Python file to see analysis options and download report.")