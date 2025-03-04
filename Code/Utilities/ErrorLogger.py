import sys
import traceback
from datetime import datetime


def log_error(error_message, error_traceback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}]\n")
        log_file.write(f"Error: {error_message}\n")
        log_file.write(f"Traceback:\n{error_traceback}\n")
        log_file.write("-" * 50 + "\n")


def exception_handler(exc_type, exc_value, exc_traceback):
    error_message = str(exc_value)
    error_traceback = "".join(traceback.format_tb(exc_traceback))
    log_error(error_message, error_traceback)

    # Print the full error and traceback to console
    print("An error occurred:")
    print(f"Error Type: {exc_type.__name__}")
    print(f"Error Message: {error_message}")
    print("Traceback:")
    print(error_traceback)
    print("This error has been logged to error_log.txt")


def print_error_message(error_message, error_traceback):
    print("An error occurred:")
    print(f"Error message: {error_message}")
    print("Traceback:")
    print(error_traceback)
    print("This error has been logged to the error log file.")


# Set the custom exception handler
sys.excepthook = exception_handler
