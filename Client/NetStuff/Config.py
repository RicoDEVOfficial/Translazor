import json, os

# Load configuration from JSON into a dict `cfg`
_cfg_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(_cfg_path, 'r') as _f:
    cfg = json.load(_f)