"""Tests for the _detect_ready helper in reasoning_handler."""

import pytest

from crewai.utilities.reasoning_handler import _detect_ready


@pytest.mark.parametrize(
    "text,expected",
    [
        # Legacy full sentence (backward compat)
        ("READY: I am ready to execute the task.", True),
        # Bare verdicts
        ("READY", True),
        ("ready", True),
        # Markdown emphasis variants
        ("**READY**", True),
        ("*READY*", True),
        # Negated forms
        ("NOT READY", False),
        ("NOT **READY**", False),
        # Trailing NOT READY wins
        ("I need more info. NOT READY", False),
        # Last-verdict-wins: trailing NOT READY overrides earlier READY
        ("READY but then NOT READY", False),
        # Last-verdict-wins: trailing READY overrides earlier NOT READY
        ("NOT READY then READY", True),
        # Edge cases
        ("", False),
        ("some other text", False),
    ],
)
def test_detect_ready(text: str, expected: bool) -> None:
    assert _detect_ready(text) == expected
