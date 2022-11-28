import gnupg

class Signature:
    # setup gnupg
    def __init__(self):
        self.documentspath = './uploads/'
        self.signaturepath = './signed/'
        self.gpg = gnupg.GPG(gnupghome='/home/garvitsingh/.gnupg')
        self.gpg.encoding = 'utf-8'

    # keyid = fingerprint of signer
    def sign(self, filename, keyid=None):
        # read message
        stream = open(self.documentspath + filename, 'rb')
        self.message = stream.read()
        stream.close()

        # sign 
        output_path = self.signaturepath + filename + '.sig'
        self.signed_data = self.gpg.sign(self.message, output=output_path, keyid=keyid)