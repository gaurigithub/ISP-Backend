import gnupg

from key_generator import KeyGenerator

class Encryptor:
    # setup gnupg
    def __init__(self):
        self.documentspath = './uploads/'
        self.encryptpath = './encrypted/'
        self.gpg = gnupg.GPG(gnupghome='/home/garvitsingh/.gnupg')
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

if __name__ == "__main__":

    kg = KeyGenerator()
    print(kg.listing_key(True))

    enc = Encryptor()
    enc.encrypt(filename='test.txt', keyid='687909CED4F1E1882FC84221C1D07F3645328DDB')