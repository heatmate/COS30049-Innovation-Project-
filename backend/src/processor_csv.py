import pandas as pd
import os
from .features import clean_code, extract_features
import re

# Group vulnerability types categorically SAME AS OTHER FILE
def categorize_vulnerability(vuln_type):
    if not isinstance(vuln_type, str) or pd.isna(vuln_type):
        return 'Other'
    vuln_lower = vuln_type.lower()
    if any(term in vuln_lower for term in ['sql', 'injection', 'command']):
        return 'Injection'
    elif any(term in vuln_lower for term in ['xss', 'cross-site']):
        return 'XSS'
    elif any(term in vuln_lower for term in ['auth', 'session', 'token']):
        return 'Authentication'
    elif any(term in vuln_lower for term in ['file', 'upload', 'path']):
        return 'File_Handling'
    elif any(term in vuln_lower for term in ['config', 'cord', 'header']):
        return 'Configuration'
    else:
        return 'Other'

class CSVProcessor:
    def __init__(self, csv_path, output_path=None, chunksize=None):
        self.csv_path = csv_path
        self.output_path = output_path
        self.chunksize = chunksize
        self.df = None

    def process_frame(self, df_chunk):
        expected_cols = ['vulnerability_type', 'vulnerable_code', 'fixed_code']
        for c in expected_cols:
            if c not in df_chunk.columns:
                raise ValueError(f"Expected column not in CSV: {c}")

        # Build vulnerable and fixed sets
        vul_df = df_chunk[['vulnerability_type', 'vulnerable_code']].copy()
        vul_df = vul_df.rename(columns={'vulnerable_code': 'code_snippet'})
        vul_df['vul'] = 1

        fix_df = df_chunk[['vulnerability_type', 'fixed_code']].copy()
        fix_df = fix_df.rename(columns={'fixed_code': 'code_snippet'})
        fix_df['vul'] = 0

        combined = pd.concat([vul_df, fix_df], ignore_index=True)

        # Drop rows with ANY missing code
        before = len(combined)
        combined = combined.dropna(subset=['code_snippet'])
        dropped = before - len(combined)
        if dropped > 0:
            print(f"Dropped {dropped} rows with missing code")

        # Clean and extract all the features
        combined['clean_code'] = combined['code_snippet'].apply(clean_code)
        feats = combined['code_snippet'].apply(extract_features)
        feats_df = pd.DataFrame(feats.tolist(), index=combined.index)
        combined = pd.concat([combined, feats_df], axis=1)

        # Same as JSON pocessor lol 
        combined['vuln_category'] = combined['vulnerability_type'].apply(categorize_vulnerability)
        return combined

    def run(self):
        if self.chunksize:
            first = True
            out_path = self.output_path
            if out_path:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)

            for chunk in pd.read_csv(self.csv_path, chunksize=self.chunksize):
                processed = self.process_frame(chunk)

                if out_path:
                    if first:
                        processed.to_csv(out_path, index=False, mode='w')
                        first = False
                    else:
                        processed.to_csv(out_path, index=False, header=False, mode='a')
                else:
                    if self.df is None:
                        self.df = processed
                    else:
                        self.df = pd.concat([self.df, processed], ignore_index=True)

                print(f"Processed chunk, rows -> {len(processed)}")

            if out_path:
                print(f"Saved processed CSV to {out_path}")
                self.df = pd.read_csv(out_path)

        else:
            df = pd.read_csv(self.csv_path)
            self.df = self.process_frame(df)
            if self.output_path:
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                self.df.to_csv(self.output_path, index=False)
                print(f"Saved processed CSV to {self.output_path}")

        return self.df
