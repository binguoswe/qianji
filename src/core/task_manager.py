"""
Qji Max Task Manager - Multi-task Parallel Processing System
Handles concurrent subtasks with proper resource management and coordination.
"""
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Callable, Optional
import time
import logging

class TaskManager:
    def __init__(self, max_workers: int = 10):
        """Initialize task manager with thread pool."""
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_results: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        
    def create_subtask(self, task_id: str, func: Callable, *args, **kwargs) -> str:
        """
        Create a subtask for parallel execution.
        
        Args:
            task_id: Unique identifier for the task
            func: Function to execute
            *args, **kwargs: Arguments for the function
            
        Returns:
            Task ID
        """
        if task_id in self.active_tasks:
            raise ValueError(f"Task ID {task_id} already exists")
            
        self.active_tasks[task_id] = {
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'status': 'pending',
            'start_time': None,
            'end_time': None,
            'result': None,
            'error': None
        }
        
        return task_id
        
    def execute_subtask(self, task_id: str) -> Any:
        """
        Execute a single subtask synchronously.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task result or raises exception
        """
        if task_id not in self.active_tasks:
            raise ValueError(f"Task ID {task_id} not found")
            
        task = self.active_tasks[task_id]
        task['status'] = 'running'
        task['start_time'] = time.time()
        
        try:
            result = task['func'](*task['args'], **task['kwargs'])
            task['status'] = 'completed'
            task['result'] = result
            task['end_time'] = time.time()
            self.task_results[task_id] = result
            return result
        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)
            task['end_time'] = time.time()
            self.logger.error(f"Task {task_id} failed: {e}")
            raise e
            
    def execute_parallel_tasks(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        Execute multiple tasks in parallel using thread pool.
        
        Args:
            task_ids: List of task identifiers to execute
            
        Returns:
            Dictionary of task results {task_id: result}
        """
        futures = {}
        results = {}
        
        # Submit all tasks to thread pool
        for task_id in task_ids:
            if task_id not in self.active_tasks:
                raise ValueError(f"Task ID {task_id} not found")
                
            task = self.active_tasks[task_id]
            future = self.executor.submit(
                self._execute_task_wrapper, 
                task_id, 
                task['func'], 
                task['args'], 
                task['kwargs']
            )
            futures[future] = task_id
            
        # Collect results
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                result = future.result()
                results[task_id] = result
            except Exception as e:
                self.logger.error(f"Task {task_id} failed: {e}")
                results[task_id] = {'error': str(e)}
                
        return results
        
    def _execute_task_wrapper(self, task_id: str, func: Callable, args: tuple, kwargs: dict) -> Any:
        """Wrapper function for thread pool execution."""
        task = self.active_tasks[task_id]
        task['status'] = 'running'
        task['start_time'] = time.time()
        
        try:
            result = func(*args, **kwargs)
            task['status'] = 'completed'
            task['result'] = result
            task['end_time'] = time.time()
            return result
        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)
            task['end_time'] = time.time()
            raise e
            
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get current status of a task."""
        if task_id not in self.active_tasks:
            raise ValueError(f"Task ID {task_id} not found")
        return self.active_tasks[task_id].copy()
        
    def get_all_task_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all tasks."""
        return {tid: task.copy() for tid, task in self.active_tasks.items()}
        
    def cleanup_completed_tasks(self):
        """Clean up completed tasks to free memory."""
        completed_tasks = [
            tid for tid, task in self.active_tasks.items() 
            if task['status'] in ['completed', 'failed']
        ]
        for tid in completed_tasks:
            del self.active_tasks[tid]
            
    def shutdown(self):
        """Shutdown the thread pool."""
        self.executor.shutdown(wait=True)

# Async version for web applications
class AsyncTaskManager:
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks: Dict[str, asyncio.Task] = {}
        
    async def execute_async_task(self, task_id: str, coro: asyncio.Coroutine) -> Any:
        """Execute an async task with concurrency control."""
        async with self.semaphore:
            task = asyncio.create_task(coro)
            self.active_tasks[task_id] = task
            try:
                result = await task
                return result
            finally:
                if task_id in self.active_tasks:
                    del self.active_tasks[task_id]
                    
    async def execute_multiple_async_tasks(self, tasks: Dict[str, asyncio.Coroutine]) -> Dict[str, Any]:
        """Execute multiple async tasks concurrently."""
        task_coros = [
            self.execute_async_task(tid, coro) 
            for tid, coro in tasks.items()
        ]
        results = await asyncio.gather(*task_coros, return_exceptions=True)
        
        # Map results back to task IDs
        result_dict = {}
        for i, (tid, _) in enumerate(tasks.items()):
            if isinstance(results[i], Exception):
                result_dict[tid] = {'error': str(results[i])}
            else:
                result_dict[tid] = results[i]
                
        return result_dict

# Example usage and testing
def example_search_task(query: str, source: str = "web") -> Dict[str, Any]:
    """Example search task function."""
    from .web_search import WebSearch
    searcher = WebSearch()
    return searcher.search(query, source=source)

def example_skill_task(skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Example skill task function."""
    from .skills import SkillManager
    skill_manager = SkillManager()
    return skill_manager.execute_skill(skill_name, input_data)

if __name__ == "__main__":
    # Test the task manager
    import json
    
    # Initialize task manager
    tm = TaskManager(max_workers=5)
    
    # Create search tasks
    search_task1 = tm.create_subtask("search1", example_search_task, "人工智能最新发展")
    search_task2 = tm.create_subtask("search2", example_search_task, "量子计算突破")
    
    # Create skill tasks  
    skill_task1 = tm.create_subtask("skill1", example_skill_task, "weather", {"location": "北京"})
    
    # Execute all tasks in parallel
    all_tasks = [search_task1, search_task2, skill_task1]
    results = tm.execute_parallel_tasks(all_tasks)
    
    print("Parallel task results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Cleanup
    tm.cleanup_completed_tasks()
    tm.shutdown()