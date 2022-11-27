import hashlib

class Hash:
    def __init__(self):
        pass
    
    def hash(self, message):
        sha = hashlib.sha256()
        sha.update(message)
        return sha.hexdigest()