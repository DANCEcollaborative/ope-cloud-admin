import tarfile
import os
import shutil
import subprocess

def test(task:str):
    # Compress the logs and create a tar file
    name_of_file = f"{task}.tgz"
    file = tarfile.open(name_of_file,"w:gz")
    file.add("explain.json")
    file.add("result")
    file.add(f"{task}.sql")
    file.close()

    shutil.rmtree('grader/', ignore_errors=True)
    os.mkdir("grader")

    shutil.move(name_of_file, f"grader/{name_of_file}")

    # Call the grader
    shutil.rmtree('local_test_feedback/', ignore_errors=True)

    os.mkdir("local_test_feedback")
    os.mkdir(f"local_test_feedback/{task}")

    files = [f"local_test_feedback/{task}/feedback", f"local_test_feedback/{task}/score", f"local_test_feedback/{task}/log"]
    for fn in files:
        with open(fn, "w") as f:
            pass

    pwd = os.getcwd()

    # call java grader
    grader = f"T{task[1:]}Grader" 
    subprocess.call(["java", "-cp", "ope_grader.jar", grader, f'{pwd}/grader/', f"{task}.tgz", f"../local_test_feedback/{task}/feedback", f"../local_test_feedback/{task}/score", f"../local_test_feedback/{task}/log", '', '', '', 'tests.json'])

    shutil.rmtree('grader/', ignore_errors=True)

    os.remove("explain.json")
    os.remove("result")
    os.remove(f"{task}.sql")

    # read feedback
    feedback = None
    with open(f"local_test_feedback/{task}/feedback", "r") as f:
        feedback = f.read()

    shutil.rmtree(f'solutions/{task}', ignore_errors=True)
    
    shutil.copytree(f'local_test_feedback/{task}', f'solutions/{task}')

    shutil.rmtree('local_test_feedback', ignore_errors=True)

    return feedback
