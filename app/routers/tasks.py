"""Task management endpoints."""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.database import get_db
from app.models import Task, User, TaskStatus
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tasks for the current user with pagination and filtering.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        status: Optional status filter
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[TaskResponse]: List of tasks
    """
    query = select(Task).where(Task.owner_id == current_user.id)
    
    # Apply status filter if provided
    if status:
        query = query.where(Task.status == status)
    
    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Task data
        
    Raises:
        HTTPException: If task not found or unauthorized
    """
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.owner_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Created task data
    """
    db_task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id
    )
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TaskResponse: Updated task data
        
    Raises:
        HTTPException: If task not found or unauthorized
    """
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.owner_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update task fields
    update_data = task_data.model_dump(exclude_unset=True)
    
    # Set completed_at when status changes to DONE
    if "status" in update_data and update_data["status"] == TaskStatus.DONE:
        if task.status != TaskStatus.DONE:
            update_data["completed_at"] = datetime.utcnow()
    elif "status" in update_data and update_data["status"] != TaskStatus.DONE:
        update_data["completed_at"] = None
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If task not found or unauthorized
    """
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.owner_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(task)
    await db.commit()


@router.get("/stats/summary")
async def get_task_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get task statistics for the current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Task statistics
    """
    # Count tasks by status
    result = await db.execute(
        select(Task.status, func.count(Task.id))
        .where(Task.owner_id == current_user.id)
        .group_by(Task.status)
    )
    
    status_counts = {status.value: 0 for status in TaskStatus}
    for status, count in result:
        status_counts[status.value] = count
    
    # Get total count
    total_result = await db.execute(
        select(func.count(Task.id)).where(Task.owner_id == current_user.id)
    )
    total_tasks = total_result.scalar()
    
    return {
        "total_tasks": total_tasks,
        "by_status": status_counts
    }
