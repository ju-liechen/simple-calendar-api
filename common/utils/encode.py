from uuid import UUID
import json
import base64


class JSONEncoderWithUUID(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


def dict_to_base64(d):
    return base64.b64encode(json.dumps(d, cls=JSONEncoderWithUUID).encode()).decode()


def base64_to_dict(s):
    return json.loads(base64.b64decode(s.encode()).decode())
