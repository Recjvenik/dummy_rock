#!/usr/bin/env python3
"""
Script to fix all Django templates that have {% block extra_css %} without <style> tags
"""

import os
import re

TEMPLATES_DIR = "/home/ravi/latest project repo/RESREACH_PROJECTS/AL_ML_TECH_DASHBOARD/templates/core"

def fix_template(filepath):
    """Fix a single template file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has {% block extra_css %}
    if '{% block extra_css %}' not in content:
        return False, "No extra_css block"
    
    # Check if it already has <style> tag after {% block extra_css %}
    if re.search(r'{%\s*block\s+extra_css\s*%}\s*<style>', content):
        return False, "Already has <style> tag"
    
    # Pattern to match {% block extra_css %} ... {% endblock %}
    pattern = r'({%\s*block\s+extra_css\s*%})(.*?)({%\s*endblock\s*%})'
    
    def replacer(match):
        start = match.group(1)
        css_content = match.group(2)
        end = match.group(3)
        
        # Add <style> and </style> tags
        return f"{start}\n<style>{css_content}</style>\n{end}"
    
    # Replace the pattern
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content == content:
        return False, "No changes made"
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Fixed successfully"

def main():
    """Main function to process all templates"""
    print("🔧 Fixing Django template CSS blocks...\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for filename in sorted(os.listdir(TEMPLATES_DIR)):
        if not filename.endswith('.html'):
            continue
        
        filepath = os.path.join(TEMPLATES_DIR, filename)
        success, message = fix_template(filepath)
        
        if success:
            print(f"✅ {filename}: {message}")
            fixed_count += 1
        else:
            print(f"⏭️  {filename}: {message}")
            skipped_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Fixed: {fixed_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total: {fixed_count + skipped_count}")

if __name__ == '__main__':
    main()
