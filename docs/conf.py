# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# Install the following dependencies: sphinxcontrib-restbuilder, sphinx-autodoc-typehints, myst-parser, sphinx-rtd-theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'metagrapho-tropy'
copyright = '2023, Maximilian Hindermann (rise@unibas.ch)'
author = 'Maximilian Hindermann (rise@unibas.ch)'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinxcontrib.restbuilder',  # sphinxcontrib-restbuilder
              'sphinx_autodoc_typehints',  # sphinx-autodoc-typehints
              'myst_parser',  # myst-parser
              'sphinx.ext.githubpages']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # sphinx-rtd-theme
html_static_path = ['_static']
