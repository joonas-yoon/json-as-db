import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(cwd, '..', '..', 'src')
src_dir = os.path.abspath(src_dir)
sys.path.insert(0, src_dir)
print('Add src/ into pythonpath:', src_dir)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'json-as-db'
copyright = '2022, Joonas'
author = 'Joonas'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

# The suffix(es) of source filenames.
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


def setup(app):
    app.add_css_file('override.css')
