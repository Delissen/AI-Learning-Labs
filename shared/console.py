"""
Console helper functions.

Shared helper methods for displaying banners, status messages
and application output throughout the AI Learning Labs.
"""

import os


def clear_console() -> None:
    """
    Clear the console window.
    """

    os.system("cls" if os.name == "nt" else "clear")


def print_banner(title: str) -> None:
    """
    Display a formatted application banner.
    """

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def print_status(message: str) -> None:
    """
    Display a status message.
    """

    print(f"[INFO] {message}")


def print_success(message: str) -> None:
    """
    Display a success message.
    """

    print(f"[SUCCESS] {message}")


def print_warning(message: str) -> None:
    """
    Display a warning message.
    """

    print(f"[WARNING] {message}")


def print_error(message: str) -> None:
    """
    Display an error message.
    """

    print(f"[ERROR] {message}")
