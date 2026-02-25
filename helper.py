import datetime
from typing import Any

def serialize(obj: Any):
	"""Convert datetime/tzinfo and dict/list recursively to JSON-safe values."""
	if isinstance(obj, dict):
		return {k: serialize(v) for k, v in obj.items()}
	if isinstance(obj, (list, tuple)):
		return [serialize(v) for v in obj]
	if isinstance(obj, (datetime.datetime, datetime.date, datetime.time, datetime.tzinfo)):
		return str(obj)
	return obj