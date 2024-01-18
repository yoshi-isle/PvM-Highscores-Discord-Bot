from Crypto.Random import random
from dataclasses import dataclass
from typing import List
from constants.dartboard_tasks import tasks

@dataclass(frozen=True)
class Task:
    """
    Defines a singluar task for kitty dartboard
    """

    task_name: str
    task_number: int
    task_description: str
    task_points: int
    task_challenge_name: str
    task_challenge_description: str
    task_challenge_points: int
    image_link: str
    

class TaskManager:
    """
    
    """
    def __init__(self):
        self.tasks = {}

    def add_task(self, task: Task):
        self.tasks[task.task_number] = task

    def load_tasks(self, task_list: List[Task]):
        for task_info in task_list:
            task = Task(**task_info)
            self.add_task(task)

    def get_task(self, task_number:int) -> Task:
        return self.tasks.get(task_number, None)


class Dartboard:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_manager.load_tasks(tasks)


    def roll_dice(self) -> int:
        """
        Generates a task for a team and posts the embed to the rolling channel
        """
        task_number: int = random.randint(1,72)

    def get_task(self) -> Task:
        """
        """
        task_number = self.roll_dice()
        return self.task_manager.get_task(task_number=task_number)