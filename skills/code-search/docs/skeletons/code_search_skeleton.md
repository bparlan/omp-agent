# Code-Search Codebase Skeletons
> Use this for low-token code understanding. Prefer over reading full files.

### File: skills/code-search/code_indexer.py
import json
import os
import tree_sitter_language_pack
import json
import os
import tree_sitter_language_pack
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List
def _init_python_parser():
def get_db_path() -> Path:
def get_skeleton_path() -> Path:
def extract_skeleton(filepath: Path) -> str | None:
def _extract_python_skeleton(filepath: Path) -> str | None:
def _extract_generic_skeleton(filepath: Path) -> str | None:
def generate_skeletons():
def index_project():
def search(query: str, limit: int = 10):

