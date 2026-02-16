from fastapi import HTTPException, status

class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )

class TaskCreationException(HTTPException):
    def __init__(self, detail: str = "Failed to create task."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class TaskUpdateException(HTTPException):
    def __init__(self, task_id: int, detail: str = "Failed to update task."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task with ID {task_id}. {detail}"
        )

class TaskDeletionException(HTTPException):
    def __init__(self, task_id: int, detail: str = "Failed to delete task."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task with ID {task_id}. {detail}"
        )
