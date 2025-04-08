import multiprocessing


class RequiresSpawnContext:
    """Some functionality of airo-ipc requires that Python's multiprocessing context is set to 'spawn'.
    When this is not the case, functionality can silently fail. To avoid this happening, we use this class to check the context.
    We log a warning if the context is not 'spawn', and suggest to call `initialize_ipc()`.
    Any classes that use multiprocessing functionality should therefore inherit from this class, and call this class's __init__ method
    in their own __init__ method.

    Known classes that should inherit from RequiresSpawnContext:
    - SMReader
    - SMWriter
    """
    __airo_ipc_checked_multiprocessing_start_method = False

    def __init__(self):
        if not RequiresSpawnContext.__airo_ipc_checked_multiprocessing_start_method:
            from loguru import logger

            current_start_method = multiprocessing.get_start_method(allow_none=True)
            if current_start_method != 'spawn':
                logger.warning(f"The multiprocessing start method is not 'spawn', but '{current_start_method}'. "
                                   "This may cause issues with shared memory, leading to silent failures that are hard to debug! "
                                   "Consider calling `initialize_ipc()`.")
            RequiresSpawnContext.__airo_ipc_checked_multiprocessing_start_method = True
