import json
import uuid

from tabulate import tabulate

from .utils import is_slice_syntax, apply_slice



def manipulate_json(jo, args):
	current = jo
	for arg in args:
		if type(current) is dict:
			match arg:
				case "--table": print(tabulate(current['data'], headers=current['headers']))
				case ":k" | ":keys": current = list(current.keys())
				case ":v" | ":values": current = list(current.values())
				case ":kv": current = [[k, current[k]] for k in current]
				case ":vk": current = [[current[k], k] for k in current]
				case _:
					if arg in current:
						current = current[arg]
					else:
						print(f"Key not found arg: '{arg}' {list(current.keys())}"); return
		elif type(current) is list:
			match arg:
				case "-j": print(json.dumps(current))
				case "--json": print(json.dumps(current, indent="\t"))
				case ":k" | ":keys": current = [i for i, x in enumerate(current)]
				case "--" | ":flat": current = [y for x in current for y in x]
				case ":id":
					for idx, obj in enumerate(current, start=1):
						obj['id'] = idx
				case ":index":
					for idx, obj in enumerate(current):
						obj['index'] = idx
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
						try:
							n = int(arg)
							current = current[n]
						except Exception as e:
							print(f"Invalid index: '{arg}' (array has {len(current)} elements)")
							return
					else:
						print(f"Unknown arg: '{arg}'"); return
		else:
			print(f"Unknown arg: '{arg}'"); return

