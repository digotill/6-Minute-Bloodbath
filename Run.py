from Code.Utilities.ErrorLogger import *
from Code.Game import *

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

sys.exit(1)
