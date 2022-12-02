import gnupg
from .hash import Hash
from ..env import UPLOAD_FOLDER, SIGNED_FOLDER, GNUPG_HOME_GARVIT

class Signature:
    # setup gnupg
    def __init__(self):
        self.documentspath = UPLOAD_FOLDER
        self.signaturepath = SIGNED_FOLDER
        self.gpg = gnupg.GPG(gnupghome=GNUPG_HOME_GARVIT)
        self.gpg.encoding = 'utf-8'

    # keyid = fingerprint of signer
    def sign(self, filename, password=None, email=None):
        # read message
        stream = open(self.documentspath + filename, 'rb')
        self.message = stream.read()
        self.message = Hash().hash(message=self.message)
        stream.close()

        # sign 
        output_path = self.signaturepath + filename + '.sig'
        self.signed_data = self.gpg.sign(self.message, output=output_path, keyid=email, passphrase=password)