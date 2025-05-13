


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

