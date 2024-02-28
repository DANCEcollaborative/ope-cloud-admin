# Python server script to monitor MySQL logs and talk to Bazaar.
import os
import sys
import time
import uuid 
import urllib
import logging
import requests
import subprocess
from collections import deque
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

commands_seen = {}
def parse_log(path: str):
    import re
    timestamp_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z'
    argument = ""
    data = []
    with open(path, "r") as f:
        i = 0
        for line in f:
            i += 1
            line = line.strip()
            if i < 4: continue
            words = line.split()
            try: timestamp = words[0].strip()
            except IndexError:
                # print(words, line)
                continue
            if len(re.findall(timestamp_pattern, timestamp)) > 0:
                id = words[1].strip()
                # argument = line.replace(timestamp+"	   "+id+" ", "")
                argument = "\t".join(line.split("\t")[2:])
                command_type = line.split("\t")[1].replace(id, "").strip()
                record = {"timestamp": timestamp, "id": id, "command": argument, "command_type": command_type}
                assert record["timestamp"] is not None
                assert record["id"] is not None
                if command_type == "Query": data.append(record)
            else:
                data[-1]["command"] += ("\n"+line)

    return data

# https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
def tail(filename, n=10):
    'Return the last n lines of a file (memory efficient)'
    with open(filename) as f:
        return deque(f, n) 

def get_last_line(path: str):
    with open(path, 'rb') as f:
        """Time efficient solution for large files."""
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()

        return last_line

SESSION_ID = os.getenv('OPE_SESSION_NAME') #uuid.uuid4().hex[:6].upper() # derive from local properties of server
MYSQL_LOG_FILE_PATH = "/grader/query.log"
OPENAI_SERVER_URL = "https://bazaar.lti.cs.cmu.edu"
BASE_URL = OPENAI_SERVER_URL#+f":{PORT}"

class MySQLLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # print(f'event type: {event.event_type}  path : {event.src_path}')
        if event.event_type == "modified":
            log_commands = parse_log(MYSQL_LOG_FILE_PATH)
            for command in log_commands:
                task_id = "task1" # TODO: find a way to track this.
                if command["command"] not in commands_seen:
                    url = os.path.join(BASE_URL, "interactive_reflection_prompts")
                    params = {"session_id": SESSION_ID, "task_id": task_id, "timestamp": str(command["timestamp"]), "command": command["command"]}
                    url=url+"?"+urllib.parse.urlencode(params)
                    print(url)
                    # print(command["timestamp"], command["command"])
                    # send command, timestamp (and task info) to OpenAI server.
                    resp = requests.get(url)
                    print("STATUS_CODE:", resp.status_code)
                    print("VALUE:", resp.text)
                    # if successful response then only ignore command. Otherwise try to send command again in the future.
                    if resp.status_code == 200:
                        commands_seen[command["command"]] = None
        # print(log_commands)

if __name__ == "__main__":
    while not os.path.exists(MYSQL_LOG_FILE_PATH):
        time.sleep(5)
        try:
            print("Enable MySQL logging")
            subprocess.run(["mysql", "-u", "root", "-pCloudCC@100", "-h", "127.0.0.1", "employees", "-e", "SET GLOBAL general_log_file = '/grader/query.log';"], stdout=subprocess.PIPE)
            subprocess.run(["mysql", "-u", "root", "-pCloudCC@100", "-h", "127.0.0.1", "employees", "-e", "SET GLOBAL general_log = 'ON';"], stdout=subprocess.PIPE)
        except Exception as e:
            print(f"Enable logging failed with: {e}")
            
    event_handler = MySQLLogHandler()
    observer = Observer()
    observer.schedule(event_handler, MYSQL_LOG_FILE_PATH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.stop()
        observer.join()
    observer.join()
