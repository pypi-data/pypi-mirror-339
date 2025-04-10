import requests
import subprocess
import time
from contextlib import contextmanager
from playwright.sync_api import Page, expect
from requests.exceptions import ConnectionError
from time import sleep
from typing import Literal


def wait_for_server(url: str, timeout: int = 10, interval: float = 0.5):
    """Wait for server to be ready"""
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except ConnectionError:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Server at {url} did not start within {timeout} seconds"
                )
            time.sleep(interval)


@contextmanager
def streamlit_server():
    process = subprocess.Popen(
        [
            "streamlit",
            "run",
            "--server.port=8501",
            "--server.headless=true",
            "tests/app.py",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    url = "http://localhost:8501"
    wait_for_server(url)

    yield

    print("Terminating streamlit server")
    process.terminate()
    process.wait()


def assert_toggle_state_in_main(page: Page, state: Literal["True", "False", "None"]):
    """a string in main app reflect the toggle state inside the dialog, updated by app rerun"""
    expect(page.get_by_text(f"dialog_toggle: {state}")).to_be_visible()


def test_detector(page: Page):
    with streamlit_server():
        page.goto("http://localhost:8501")

        # ================================
        # no detector
        # ================================

        # Verify the toggle state is not initialized
        assert_toggle_state_in_main(page, "None")

        # Click the show modal button
        page.get_by_role("button", name="show modal").click()

        # open dialog trigger rerun, toggle state initialized as False
        assert_toggle_state_in_main(page, "False")

        # Toggle the switch in the dialog
        page.get_by_test_id("stDialog").get_by_test_id("stCheckbox").locator(
            "div"
        ).first.click()

        # press escape key to exit dialog
        page.get_by_role("checkbox", name="my toggle").press("Escape")

        # dectector not added yet, toggle state not updated
        assert_toggle_state_in_main(page, "False")

        # ================================
        # has detector
        # ================================

        # enable detector
        page.get_by_test_id("stCheckbox").locator("div").first.click()

        # Click the show modal button
        page.get_by_role("button", name="show modal").click()

        # open dialog trigger rerun, toggle state updated to True
        assert_toggle_state_in_main(page, "True")

        # Toggle the switch in the dialog
        page.get_by_test_id("stDialog").get_by_test_id("stCheckbox").locator(
            "div"
        ).first.click()

        # open dialog trigger rerun, toggle state not updated before closing dialog
        assert_toggle_state_in_main(page, "True")
        sleep(0.3)

        # press escape key to exit dialog
        page.get_by_role("checkbox", name="my toggle").press("Escape")
        sleep(0.3)

        # detector added, toggle state updated
        assert_toggle_state_in_main(page, "False")
