import re
import pandas as pd 

# Clean and normalise code snippets for easier processing
def clean_code(code):
    if pd.isna(code):
        return ""
    # Removes all comments
    code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', str(code))
    # Removes the extra whitespace
    code = re.sub(r'\s+', ' ', code)
    # Remove the common boilerplate
    code = re.sub(r'require\([\'"][\w\-/\.]+[\'"]\)', 'require()', code)
    return code.strip()

# Different keywords when extracting from code snippets
def extract_features(code):
    if pd.isna(code):
        return {}
    code_str = str(code).lower()
    return {
        'has_user_input': any(keyword in code_str.lower() for keyword in
                                ['req.', 'input', 'param', 'query', 'body']),
        'has_db_operation': any(keyword in code_str.lower() for keyword in
                                ['query', 'exec', 'select', 'insert', 'update', 'complete']),
        'has_file_operation': any(keyword in code_str.lower() for keyword in
                                    ['readfile', 'writefile', 'open', 'fs.']),
        'has_eval': any(keyword in code_str.lower() for keyword in
                        ['exec', 'eval', 'system', 'shell']),
        'code_length': len(code_str),
        'has_validation': any(keyword in code_str.lower() for keyword in
                                ['validate', 'sanitize', 'escape', 'filter']),
        'has_quotes': "'" in code_str or '"' in code_str,
        'has_concatenation': '+' in code_str or '${' in code_str or '%s' in code_str
    }


