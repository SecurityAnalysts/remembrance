class HandleException(Exception):
    ...


class ProcessException(Exception):
    ...


class ProcessNotFoundException(ProcessException):
    ...


class ThreadException(Exception):
    ...


class ModuleException(Exception):
    ...


class ModuleNotFoundException(ModuleException):
    ...
