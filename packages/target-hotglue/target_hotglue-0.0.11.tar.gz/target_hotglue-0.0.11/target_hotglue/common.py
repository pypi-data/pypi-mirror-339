from datetime import datetime
from json import JSONEncoder
from typing import Any

class HGJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()

        return super().default(o)
