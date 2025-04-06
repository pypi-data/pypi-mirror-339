from time import monotonic
from typing import final
import logging
from logging import Logger
from warnings import warn
from threading import Lock

@final
class AsdfTimer():
    """A simple thread-safe utility timer class to measure elapsed time.
    This class provides methods to check, stop, resume, and restart a timer.
    It can also be used as a context manager to automatically stop the timer
    when exiting the context.
    
    Attributes:
        name (str): Name of the timer. Used for logging and printing purposes.
        logger (Logger): Logger instance for logging elapsed time. If None, uses print() instead.
        disable_print (bool): Flag to disable logging when check() or stop() are called.
        print_digits (int): Number of decimal places to print for elapsed time.
        elapsed (float): The elapsed time in seconds.
        is_stopped (bool): Indicates whether the timer is currently stopped.
        
    Methods:
        check() -> float: Output the elapsed time.
        stop() -> float: Pause the timer and output the elapsed time.
        resume() -> None: Unstop the timer.
        restart() -> None: Restart the timer.
    """
    
    name: str
    """Name of the timer. Used for logging and printing purposes."""
    logger: Logger
    """Logger instance for logging elapsed time. If None, uses print() instead."""
    disable_print: bool
    """Flag to disable logging when check() or stop() are called."""
    print_digits: int
    """Number of decimal places to print for elapsed time."""

    def __init__(self, name="AsdfTimer", logger:logging.Logger=None, disable_print:bool=False, print_digits:int=2) -> None:
        """Initialize the Timer instance.

        Args:
            name (str, optional): The name of the timer. Defaults to "AsdfTimer".
            logger (Logger, optional): A logger instance for logging. Uses print() if None.
            disable_print (bool, optional): Whether to disable logging/printing the elapsed time. Defaults to False.
            print_digits (int, optional): Number of decimal places to print for elapsed time. Defaults to 2.
        """        
        self.name = name
        self.logger = logger
        assert isinstance(self.logger, (Logger, type(None))), "logger must be a logging.Logger instance or None"
        self.disable_print = disable_print
        self.print_digits = print_digits
        
        # Start the timer
        self._stop_time = None
        self._elapsed_acc = 0
        self._start_time = monotonic()
        self._lock = Lock()  # Add a threading lock
    
    def _get_is_stopped(self) -> bool:
        """Check if the timer is currently stopped.

        Returns:
            bool: True if the timer is stopped, False otherwise.
        """
        return self._stop_time is not None
    
    @property
    def is_stopped(self) -> bool:
        """Check if the timer is currently stopped.

        Returns:
            bool: True if the timer is stopped, False otherwise.
        """
        return self._get_is_stopped()
    
    def _get_elapsed(self):
        check_time = self._stop_time or monotonic()
        elapsed_time = check_time - self._start_time
        # If the timer was stopped, add the accumulated elapsed time
        elapsed_time += self._elapsed_acc
        return elapsed_time
    
    @property
    def elapsed(self) -> float:
        """Get the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        with self._lock:  # Ensure thread-safe access
            return self._get_elapsed()

    
    def _check(self) -> float:
        """Thread-unsafe version of check()"""
        elapsed_time = self._get_elapsed()
            
        if not self.disable_print:
            message = f'{self.name} took {elapsed_time:.{self.print_digits}f} seconds'
            if self.logger:
                self.logger.info(message)
            else:
                print(message)
        return elapsed_time
    
    def check(self) -> float:
        """Return and output the elapsed time.
        
        Returns:
            float: The elapsed time in seconds.
        """
        with self._lock:  # Ensure thread-safe access
            elapsed_time = self._get_elapsed()
            
        if not self.disable_print:
            message = f'{self.name} took {elapsed_time:.{self.print_digits}f} seconds'
            if self.logger:
                self.logger.info(message)
            else:
                print(message)
        return elapsed_time

    def stop(self) -> float:
        """Pause the timer and check the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        with self._lock:  # Ensure thread-safe access
            if self._stop_time is not None:
                warn(RuntimeWarning("Timer is already stopped. Doing nothing."))
                return self._check()
            self._stop_time = monotonic()
        return self._check()
    
    def resume(self) -> None:
        """Unstop the timer."""
        with self._lock:  # Ensure thread-safe access
            if self._stop_time is None:
                warn(RuntimeWarning("Timer is already running. Doing nothing."))
                return
            # Accumulate the elapsed time and reset the start time
            self._elapsed_acc += self._stop_time - self._start_time
            self._stop_time = None
            self._start_time = monotonic()
        
    
    def restart(self) -> None:
        """Restart the timer."""
        with self._lock:  # Ensure thread-safe access
            self._elapsed_acc = 0
            self._stop_time = None
            self._start_time = monotonic()
        
    
    def __enter__(self):
        """Use the Timer instance as a context manager.

        Returns:
            Timer: The Timer instance itself.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Stop the timer when exiting the context. Output the elapsed time.
        Does not warn if the timer is already stopped."""
        if not self._get_is_stopped():
            self.stop()
        else:
            self.check()
    
    def __repr__(self) -> str:
        """String representation of the Timer instance."""
        return f"Timer(name={self.name}, disable_print={self.disable_print}, print_digits={self.print_digits}, elapsed={self.elapsed:.{self.print_digits}f}, is_stopped={self.is_stopped})"
    
    def __str__(self) -> str:
        """String representation of the Timer instance."""
        return self.__repr__()