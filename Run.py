from Code.Utilities.ErrorLogger import *
from Code.Game import Game
import sys

# Set DPI awareness for Windows
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        log_error("Failed to set DPI awareness on Windows", str(e))

# Set high DPI mode for macOS
elif sys.platform == "darwin":
    try:
        from AppKit import NSApplication, NSApplicationActivationPolicyRegular
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    except Exception as e:
        log_error("Failed to set high DPI mode on macOS", str(e))

Performance_Profile = False

if __name__ == "__main__":
          if Performance_Profile:
                    profiler = cProfile.Profile()
                    profiler.enable()

          try:
                    game = Game()
                    game.run_game()

          except Exception as e:
                    error_message = str(e)
                    error_traceback = traceback.format_exc()
                    log_error(error_message, error_traceback)
                    print_error_message(error_message, error_traceback)
          finally:
                    if Performance_Profile:
                              profiler.disable()
                              stats = Stats(profiler)
                              stats.sort_stats('time').reverse_order().print_stats()
