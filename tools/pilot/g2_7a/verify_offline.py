#!/usr/bin/env python3
"""One offline review check; PILOT_ONLY / NON_PRODUCTION, never authorization.

Builder/source validation uses local Git reads. Tests are in-memory/temporary
and run with network/process entrypoints blocked. Static inventories and text
diagnostics do not prove physical isolation or universal absence of I/O.
"""

from __future__ import annotations

import ast
import json
import os
import re
import socket
import subprocess
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

import build_bundle as builder
import validate_bundle


def validate_candidate_snapshot(root: Path) -> validate_bundle.ValidationReport:
    """Candidate-only restrictions, separate from reusable frozen-input integrity."""
    report = validate_bundle.ValidationReport()
    base = root / "docs/pilot/g2.7a"
    forbidden = [path for pattern in ("**/*authorization*.json", "**/*preflight-result*", "**/*.jsonl", "**/*raw-output*")
                 for path in base.glob(pattern)]
    report.check(not forbidden, "CANDIDATE_AUTHORIZATION_OR_RUN_OUTPUT_PRESENT")
    tree = ast.parse((root / "tools/pilot/g2_7a/transport.py").read_text(encoding="utf-8"))
    classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    report.check(classes == {
        "TransportResponse", "TransportError", "Session", "Transport", "FakeCall",
        "FakeSessionState", "FakeSession", "FakeTransport",
    }, "CANDIDATE_TRANSPORT_TYPE_INVENTORY_CHANGED")
    # Inventory changes require review; matching class names is not proof of no calls.
    paths = [path for directory in (base, root / "tools/pilot/g2_7a")
             for path in directory.rglob("*") if path.is_file()]
    state = root / "docs/CURRENT_STATE.md"
    if state.is_file():
        paths.append(state)
    private_path = re.compile(rb"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]")
    report.check(all(private_path.search(path.read_bytes()) is None for path in paths),
                 "CANDIDATE_PRIVATE_ABSOLUTE_PATH_PRESENT")
    return report


def run_tests(root: Path) -> unittest.TestResult:
    with ExitStack() as stack:
        for owner, name in ((socket, "socket"), (socket, "create_connection"),
                            (subprocess, "Popen"), (os, "system")):
            stack.enter_context(patch.object(owner, name, side_effect=AssertionError("offline tests forbid network/process calls")))
        if hasattr(os, "startfile"):
            stack.enter_context(patch.object(os, "startfile", side_effect=AssertionError("offline tests forbid external commands")))
        suite = unittest.defaultTestLoader.discover(str(root / "tools/pilot/g2_7a/tests"))
        return unittest.TextTestRunner(verbosity=2).run(suite)


def main() -> int:
    sys.dont_write_bytecode = True
    root = builder.repo_root()
    if builder.main(["--check"]) != 0:
        return 1
    if validate_bundle.validate_repository(root) != 0:
        return 1
    report = validate_candidate_snapshot(root)
    print(json.dumps({"stage": "candidate_snapshot", "checks_passed": report.checks_passed,
                      "errors": report.errors, "isolation_proven": False}, sort_keys=True))
    if report.errors:
        return 1
    result = run_tests(root)
    passed = result.wasSuccessful()
    print(json.dumps({"stage": "offline_review", "status": "PASS" if passed else "FAIL",
                      "tests_run": result.testsRun, "execution_authorized": False,
                      "independent_review": False}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
