import os
import re

def search_text_in_files(search_text, directory=None, file_pattern=r'.*'):
    if not directory:
        directory = os.getcwd()
    
    results = {}
    pattern = re.compile(search_text, re.IGNORECASE)
    file_matcher = re.compile(file_pattern)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if not file_matcher.match(file):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                matches = []
                for i, line in enumerate(lines, 1):
                    if pattern.search(line):
                        matches.append((i, line))
                
                if matches:
                    results[file_path] = matches
            except:
                pass
    
    return results 