import json
import requests
import os
import re
import grading_pb2
import grading_pb2_grpc
import local_grader
import grading_utils
from concurrent import futures
import logging
import grpc
import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LocalGradingService(grading_pb2_grpc.GraderServicer):
  def __init__(self) -> None:
    super().__init__()
    # there is one local grader object which calls into
    # task specific test cases
    self.localGrader = local_grader.LocalGrader()
    self.ope_session_name = os.getenv("OPE_SESSION_NAME")
    self.namespace = os.getenv("OPE_SESSION_NAMESPACE")

  def Grade(self, request, context):
    task = request.task
    logger.debug(f'[DEBUG][LocalGradingService]: Call Grade {task}')
    response = grading_utils.extract_tagged_content(f'workspace/workspace.ipynb', task)

    pass_task, feedback = self.localGrader.grade(response, task)
    logger.debug(f'[DEBUG][LocalGradingService]: result is {pass_task}. Feedback is {feedback}')

    if pass_task:
      # send response to bot and students
      # that task status is pass
      logger.debug(f'[DEBUG][LocalGradingService-->Proxy]: Call Complete {self.ope_session_name}/{task}')
      utils.complete(session_name=self.ope_session_name, task=task)
    return grading_pb2.Response(response=feedback)

  def getPostQuizToken(self, submission_username, submission_password):
      """
      args:
         submission_username: SAIL() username
         submission_password: SAIL() password
      """
      # retrieve post quiz token
      # moduleSlug = "ope-learn-autoscalin-mpfs4jua"
      # url = f"https://theproject.zone/api/get_tokens/?key=vXuGzlO3a89BE76pcvXRivaeHjZNK9sxftrdejmbqHGm56c1nMkc30cg2AyrDmsu&submission_password={submission_password}&course=cloud-admi-learn-87mc1pjd&module={moduleSlug}&entity={submission_username}"
      # response = requests.get(url)
      # tokenJson = json.loads(response.content.decode('utf-8'))
      # tokens = tokenJson["tokens"]
      # for tokObj in tokens:
      #   if tokObj["descriptive_name"] == "post_quiz_token":
      #     return tokObj["token"]
      return ""

  def Submit(self, request, context):
    # iterate through each student in session
    # and make a submission for that student to AGS (which will submit to SAIL())
    url = f'https://ope.sailplatform.org/api/v1/getSubmissionInfo/{self.namespace}/{self.ope_session_name}'
    response = requests.get(url)
    participantList = json.loads(response.content.decode('utf-8'))
    resp = 'Submission successful. Thank you.'
    for participant in participantList:
      submission_username = participant.get('email', '')
      submission_password = participant.get('password', '')
      postQuizToken = self.getPostQuizToken(submission_username, submission_password)
      logger.debug(f'[DEBUG][Submission]: Submit {submission_username}/{submission_password}')
      self.localGrader.submit(submission_username, submission_password)
      # resp += f'Post Quiz Token for {submission_username} is {postQuizToken}\n'
    return grading_pb2.Response(response=resp)

  def Release(self, request, context):
    # release next task to Jupyter Notebook
    task = request.task
    logger.debug(f'[DEBUG][LocalGradingService]: call release {task}')
    grading_utils.release(task=task)
    resp = f'Released {task}.'
    return grading_pb2.Response(response=resp)


def serve():
  logger.debug(f'[DEBUG][LocalGradingService]: Start')
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  grading_pb2_grpc.add_GraderServicer_to_server(LocalGradingService(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
  serve()
