import grading_utils as utils
import mysql.connector
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
    self.feedbacks = {}
    self.test_functions = set([
      'task1',
      'task2',
      'task3'])
    self.result = {
      task_tag : 0
      for task_tag in self.test_functions
    }

    count = 120
    while count:
      try:
        # create connection to mysql container
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="CloudCC@100",
            database="employees"
        )
        count = 0
      except Exception:
        time.sleep(5)
        count -= 5
    self.mydb.close()


  def grade(self, sql_query:str, task: str)-> Tuple[bool, str]:
    if task not in self.test_functions:
      return False, f"Task does not exist: {task}"
    
    self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="CloudCC@100",
            database="employees"
    )

    mycursor = self.mydb.cursor()

    explain_sql_query = f"EXPLAIN FORMAT=JSON {sql_query}"

    passed = True
    # execute explain command and save
    try:
      mycursor.execute(explain_sql_query)
      explain_result = mycursor.fetchall()
      with open("explain.json", "w") as f:
        f.write(explain_result[0][0].replace("\n", ""))
    except Exception as e:
      passed, feedback_message = False, f"Your Query: {sql_query}\n\nRunning sql command failed with:\n{e}"

    # execute sql and save
    try:
      mycursor.execute(sql_query)
      sql_result = mycursor.fetchall()

      result = []
      for res in sql_result:
        res = [str(r) for r in res]
        result.append("{}\n".format("\t".join(res)))

      with open("result", "w") as f:
        f.writelines(result)

    except Exception as e:
      passed, feedback_message = False, f"Your Query: {sql_query}\n\nRunning sql command failed with:\n{e}"
    
    mycursor.close()
    self.mydb.close()

    if passed:
      feedback_message = taskTest.test(task)
      passed = utils.read_test_json(task, "tests.json")

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
    task_code = utils.extract_task_n_code(f'../tasks/{task_tag}.ipynb', task_tag)
    task_fn = utils.string_to_function(task_code, task_tag)
    passed, task_feedback = grader.grade(task_tag, task_fn)
    print(task_feedback)
        