import os
import sys

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
]
autodoc_default_options = {
    'member-order': 'bysource',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'basic'
html_static_path = ['_static']
html_search_scorer = '_static/scorer.js'
html_js_files = [
  'custom.js',
  'settings.js',
  'copy.js',
  'sidebar.js'
]
html_experimental_html5_writer = True
