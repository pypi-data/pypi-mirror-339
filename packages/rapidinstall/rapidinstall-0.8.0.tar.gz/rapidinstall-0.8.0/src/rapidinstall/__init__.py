# rapidinstall/__init__.py

# Import the core function to make it available directly under the package namespace
from rapidinstall.run import run_tasks

# Define the public API - the install function
# It's essentially a wrapper around run_tasks for the desired usage pattern
def install(todos, update_interval=None, verbose=True):
    """
    Runs a list of installation tasks (shell commands) in parallel.

    Provides real-time status updates and aggregated output. See run_tasks
    for more detailed argument descriptions.

    Example:
        import rapidinstall
        my_tasks = [
            {'name': 'task1', 'commands': 'echo "Hello"; sleep 2'},
            {'name': 'task2', 'commands': 'echo "World"; sleep 1'}
        ]
        results = rapidinstall.install(my_tasks)
        print(results)

    Args:
        todos: List of task dictionaries [{'name': str, 'commands': str}, ...].
        update_interval (Optional[int]): Print status every N iterations.
            Defaults to executor.DEFAULT_STATUS_UPDATE_INTERVAL.
            Set to 0 or None to disable.
        verbose (bool): Print progress and output to console. Defaults to True.

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary mapping task names to results
            (stdout, stderr, returncode, pid).
    """
    # Use default from executor if not provided
    interval = update_interval if update_interval is not None else run.DEFAULT_STATUS_UPDATE_INTERVAL

    return run_tasks(todos=todos, update_interval=interval, verbose=verbose)

# Package version (consider using importlib.metadata for complex cases)
__version__ = "0.8.0"

# Optionally define __all__ to control `from rapidinstall import *`
__all__ = ['install', 'run_tasks', 'run'] # Expose both the simple and core functions

# Add a reference to the core executor module for potential advanced use
from . import run