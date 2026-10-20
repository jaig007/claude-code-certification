"""Tests for calc.py functions and the cli.py command-line interface."""

import subprocess
import sys

import pytest

from calc import add, subtract, multiply, divide, power, average


# ── Unit tests for calc.py ────────────────────────────────────────────────────

def test_add() -> None:
    """add returns correct sum."""
    assert add(2, 3) == 5.0


def test_subtract() -> None:
    """subtract returns correct difference."""
    assert subtract(10, 3) == 7.0


def test_multiply() -> None:
    """multiply returns correct product."""
    assert multiply(4, 5) == 20.0


def test_divide() -> None:
    """divide returns correct quotient."""
    assert divide(10, 2) == 5.0


def test_divide_by_zero() -> None:
    """divide raises ValueError when divisor is zero."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_power() -> None:
    """power returns correct result."""
    assert power(2, 8) == 256.0


def test_average() -> None:
    """average returns correct mean."""
    assert average([1, 2, 3]) == 2.0


def test_average_empty() -> None:
    """average raises ValueError on an empty list."""
    with pytest.raises(ValueError, match="empty"):
        average([])


# ── CLI integration tests ─────────────────────────────────────────────────────

def _run(*args: str) -> subprocess.CompletedProcess:
    """Run cli.py with the given arguments and return the result."""
    return subprocess.run(
        [sys.executable, "cli.py", *args],
        capture_output=True,
        text=True,
    )


def test_cli_add() -> None:
    """CLI add prints correct result."""
    result = _run("add", "2", "3")
    assert result.returncode == 0
    assert result.stdout.strip() == "5.0"


def test_cli_subtract() -> None:
    """CLI subtract prints correct result."""
    result = _run("subtract", "10", "3")
    assert result.returncode == 0
    assert result.stdout.strip() == "7.0"


def test_cli_multiply() -> None:
    """CLI multiply prints correct result."""
    result = _run("multiply", "4", "5")
    assert result.returncode == 0
    assert result.stdout.strip() == "20.0"


def test_cli_divide() -> None:
    """CLI divide prints correct result."""
    result = _run("divide", "10", "2")
    assert result.returncode == 0
    assert result.stdout.strip() == "5.0"


def test_cli_divide_by_zero() -> None:
    """CLI divide by zero exits with code 1 and prints an error."""
    result = _run("divide", "10", "0")
    assert result.returncode == 1
    assert "Error" in result.stderr


def test_cli_power() -> None:
    """CLI power prints correct result."""
    result = _run("power", "2", "8")
    assert result.returncode == 0
    assert result.stdout.strip() == "256.0"


def test_cli_average() -> None:
    """CLI average prints correct mean."""
    result = _run("average", "1", "2", "3")
    assert result.returncode == 0
    assert result.stdout.strip() == "2.0"


def test_cli_unknown_operation() -> None:
    """CLI exits non-zero for an unknown operation."""
    result = _run("foo")
    assert result.returncode != 0
