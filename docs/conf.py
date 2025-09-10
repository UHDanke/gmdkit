import sys
import os

# Add your src folder to sys.path so Sphinx can import your package
sys.path.insert(0, os.path.abspath('../src'))

# Try to get version from installed package first
try:
    from importlib.metadata import version as pkg_version
except ImportError:
    from importlib_metadata import version as pkg_version

try:
    release = pkg_version("gmdkit")  # setuptools-scm will fill this
except Exception:
    # fallback if package not installed
    from setuptools_scm import get_version
    release = get_version(root='..', relative_to=__file__)

version = release  # short version string if needed
