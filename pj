#!/usr/bin/env python3

import json
import os
import sys
import uuid



def is_slice_syntax(arg):
	if not ":" in arg: return False
	return all((ch in "0123456789:-") for ch in arg)

def apply_slice(arr, slice_str):
	try:
		parts = slice_str.split(':')
		slice_args = [int(p) if p else None for p in parts]
		while len(slice_args) < 3:
			slice_args.append(None)
		return arr[slice(*slice_args)]
	except Exception:
		return None


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

	current = jo
	for arg in rest:
		if type(current) is dict:
			match arg:
				case ":k" | ":keys": current = list(current.keys())
				case ":v" | ":values": current = list(current.values())
				case ":kv": current = [[k, current[k]] for k in current]
				case ":vk": current = [[current[k], k] for k in current]
				case _:
					if arg in current:
						current = current[arg]
					else:
						print(f"Unknown arg: '{arg}'"); return
		elif type(current) is list:
			match arg:
				case ":k" | ":keys": current = [i for i, x in enumerate(current)]
				case "--" | ":flat": current = [y for x in current for y in x]
				case ":id":
					for idx, obj in enumerate(current):
						obj['id'] = idx
				case ":uuid":
					for obj in current:
						obj['uuid'] = str(uuid.uuid4())
				case _:
					if is_slice_syntax(arg):
						current = apply_slice(current, arg)
						if not current:
							print(f"Slice failed: '{arg}'"); return 1
					elif arg.startswith("m:"):
						map_prop = arg[2:]
						current = [x[map_prop] for x in current]
					elif arg.isnumeric():
						n = int(arg)
						current = current[n]
					else:
						print(f"Unknown arg: '{arg}'"); return
		else:
			print(f"Unknown arg: '{arg}'"); return

	print(json.dumps(current, indent="\t"))


if __name__ == '__main__':
	main()
