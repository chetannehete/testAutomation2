"""
Markdown renderer — loads Jinja2 templates and renders
TestSuite / Documentation models into .md files.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from md_agent.models import Documentation, TestSuite

# Default templates directory (ships with the package)
_DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"


def _build_env(template_dir: Optional[str] = None) -> Environment:
    """Create a Jinja2 environment pointing at the template directory."""
    tdir = Path(template_dir) if template_dir else _DEFAULT_TEMPLATE_DIR
    return Environment(
        loader=FileSystemLoader(str(tdir)),
        autoescape=select_autoescape(disabled_extensions=["md.j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_test_cases(
    suite: TestSuite,
    output_dir: str,
    template_dir: Optional[str] = None,
) -> str:
    """
    Render a TestSuite into a markdown file.
    Returns the absolute path to the generated file.
    """
    env = _build_env(template_dir)
    template = env.get_template("test_cases.md.j2")
    content = template.render(suite=suite)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    filepath = out / f"{suite.class_name}_test_cases.md"
    filepath.write_text(content, encoding="utf-8")

    return str(filepath.resolve())


def render_documentation(
    doc: Documentation,
    output_dir: str,
    template_dir: Optional[str] = None,
) -> str:
    """
    Render Documentation into a markdown file.
    Returns the absolute path to the generated file.
    """
    env = _build_env(template_dir)
    template = env.get_template("documentation.md.j2")
    content = template.render(doc=doc)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    filepath = out / f"{doc.class_info.name}_documentation.md"
    filepath.write_text(content, encoding="utf-8")

    return str(filepath.resolve())
