class LightwaveError(Exception):
    """Base exception for all Lightwave errors."""
    pass

class TaskError(LightwaveError):
    """Base exception for task-related errors."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found."""
    pass

class TaskValidationError(TaskError):
    """Raised when task validation fails."""
    pass

class SprintError(LightwaveError):
    """Base exception for sprint-related errors."""
    pass

class SprintNotFoundError(SprintError):
    """Raised when a sprint cannot be found."""
    pass

class SprintValidationError(SprintError):
    """Raised when sprint validation fails."""
    pass

class ScrumError(LightwaveError):
    """Base exception for scrum-related errors."""
    pass

class ScrumNotFoundError(ScrumError):
    """Raised when a scrum project cannot be found."""
    pass

class ScrumValidationError(ScrumError):
    """Raised when scrum validation fails."""
    pass

class ConfigurationError(LightwaveError):
    """Raised when there is a configuration error."""
    pass

class DependencyError(LightwaveError):
    """Raised when there is a dependency-related error."""
    pass

class CircularDependencyError(DependencyError):
    """Raised when a circular dependency is detected."""
    pass

class FileOperationError(LightwaveError):
    """Raised when a file operation fails."""
    pass

class PermissionError(LightwaveError):
    """Raised when there are insufficient permissions."""
    pass 