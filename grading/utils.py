import grpc
import success_pb2_grpc
import success_pb2
import grading_pb2_grpc
import grading_pb2
import sys
import os
sys.path.append(os.path.abspath('../'))


def grade(task: str):
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = grading_pb2_grpc.GraderStub(channel)
    taskName = grading_pb2.Task(task=task)
    print(stub.Grade(taskName).response)


def submit():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = grading_pb2_grpc.GraderStub(channel)
    print(stub.Submit(grading_pb2.Empty()).response)


def complete(session_name: str, task: str):
  with grpc.insecure_channel('chat-bazaar-proxy:50051') as channel:
    stub = success_pb2_grpc.ProxyStub(channel)
    response = stub.Success(success_pb2.Task(task=task, session_name=session_name))
    print(response.response)
