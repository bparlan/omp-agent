#!/usr/bin/env python3
# V-006
# FR-MAIN_ORCHESTRATION
# Test Type: IMPLEMENTATION_CHECK

"""Tests for main.py public interface contract (V-006).

Pre-implementation: main.py does not exist.
Expected VALID_INITIAL_FAILURE: test error with exit code 1.
"""

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def _import_main():
    """Import main module dynamically to avoid collection-time failures."""
    sys.path.insert(0, str(PROJECT_ROOT))
    return importlib.import_module("main")


def test_main_exports_main_callable():
    """V-006: main.py must export a callable main() function."""
    main = _import_main()
    assert hasattr(main, "main"), "main.py must export a 'main' function"
    assert callable(main.main), "main.main must be callable"


def test_main_has_main_guard():
    """V-006: main.py must have if __name__ == '__main__' guard."""
    source = (PROJECT_ROOT / "main.py").read_text(encoding="utf-8")
    assert 'if __name__ == "__main__"' in source or "if __name__ == '__main__'" in source, (
        "main.py must have if __name__ == '__main__' guard"
    )


def test_main_returns_int_exit_status():
    """V-006: main() must return an integer exit status."""
    main = _import_main()
    # Test with --help which should always work
    try:
        exit_code = main.main(["--help"])
    except SystemExit as exc:
        exit_code = exc.code if exc.code is not None else 0

    assert isinstance(exit_code, int), (
        f"main() must return int exit status, got {type(exit_code)}: {exit_code}"
    )


def test_main_interface_matches_spec():
    """V-006: main() interface must match specification contract."""
    main = _import_main()

    # Verify main() accepts expected arguments
    import inspect
    sig = inspect.signature(main.main)
    params = list(sig.parameters.keys())

    # main() should accept argv parameter or similar
    assert len(params) >= 1, "main() must accept at least one parameter (argv or similar)"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
