"""
Analyzer module — derives test cases and documentation sections
from the parsed Java code model using rule-based heuristics.

Each rule inspects method signatures, parameters, return types,
exceptions, and annotations to produce actionable test cases
and structured documentation sections.
"""

from __future__ import annotations

from typing import List

from md_agent.models import (
    ClassInfo,
    DocSection,
    Documentation,
    MethodInfo,
    TestCase,
    TestSuite,
)


# ── Numeric / nullable type sets ────────────────────────────────────────

_NUMERIC_TYPES = {"int", "long", "short", "byte", "float", "double",
                  "Integer", "Long", "Short", "Byte", "Float", "Double",
                  "BigDecimal", "BigInteger"}

_NULLABLE_TYPES = {"String", "Integer", "Long", "Short", "Byte", "Float",
                   "Double", "Boolean", "Object", "List", "Map", "Set",
                   "Collection", "BigDecimal", "BigInteger"}

_COLLECTION_TYPES = {"List", "Set", "Map", "Collection", "ArrayList",
                     "LinkedList", "HashMap", "TreeMap", "HashSet", "TreeSet"}


# ═══════════════════════════════════════════════════════════════════════
#  TEST CASE GENERATION
# ═══════════════════════════════════════════════════════════════════════

def generate_test_suite(class_info: ClassInfo) -> TestSuite:
    """Generate a full TestSuite for one ClassInfo."""
    suite = TestSuite(
        class_name=class_info.name,
        package=class_info.package,
        source_file=class_info.source_file,
    )

    tc_counter = 0
    for method in class_info.methods:
        if _is_private(method):
            continue
        cases = _generate_method_test_cases(method, class_info)
        for c in cases:
            tc_counter += 1
            c.id = f"TC-{tc_counter:03d}"
        suite.test_cases.extend(cases)

    for ctor in class_info.constructors:
        cases = _generate_method_test_cases(ctor, class_info)
        for c in cases:
            tc_counter += 1
            c.id = f"TC-{tc_counter:03d}"
        suite.test_cases.extend(cases)

    return suite


def _is_private(method: MethodInfo) -> bool:
    return "private" in method.modifiers


def _generate_method_test_cases(method: MethodInfo, cls: ClassInfo) -> List[TestCase]:
    """Apply all heuristic rules to one method and return test cases."""
    cases: List[TestCase] = []

    # ── Rule 1: Happy-path for every testable method ─────────────────
    param_str = ", ".join(f"{p.type} {p.name}" for p in method.parameters)
    call_example = f"{method.name}({', '.join(_example_value(p.type) for p in method.parameters)})"

    if method.is_constructor:
        call_example = f"new {method.name}({', '.join(_example_value(p.type) for p in method.parameters)})"

    expected = "Object is created successfully" if method.is_constructor else (
        f"Returns expected {method.return_type} value" if method.return_type != "void"
        else "Method executes without error"
    )

    cases.append(TestCase(
        id="",
        method_name=f"{method.name}({param_str})",
        category="Happy Path",
        description=f"Verify {method.name} works with valid inputs",
        preconditions=_preconditions(method, cls),
        steps=f"Call `{call_example}`",
        expected_result=expected,
    ))

    # ── Rule 2: Null-input edge cases for nullable params ────────────
    for p in method.parameters:
        base_type = p.type.split("<")[0].split("[")[0]
        if base_type in _NULLABLE_TYPES:
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Edge Case",
                description=f"Pass null for parameter `{p.name}` ({p.type})",
                preconditions=_preconditions(method, cls),
                steps=f"Call `{method.name}(...)` with `{p.name} = null`",
                expected_result="Throws NullPointerException or handles gracefully",
            ))

    # ── Rule 3: Boundary values for numeric params ───────────────────
    for p in method.parameters:
        base_type = p.type.split("<")[0].split("[")[0]
        if base_type in _NUMERIC_TYPES:
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Boundary",
                description=f"Pass zero for numeric parameter `{p.name}`",
                preconditions=_preconditions(method, cls),
                steps=f"Call `{method.name}(...)` with `{p.name} = 0`",
                expected_result="Returns correct boundary result",
            ))
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Boundary",
                description=f"Pass negative value for `{p.name}`",
                preconditions=_preconditions(method, cls),
                steps=f"Call `{method.name}(...)` with `{p.name} = -1`",
                expected_result="Returns correct result or rejects negative input",
            ))
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Boundary",
                description=f"Pass MAX value for `{p.name}` ({base_type})",
                preconditions=_preconditions(method, cls),
                steps=f"Call `{method.name}(...)` with `{p.name} = {base_type}.MAX_VALUE`",
                expected_result="Handles overflow / large value correctly",
            ))

    # ── Rule 4: Exception test cases ─────────────────────────────────
    for exc in method.exceptions:
        cases.append(TestCase(
            id="",
            method_name=f"{method.name}({param_str})",
            category="Exception",
            description=f"Trigger {exc} from `{method.name}`",
            preconditions=_preconditions(method, cls),
            steps=f"Call `{method.name}(...)` with inputs that cause `{exc}`",
            expected_result=f"`{exc}` is thrown with a meaningful message",
        ))

    # ── Rule 5: Boolean return — true and false cases ────────────────
    if method.return_type == "boolean" or method.return_type == "Boolean":
        cases.append(TestCase(
            id="",
            method_name=f"{method.name}({param_str})",
            category="Happy Path",
            description=f"Verify `{method.name}` returns true",
            preconditions=_preconditions(method, cls),
            steps=f"Call `{method.name}(...)` with inputs expected to yield `true`",
            expected_result="Returns `true`",
        ))
        cases.append(TestCase(
            id="",
            method_name=f"{method.name}({param_str})",
            category="Happy Path",
            description=f"Verify `{method.name}` returns false",
            preconditions=_preconditions(method, cls),
            steps=f"Call `{method.name}(...)` with inputs expected to yield `false`",
            expected_result="Returns `false`",
        ))

    # ── Rule 6: Void method — state mutation check ───────────────────
    if method.return_type == "void" and not method.is_constructor:
        cases.append(TestCase(
            id="",
            method_name=f"{method.name}({param_str})",
            category="Happy Path",
            description=f"Verify state change after calling `{method.name}`",
            preconditions=_preconditions(method, cls),
            steps=f"Call `{method.name}(...)` and inspect object state",
            expected_result="Object state is updated as expected",
        ))

    # ── Rule 7: Collection params — empty collection edge case ───────
    for p in method.parameters:
        base_type = p.type.split("<")[0].split("[")[0]
        if base_type in _COLLECTION_TYPES or p.type.endswith("[]"):
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Edge Case",
                description=f"Pass empty collection/array for `{p.name}`",
                preconditions=_preconditions(method, cls),
                steps=f"Call `{method.name}(...)` with `{p.name}` as empty",
                expected_result="Handles empty input gracefully",
            ))

    # ── Rule 8: String params — empty string edge case ───────────────
    for p in method.parameters:
        if p.type == "String":
            cases.append(TestCase(
                id="",
                method_name=f"{method.name}({param_str})",
                category="Edge Case",
                description=f"Pass empty string for `{p.name}`",
                preconditions=_preconditions(method, cls),
                steps=f'Call `{method.name}(...)` with `{p.name} = ""`',
                expected_result="Handles empty string gracefully",
            ))

    return cases


def _preconditions(method: MethodInfo, cls: ClassInfo) -> str:
    """Build a preconditions string."""
    parts = []
    if not method.is_constructor and "static" not in method.modifiers:
        parts.append(f"`{cls.name}` instance is created")
    if method.is_constructor:
        return "None"
    return ", ".join(parts) if parts else "None"


def _example_value(type_str: str) -> str:
    """Return a representative example literal for a given Java type."""
    base = type_str.split("<")[0].split("[")[0]
    examples = {
        "int": "1", "long": "1L", "short": "(short) 1", "byte": "(byte) 1",
        "float": "1.0f", "double": "1.0", "boolean": "true", "char": "'a'",
        "String": '"hello"', "Integer": "1", "Long": "1L",
        "Boolean": "true", "Double": "1.0",
    }
    return examples.get(base, f"mock{base}")


# ═══════════════════════════════════════════════════════════════════════
#  DOCUMENTATION GENERATION
# ═══════════════════════════════════════════════════════════════════════

def generate_documentation(class_info: ClassInfo) -> Documentation:
    """Generate structured Documentation for one ClassInfo."""
    doc = Documentation(class_info=class_info)

    # ── Class overview section ───────────────────────────────────────
    overview_lines = []
    if class_info.javadoc:
        overview_lines.append(class_info.javadoc)
    else:
        overview_lines.append(f"{class_info.name} class.")

    if class_info.extends:
        overview_lines.append(f"\nExtends `{class_info.extends}`.")
    if class_info.implements:
        overview_lines.append(f"\nImplements {', '.join(f'`{i}`' for i in class_info.implements)}.")

    doc.sections.append(DocSection(
        title="Class Overview",
        content="\n".join(overview_lines),
        level=2,
    ))

    # ── Fields section ───────────────────────────────────────────────
    if class_info.fields:
        rows = []
        rows.append("| Modifier | Type | Name | Default |")
        rows.append("|----------|------|------|---------|")
        for f in class_info.fields:
            mods = " ".join(f.modifiers) if f.modifiers else "-"
            default = f"`{f.default_value}`" if f.default_value else "-"
            rows.append(f"| `{mods}` | `{f.type}` | `{f.name}` | {default} |")
        doc.sections.append(DocSection(title="Fields", content="\n".join(rows), level=2))

    # ── Constructors section ─────────────────────────────────────────
    if class_info.constructors:
        for ctor in class_info.constructors:
            doc.sections.append(_method_doc_section(ctor, class_info, heading_level=3))

    # ── Methods section ──────────────────────────────────────────────
    for method in class_info.methods:
        doc.sections.append(_method_doc_section(method, class_info, heading_level=3))

    return doc


def _method_doc_section(method: MethodInfo, cls: ClassInfo, heading_level: int = 3) -> DocSection:
    """Build a DocSection for one method/constructor."""
    param_sig = ", ".join(f"{p.type} {p.name}" for p in method.parameters)
    if method.is_constructor:
        title = f"`{method.name}({param_sig})`"
    else:
        title = f"`{method.name}({param_sig})` → `{method.return_type}`"

    lines = []

    # Javadoc description
    if method.javadoc:
        lines.append(method.javadoc)
    else:
        lines.append(f"{'Constructor' if method.is_constructor else 'Method'} `{method.name}`.")

    lines.append("")

    # Modifiers
    if method.modifiers:
        lines.append(f"**Modifiers:** `{' '.join(method.modifiers)}`")
        lines.append("")

    # Annotations
    if method.annotations:
        lines.append(f"**Annotations:** {', '.join(f'`@{a}`' for a in method.annotations)}")
        lines.append("")

    # Parameters table
    if method.parameters:
        lines.append("**Parameters:**")
        lines.append("")
        lines.append("| Name | Type | Description |")
        lines.append("|------|------|-------------|")
        for p in method.parameters:
            desc = _param_description_from_javadoc(method.javadoc, p.name) if method.javadoc else "-"
            lines.append(f"| `{p.name}` | `{p.type}` | {desc} |")
        lines.append("")

    # Return type
    if not method.is_constructor and method.return_type != "void":
        lines.append(f"**Returns:** `{method.return_type}`")
        lines.append("")

    # Exceptions
    if method.exceptions:
        lines.append("**Throws:**")
        lines.append("")
        for exc in method.exceptions:
            lines.append(f"- `{exc}`")
        lines.append("")

    return DocSection(
        title=title,
        content="\n".join(lines),
        level=heading_level,
    )


def _param_description_from_javadoc(javadoc: str, param_name: str) -> str:
    """Try to extract @param description from Javadoc text."""
    if not javadoc:
        return "-"
    for line in javadoc.split("\n"):
        stripped = line.strip()
        if stripped.startswith(f"@param {param_name}"):
            desc = stripped[len(f"@param {param_name}"):].strip()
            return desc if desc else "-"
    return "-"
