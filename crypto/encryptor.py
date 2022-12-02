import gnupg
from ..env import UPLOAD_FOLDER, GNUPG_HOME_GARVIT

from key_generator import KeyGenerator

class Encryptor:
    # setup gnupg
    def __init__(self):
        self.documentspath = UPLOAD_FOLDER
        self.encryptpath = './encrypted/'
        self.gpg = gnupg.GPG(gnupghome=GNUPG_HOME_GARVIT)
        self.gpg.encoding = 'utf-8'

    # keyid = fingerprint of student
    def encrypt(self, filename, keyid=None):
        # read message
        stream = open(self.documentspath + filename, 'rb')

        # encrypted 
        output_path = self.encryptpath + filename + '.enc'
        self.encrypted_data = self.gpg.encrypt_file(stream, recipients=keyid, output=output_path, always_trust=True)

        print(self.encrypted_data.status)

        # close stream
        stream.close()