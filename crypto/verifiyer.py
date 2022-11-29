# verifyer class
import gnupg
from ..env import SIGNED_FOLDER

class Verifyer:
    def __init__(self):
        self.signedpath = SIGNED_FOLDER
        self.gpg = gnupg.GPG(gnupghome='/home/garvitsingh/.gnupg')
        self.gpg.encoding = 'utf-8'

    def decrypt(self, filename, keyid=None):
        # read message from encrypted file
        stream = open(self.signedpath + filename + '.sig', 'rb')
        self.message = stream.read()
        stream.close()

        # verify signature of person
        verified = self.gpg.verify(data=self.message)
        if (verified and verified.fingerprint == keyid):
            # retreive message and return the hash
            return self.gpg.decrypt(self.message)
        else:
            return None