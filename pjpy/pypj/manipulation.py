import json

from .utils import apply_slice



def manipulate_json(jo, args):
	current = jo
	for arg in args:
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

