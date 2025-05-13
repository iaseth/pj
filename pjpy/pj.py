#!/usr/bin/env python3

import json
import os
import sys

from pypj.manipulation import manipulate_json



def main():
	args = sys.argv[1:]
	if len(args) == 0:
		print(f"Usage:\n\tpj <json_path> args"); return

	json_path, *rest = args

	if not os.path.isfile(json_path):
		print(f"Not found: {json_path}"); return 1

	try:
		with open(json_path) as f:
			jo = json.load(f)
	except Exception as e:
		print(f"Parsing: '{json_path}'")
		print(f"\tError: {e}"); return

	manipulate_json(jo, rest)


if __name__ == '__main__':
	main()
