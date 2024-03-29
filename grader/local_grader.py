import grading_utils as utils
import taskTest
import submitter_script
from typing import Tuple
import time

class Feedback:
  def __init__(self, score: int, message: str = "") -> None:
    self.message = message
    self.score = score

  def __str__(self) -> str:
    return f"Feedback:\n{self.message}" + f"\n***Final Score***: {self.score}"

class LocalGrader:
  def __init__(self) -> None:
    self.responseUnchanged = utils.extract_tagged_content(f'./response_unchanged.ipynb', 'task0')
    self.feedbacks = {}
    self.response_cells = set([
      'task1a',
      'task1a2',
      'task1b',
      'task1b2',
      'task1c',
      'task1c2',
      'task1d',
      'task1d2',
      'task2a',
      'task2a2',
      'task2b',
      'task2b2',
      'task2c',
      'task2c2',
      'task2d',
      'task2d2',
      'task3a',
      'task3a2',
      'task3b',
      'task3b2',
      'task3c',
      'task3c2',
      'task3d',
      'task3d2'])
    self.result = {
      task_tag : 0
      for task_tag in self.response_cells
    }

  def grade(self, response:str, task: str)-> Tuple[bool, str]:
    if task not in self.response_cells:
      return False, f"Task does not exist: {task}"
    passed = True

    try:
      result = [response + "\nTEMP result"]
      with open("result", "w") as f:
        f.writelines(result)
    except Exception as e:
      passed, feedback_message = False, f"local_grader.grade() failed with:\n{e}"

    if passed:
      # feedback_message = task
      feedback_message = taskTest.test(task)
      passed = utils.read_test_json(task, "tests.json")

      if (response != self.responseUnchanged):
        passed = True
      else:
        passed = False

    feedback = Feedback(int(passed), feedback_message)
    self.feedbacks[task] = feedback
    if passed:
      self.result[task] = "passed"
    else:
      self.result[task] = "failed"
    return passed, str(feedback)

  def submit(self, username: str, password: str)  -> None:
    for task in self.result.keys():
      passed = utils.read_test_json(task, "tests.json")
      if passed:
        self.result[task] = "passed"
      else:
        self.result[task] = "failed"
    submitter_script.submit(username, password, self.result)

if __name__ == '__main__':
  grader = LocalGrader()
  for task_tag in grader.test_function_map.keys():
    task_code = utils.extract_tagged_content(f'../tasks/{task_tag}.ipynb', task_tag)
    task_fn = utils.string_to_function(task_code, task_tag)
    passed, task_feedback = grader.grade(task_tag, task_fn)
    print(task_feedback)
        