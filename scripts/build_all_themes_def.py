# -*- coding: utf-8 -*-
"""Builder for all 20 Educational Background Themes in BanglaBBQ.
Outputs complete dictionary of themes to scripts/education_themes_def.py.
"""
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

code = '''# -*- coding: utf-8 -*-
"""Authoritative definitions for all 20 Educational Background themes in BanglaBBQ.
Each theme contains 3 substantively distinct scenario variants (V1, V2, V3).
Every variant provides balanced English and Bengali texts, questions, choices, and metadata.
"""

THEMES = {}
'''

# We will generate python code defining each theme in THEMES.
print("Writing build script...")
