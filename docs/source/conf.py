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
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
]

autodoc_default_options = {
    'members': True,            # include class/method members
    'undoc-members': True,      # include members without docstrings
    'inherited-members': True,
    'show-inheritance': True,
    'exclude-members': '__dict__,__weakref__',  # skip huge defaults
}

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []
language = 'en'

add_module_names = False
autodoc_typehints = "description"
python_use_unqualified_type_names = True

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# -- Path setup --------------------------------------------------------------
import os, sys
sys.path.insert(0, os.path.abspath("../../src"))
