import subprocess


def test_project_script():
    """
    Test that the project script metadata is correct.
    """
    subprocess.check_call(["uv", "run", "claudebook", "--help"])  # noqa: S607
