class FileManagerError(Exception):
    """Base exception for FileManager errors."""
    pass


class FileSaveError(FileManagerError):
    """Raised when a file cannot be saved."""
    pass
