"""
Plain-English tests for the Mergington High School API.

Each test is written in a TestRigor-inspired Given / When / Then style so
that the intent is immediately clear to non-technical readers.
"""

import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities
from tests.test_framework import APITestSuite


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory database to its original state after every test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


# ──────────────────────────────────────────────────────────────────────────────
# GET /activities
# ──────────────────────────────────────────────────────────────────────────────


def test_get_activities_returns_all_activities():
    """Check that all three default activities are returned."""
    with APITestSuite(app) as test:
        test.given("the default activity database is loaded")
        test.when("I request the list of activities")
        response = test.call("GET", "/activities")
        test.then("the request succeeds", response.status_code == 200)
        data = response.json()
        test.check_field(data, "Chess Club")
        test.check_field(data, "Programming Class")
        test.check_field(data, "Gym Class")


def test_get_activities_includes_schedule_and_participants():
    """Verify that each activity has a schedule and a participants list."""
    with APITestSuite(app) as test:
        test.given("the default activity database is loaded")
        test.when("I request the list of activities")
        response = test.call("GET", "/activities")
        test.check_status(response, 200)
        chess = response.json()["Chess Club"]
        test.check_field(chess, "schedule")
        test.check_field(chess, "participants")
        test.check_field(chess, "max_participants")


# ──────────────────────────────────────────────────────────────────────────────
# POST /activities/{activity_name}/signup
# ──────────────────────────────────────────────────────────────────────────────


def test_student_can_sign_up_for_activity():
    """A new student email can be added to an existing activity."""
    with APITestSuite(app) as test:
        test.given("a student who is not yet signed up for Chess Club")
        test.when("they submit the sign-up form for Chess Club")
        response = test.call(
            "POST",
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"},
        )
        test.then("the sign-up is accepted", response.status_code == 200)
        test.check_contains(
            activities["Chess Club"]["participants"],
            "newstudent@mergington.edu",
        )


def test_signup_for_unknown_activity_returns_404():
    """Attempting to sign up for a non-existent activity must return 404."""
    with APITestSuite(app) as test:
        test.given("an activity that does not exist")
        test.when("a student tries to sign up for it")
        response = test.call(
            "POST",
            "/activities/Underwater Basket Weaving/signup",
            params={"email": "student@mergington.edu"},
        )
        test.then("the server responds with 404", response.status_code == 404)


def test_signup_response_contains_confirmation_message():
    """The signup response body should include a confirmation message."""
    with APITestSuite(app) as test:
        test.given("a valid activity and student email")
        test.when("the student signs up")
        response = test.call(
            "POST",
            "/activities/Gym Class/signup",
            params={"email": "runner@mergington.edu"},
        )
        test.check_status(response, 200)
        body = response.json()
        test.check_field(body, "message")
        test.check_contains(body["message"], "runner@mergington.edu")


def test_multiple_students_can_join_same_activity():
    """More than one student can sign up for the same activity."""
    with APITestSuite(app) as test:
        test.given("two new students who want to join Programming Class")
        test.when("both students submit the sign-up form")
        for email in ("alice@mergington.edu", "bob@mergington.edu"):
            test.call(
                "POST",
                "/activities/Programming Class/signup",
                params={"email": email},
            )
        test.then(
            "both students appear in the participants list",
            "alice@mergington.edu" in activities["Programming Class"]["participants"]
            and "bob@mergington.edu" in activities["Programming Class"]["participants"],
        )


# ──────────────────────────────────────────────────────────────────────────────
# Root redirect
# ──────────────────────────────────────────────────────────────────────────────


def test_root_redirects_to_index():
    """GET / should redirect to the static index page."""
    client = TestClient(app, follow_redirects=False)
    response = client.get("/")
    assert response.status_code in (301, 302, 307, 308)
    assert "/static/index.html" in response.headers.get("location", "")
