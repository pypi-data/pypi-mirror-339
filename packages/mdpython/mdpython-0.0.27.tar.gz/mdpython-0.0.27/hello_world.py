from mdpython.netutils import port
import json

print(json.dumps(port.get_port_details([7679,7680]),indent=2))
