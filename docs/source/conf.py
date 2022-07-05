# Configuration file for the Sphinx documentation builder.
import sys
import os
import mock

sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information

project = 'tspop'
copyright = '2022, Georgia Tsambos'
author = 'Georgia Tsambos'

release = '0.1'
version = '0.0.1'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# Master ("home") document
master_doc = 'index'

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Directory to look for API
# autoapi_dirs = ['../../src']
# autodoc_mock_imports = ["msprime", "pandas", "numpy", "numpy.core.multiarray"]
# autodoc_default_options = {"private-members": False}