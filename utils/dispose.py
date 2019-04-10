import re
from setting import RE_TOKEN, RE_TYPE, RE_NAME


class AmazonDispose:
    def __init__(self, content):
        self.content = content

    def get_token(self):
        token = re.search(RE_TOKEN, self.content, re.M)
        if not token:
            return None
        return token.group(1)

    def get_type(self):
        types = re.search(RE_TYPE, self.content, re.M)
        if not types:
            return None
        return types.group(1)

    def get_name(self):
        name = re.search(RE_NAME, self.content, re.M)
        if not name:
            return None
        return name.group(1)
