# -- Project information -----------------------------------------------------
project = 'gmdkit'
copyright = '2025, HDanke'
author = 'HDanke'

try:
    from setuptools_scm import get_version
    release = get_version(root='../..', relative_to=__file__)
except Exception:
    release = '0.0.0'
version = release

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",      # pull in docstrings
    "sphinx.ext.napoleon",     # Google/Numpy style docstrings
    "sphinx.ext.viewcode",     # links to highlighted source
    "sphinx.ext.autosummary",  # generates API index
]

autosummary_generate = True   # auto-generate .rst files from docstrings

templates_path = ['_templates']
exclude_patterns = []
language = 'en'

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# -- Path setup --------------------------------------------------------------
import os, sys
sys.path.insert(0, os.path.abspath("../../src"))
