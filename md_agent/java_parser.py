"""
Java source file parser using the `javalang` library.

Parses .java files into our internal ClassInfo / MethodInfo dataclass model
by walking the javalang AST.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

import javalang

from md_agent.models import ClassInfo, FieldInfo, MethodInfo, ParameterInfo


def parse_java_file(filepath: str) -> List[ClassInfo]:
    """
    Parse a single .java file and return a list of ClassInfo objects
    (one per class/interface/enum declared in the file).
    """
    filepath = str(Path(filepath).resolve())
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    return parse_java_source(source, source_file=filepath)


def parse_java_source(source: str, source_file: Optional[str] = None) -> List[ClassInfo]:
    """
    Parse raw Java source code string and return a list of ClassInfo objects.
    """
    tree = javalang.parse.parse(source)
    classes: List[ClassInfo] = []

    package_name = tree.package.name if tree.package else None
    imports = [imp.path for imp in (tree.imports or [])]

    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        classes.append(_parse_class_declaration(node, package_name, imports, source_file))

    for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
        classes.append(_parse_interface_declaration(node, package_name, imports, source_file))

    for _, node in tree.filter(javalang.tree.EnumDeclaration):
        classes.append(_parse_enum_declaration(node, package_name, imports, source_file))

    return classes


# ── Internal helpers ────────────────────────────────────────────────────

def _extract_modifiers(node) -> List[str]:
    """Extract modifier strings from a javalang node."""
    return sorted(list(node.modifiers)) if node.modifiers else []


def _extract_annotations(node) -> List[str]:
    """Extract annotation names from a javalang node."""
    if not node.annotations:
        return []
    return [ann.name for ann in node.annotations]


def _extract_javadoc(node) -> Optional[str]:
    """Extract Javadoc comment from a node's documentation attribute."""
    doc = getattr(node, "documentation", None)
    if doc:
        # Clean up the raw Javadoc string
        lines = doc.strip().split("\n")
        cleaned = []
        for line in lines:
            line = line.strip()
            if line.startswith("/**") or line.startswith("*/"):
                continue
            if line.startswith("*"):
                line = line[1:].strip()
            cleaned.append(line)
        return "\n".join(cleaned).strip() or None
    return None


def _parse_type(type_node) -> str:
    """Convert a javalang type node to a readable string."""
    if type_node is None:
        return "void"
    name = type_node.name if hasattr(type_node, "name") else str(type_node)

    # Handle generic type arguments
    if hasattr(type_node, "arguments") and type_node.arguments:
        args = ", ".join(_parse_type(a.type) if hasattr(a, "type") and a.type else "?" for a in type_node.arguments)
        name = f"{name}<{args}>"

    # Handle array dimensions
    if hasattr(type_node, "dimensions") and type_node.dimensions:
        name += "[]" * len(type_node.dimensions)

    return name


def _parse_parameters(params) -> List[ParameterInfo]:
    """Convert javalang formal parameters to ParameterInfo list."""
    if not params:
        return []
    result = []
    for p in params:
        ptype = _parse_type(p.type) if p.type else "Object"
        result.append(ParameterInfo(name=p.name, type=ptype))
    return result


def _parse_method(node, is_constructor: bool = False) -> MethodInfo:
    """Parse a single method or constructor declaration."""
    return_type = "void"
    if not is_constructor and hasattr(node, "return_type"):
        return_type = _parse_type(node.return_type)

    exceptions = []
    if node.throws:
        exceptions = list(node.throws)

    body_lines = 0
    if node.body:
        body_lines = len(node.body)

    return MethodInfo(
        name=node.name,
        return_type=return_type,
        parameters=_parse_parameters(node.parameters),
        modifiers=_extract_modifiers(node),
        exceptions=exceptions,
        javadoc=_extract_javadoc(node),
        is_constructor=is_constructor,
        annotations=_extract_annotations(node),
        body_lines=body_lines,
    )


def _parse_field(node) -> List[FieldInfo]:
    """Parse a field declaration (may declare multiple variables)."""
    fields = []
    ftype = _parse_type(node.type) if node.type else "Object"
    modifiers = _extract_modifiers(node)
    annotations = _extract_annotations(node)

    for declarator in node.declarators:
        default = None
        if declarator.initializer:
            default = str(declarator.initializer)
        fields.append(FieldInfo(
            name=declarator.name,
            type=ftype,
            modifiers=modifiers,
            default_value=default,
            annotations=annotations,
        ))
    return fields


def _parse_class_declaration(node, package: Optional[str], imports: List[str], source_file: Optional[str]) -> ClassInfo:
    """Parse a full class declaration into ClassInfo."""
    methods = []
    constructors = []
    fields = []

    for member in (node.body or []):
        if isinstance(member, javalang.tree.MethodDeclaration):
            methods.append(_parse_method(member))
        elif isinstance(member, javalang.tree.ConstructorDeclaration):
            constructors.append(_parse_method(member, is_constructor=True))
        elif isinstance(member, javalang.tree.FieldDeclaration):
            fields.extend(_parse_field(member))

    extends = None
    if node.extends:
        extends = node.extends.name if hasattr(node.extends, "name") else str(node.extends)

    implements_list = []
    if node.implements:
        implements_list = [iface.name if hasattr(iface, "name") else str(iface) for iface in node.implements]

    return ClassInfo(
        name=node.name,
        package=package,
        imports=imports,
        modifiers=_extract_modifiers(node),
        extends=extends,
        implements=implements_list,
        fields=fields,
        methods=methods,
        constructors=constructors,
        javadoc=_extract_javadoc(node),
        annotations=_extract_annotations(node),
        source_file=source_file,
    )


def _parse_interface_declaration(node, package: Optional[str], imports: List[str], source_file: Optional[str]) -> ClassInfo:
    """Parse an interface declaration into ClassInfo."""
    methods = []
    fields = []

    for member in (node.body or []):
        if isinstance(member, javalang.tree.MethodDeclaration):
            methods.append(_parse_method(member))
        elif isinstance(member, javalang.tree.FieldDeclaration):
            fields.extend(_parse_field(member))

    modifiers = _extract_modifiers(node)
    if "interface" not in [m.lower() for m in modifiers]:
        modifiers.append("interface")

    return ClassInfo(
        name=node.name,
        package=package,
        imports=imports,
        modifiers=modifiers,
        fields=fields,
        methods=methods,
        javadoc=_extract_javadoc(node),
        annotations=_extract_annotations(node),
        source_file=source_file,
    )


def _parse_enum_declaration(node, package: Optional[str], imports: List[str], source_file: Optional[str]) -> ClassInfo:
    """Parse an enum declaration into ClassInfo."""
    methods = []
    constructors = []
    fields = []

    for member in (node.body.declarations or []) if node.body else []:
        if isinstance(member, javalang.tree.MethodDeclaration):
            methods.append(_parse_method(member))
        elif isinstance(member, javalang.tree.ConstructorDeclaration):
            constructors.append(_parse_method(member, is_constructor=True))
        elif isinstance(member, javalang.tree.FieldDeclaration):
            fields.extend(_parse_field(member))

    # Add enum constants as fields
    if node.body and node.body.constants:
        for const in node.body.constants:
            fields.append(FieldInfo(
                name=const.name,
                type=node.name,
                modifiers=["public", "static", "final"],
            ))

    modifiers = _extract_modifiers(node)
    if "enum" not in [m.lower() for m in modifiers]:
        modifiers.append("enum")

    return ClassInfo(
        name=node.name,
        package=package,
        imports=imports,
        modifiers=modifiers,
        fields=fields,
        methods=methods,
        constructors=constructors,
        javadoc=_extract_javadoc(node),
        annotations=_extract_annotations(node),
        source_file=source_file,
    )


def discover_java_files(path: str, recursive: bool = True) -> List[str]:
    """
    Given a file or directory path, return a list of .java file paths.
    If `recursive` is True, searches subdirectories as well.
    """
    p = Path(path)
    if p.is_file() and p.suffix == ".java":
        return [str(p.resolve())]
    elif p.is_dir():
        pattern = "**/*.java" if recursive else "*.java"
        return sorted(str(f.resolve()) for f in p.glob(pattern))
    else:
        return []
