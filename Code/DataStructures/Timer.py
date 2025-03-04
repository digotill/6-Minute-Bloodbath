class Timer:
    def __init__(self, duration, start_time, func=None):
        self.duration = duration  # Set the timer duration
        self.func = func  # Optional function to call when timer finishes
        self.active = True  # Timer starts as active
        self.start_time = start_time  # Set the start time
        self.current_time = self.start_time  # Initialize current time

    def reactivate(self, start_time):
        self.active = True  # Reactivate the timer
        self.start_time = start_time  # Set new start time
        self.current_time = self.start_time  # Reset current time

    def update(self, current_time):
        if self.active:
            self.current_time = current_time  # Update current time
            if self.current_time - self.start_time >= self.duration:
                if self.func:
                    self.func()  # Call function if set
                self.active = False  # Deactivate timer
                return True  # Timer finished
        return False  # Timer not finished

    def check(self, current_time):
        return current_time - self.start_time >= self.duration  # Check if duration elapsed

    @property
    def elapsed(self):
        if not self.active:
            return 0  # Return 0 if timer is not active
        return self.current_time - self.start_time  # Calculate elapsed time

    @property
    def remaining(self):
        if not self.active:
            return self.duration  # Return full duration if not active
        return max(0, self.duration - self.elapsed)  # Calculate remaining time

    @property
    def is_finished(self):
        return not self.active  # Check if timer is finished
