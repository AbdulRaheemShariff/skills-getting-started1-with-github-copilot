"""
TestRigor-like natural language testing framework for the Mergington High School API.

This module provides a plain-English, step-based API testing DSL that mirrors the
way TestRigor lets you describe tests in human-readable language.
"""

from __future__ import annotations

from typing import Any

from httpx import Client, Response


class Step:
    """Represents a single recorded test step with its outcome."""

    def __init__(self, description: str, passed: bool, detail: str = "") -> None:
        self.description = description
        self.passed = passed
        self.detail = detail

    def __repr__(self) -> str:  # pragma: no cover
        status = "✓" if self.passed else "✗"
        detail = f" ({self.detail})" if self.detail else ""
        return f"  [{status}] {self.description}{detail}"


class APITestSuite:
    """
    A fluent, plain-English API testing helper inspired by TestRigor.

    Usage example::

        with APITestSuite(app) as test:
            test.given("a fresh activities list")
            test.when("I request GET /activities")
            response = test.call("GET", "/activities")
            test.then("the response should be successful", response.status_code == 200)
            test.check_field(response.json(), "Chess Club", exists=True)
    """

    def __init__(self, app: Any) -> None:
        self._app = app
        self._client: Client | None = None
        self._steps: list[Step] = []

    # ------------------------------------------------------------------ #
    # Context manager                                                       #
    # ------------------------------------------------------------------ #

    def __enter__(self) -> "APITestSuite":
        from fastapi.testclient import TestClient

        self._client = TestClient(self._app)
        return self

    def __exit__(self, *_: Any) -> None:
        self._print_report()

    # ------------------------------------------------------------------ #
    # Plain-English step recorders                                         #
    # ------------------------------------------------------------------ #

    def given(self, description: str) -> "APITestSuite":
        """Record a 'given' (precondition) step — always passes."""
        self._steps.append(Step(f"Given {description}", passed=True))
        return self

    def when(self, description: str) -> "APITestSuite":
        """Record a 'when' (action) step — always passes."""
        self._steps.append(Step(f"When {description}", passed=True))
        return self

    def then(self, description: str, condition: bool, detail: str = "") -> "APITestSuite":
        """Record a 'then' (assertion) step; raises AssertionError on failure."""
        step = Step(f"Then {description}", passed=condition, detail=detail)
        self._steps.append(step)
        assert condition, f"Step failed: {description}" + (f" — {detail}" if detail else "")
        return self

    def check(self, description: str, condition: bool, detail: str = "") -> "APITestSuite":
        """Generic inline check; raises AssertionError on failure."""
        step = Step(f"Check {description}", passed=condition, detail=detail)
        self._steps.append(step)
        assert condition, f"Check failed: {description}" + (f" — {detail}" if detail else "")
        return self

    # ------------------------------------------------------------------ #
    # HTTP helpers                                                          #
    # ------------------------------------------------------------------ #

    def call(self, method: str, url: str, **kwargs: Any) -> Response:
        """
        Execute an HTTP request and record the step.

        :param method: HTTP verb, e.g. "GET" or "POST".
        :param url: Request path relative to the app root.
        """
        assert self._client is not None, "Must be used inside a 'with' block"
        response = getattr(self._client, method.lower())(url, **kwargs)
        self._steps.append(
            Step(
                f"Call {method.upper()} {url}",
                passed=True,
                detail=f"status={response.status_code}",
            )
        )
        return response

    # ------------------------------------------------------------------ #
    # Higher-level assertion helpers (TestRigor-style)                     #
    # ------------------------------------------------------------------ #

    def check_status(self, response: Response, expected: int) -> "APITestSuite":
        """Verify the HTTP response status code."""
        return self.check(
            f"response status is {expected}",
            response.status_code == expected,
            detail=f"got {response.status_code}",
        )

    def check_field(
        self, data: dict[str, Any], field: str, *, exists: bool = True
    ) -> "APITestSuite":
        """Verify whether a key exists (or does not exist) in a dict."""
        present = field in data
        if exists:
            return self.check(
                f'field "{field}" exists in response',
                present,
                detail="field missing" if not present else "",
            )
        return self.check(
            f'field "{field}" is absent from response',
            not present,
            detail="field unexpectedly present" if present else "",
        )

    def check_value(
        self, data: dict[str, Any], field: str, expected: Any
    ) -> "APITestSuite":
        """Verify the value of a specific field in a dict."""
        if field not in data:
            return self.check(
                f'field "{field}" equals {expected!r}',
                False,
                detail="field is missing from response",
            )
        actual = data[field]
        return self.check(
            f'field "{field}" equals {expected!r}',
            actual == expected,
            detail=f"got {actual!r}",
        )

    def check_contains(self, container: Any, item: Any) -> "APITestSuite":
        """Verify that *item* is contained in *container*."""
        return self.check(
            f"{item!r} is present in result",
            item in container,
            detail=f"not found in {container!r}",
        )

    def check_not_contains(self, container: Any, item: Any) -> "APITestSuite":
        """Verify that *item* is NOT contained in *container*."""
        return self.check(
            f"{item!r} is absent from result",
            item not in container,
            detail=f"unexpectedly found in {container!r}",
        )

    # ------------------------------------------------------------------ #
    # Reporting                                                             #
    # ------------------------------------------------------------------ #

    def _print_report(self) -> None:  # pragma: no cover
        print("\n--- Test steps ---")
        for step in self._steps:
            print(repr(step))
