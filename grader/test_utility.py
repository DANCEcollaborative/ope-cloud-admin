import json
from cryptography.fernet import Fernet

RESULT_ENCRYPT_KEY = b'eGu_wSKEk8KVomhP7snm_T8QHenYCWm9pLFLqtM43l0='
TASK_ENCRYPT_KEY = "8D8C368627985BE"
fernet = Fernet(RESULT_ENCRYPT_KEY)

def write_result(result, filename):
	"""
	Write the result JSON
	"""
	result = json.dumps(result)
	with open(filename, "w") as f:
		f.write(result)