# 🔧 Template CSS Fix Guide

## Problem
All templates extending `base.html` are showing raw CSS as text because the `{% block extra_css %}` content needs to be wrapped in `<style>` tags.

## Solution Pattern

### ❌ WRONG (Current - Shows CSS as text):
```django
{% block extra_css %}
.my-class {
    color: red;
}
{% endblock %}
```

### ✅ CORRECT (Fixed - CSS renders properly):
```django
{% block extra_css %}
<style>
.my-class {
    color: red;
}
</style>
{% endblock %}
```

## Files That Need Fixing

Run this command to fix all templates at once:

```bash
cd "/home/ravi/latest project repo/RESREACH_PROJECTS/AL_ML_TECH_DASHBOARD/templates/core"

# For each template file, wrap CSS block content in <style> tags
```

## Quick Fix for Each File

### 1. Find the line: `{% block extra_css %}`
### 2. Add `<style>` right after it
### 3. Find the line: `{% endblock %}` (for that block)
### 4. Add `</style>` right before it

## Example Files Already Fixed:
- ✅ `home.html` - Fixed
- ✅ `neural_network_lab.html` - Fixed  
- ✅ `practice_zone.html` - Fixed
- ✅ `playground.html` - Fixed (already had style tags)
- ✅ `onboarding.html` - Fixed (already had style tags)
- ✅ `ui_showcase.html` - Fixed (already had style tags)

## Files Still Need Fixing:
- ⚠️ `module_learn.html`
- ⚠️ `ai_chat.html`
- ⚠️ `rag_visualizer.html`
- ⚠️ `agent_visualizer.html`
- ⚠️ `llm_params_lab.html`
- ⚠️ `kmeans_lab.html`
- ⚠️ `decision_tree_lab.html`
- ⚠️ `attention_lab.html`
- ⚠️ `logic_gates_lab.html`
- ⚠️ `data_sorting_lab.html`
- ⚠️ `pattern_recognition_lab.html`
- ⚠️ `glossary.html`
- ⚠️ `learning_paths.html`
- ⚠️ `concept_explorer.html`

## Automated Fix Command

You can use this sed command to fix all files at once:

```bash
cd "/home/ravi/latest project repo/RESREACH_PROJECTS/AL_ML_TECH_DASHBOARD/templates/core"

# This will add <style> after {% block extra_css %} and </style> before {% endblock %}
for file in *.html; do
    if grep -q "{% block extra_css %}" "$file"; then
        # Check if it doesn't already have <style> tag
        if ! grep -A1 "{% block extra_css %}" "$file" | grep -q "<style>"; then
            echo "Fixing $file..."
            # Add <style> after {% block extra_css %}
            sed -i '/{% block extra_css %}/a <style>' "$file"
            # Add </style> before the first {% endblock %} after extra_css
            # This is more complex and needs manual review
        fi
    fi
done
```

## Manual Fix Steps (Recommended)

Since automated fixing can be risky, here's the manual process:

1. Open each template file
2. Find `{% block extra_css %}`
3. Add `<style>` on the next line
4. Find the matching `{% endblock %}`
5. Add `</style>` on the line before it
6. Save and test

## Testing

After fixing each file:
1. Restart Django server: `./start.sh`
2. Visit the page in browser
3. Check that:
   - No CSS text appears at top of page
   - Page styling works correctly
   - No console errors

## Root Cause

The `base.html` template has:
```django
{% block extra_css %}{% endblock %}
```

This block is NOT wrapped in `<style>` tags in the base template, so child templates MUST provide their own `<style>` tags.

## Prevention

For future templates, always use this pattern:

```django
{% extends "base.html" %}

{% block extra_css %}
<style>
/* Your CSS here */
</style>
{% endblock %}

{% block content %}
<!-- Your HTML here -->
{% endblock %}
```

---

**Status**: 6/20 templates fixed. 14 remaining.
