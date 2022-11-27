import gnupg
import os
from message.hash import Hash

class Decryptor:
    def __init__(self):
        dir = os.getcwd()
        self.documentspath = dir + '/documents/'
        self.encryptpath = dir + '/documents/encrypted/'
        self.decryptpath = dir + '/documents/decrypted/'
        self.gpg = gnupg.GPG(gnupghome='/home/kushal-joseph/.gnupg')
        self.gpg.encoding = 'utf-8'

    def decrypt(self, file, key_id=None):
        # read message
        filename = file.filename
        path_to_signature_file = self.encryptpath + filename + '.sig'
        signature_stream = open(path_to_signature_file, 'rb')
        self.message = signature_stream.read()

        path_to_file = self.documentspath + filename
        self.document_stream = open(path_to_file, 'rb')
        self.document = self.document_stream.read()

        # verify signature
        verified = self.gpg.verify(data=self.message)
        print(verified)
        print(vars(verified))
        if(verified):
            print("Verified Signature")
        else:
            print("Unverified Signature")
            return
        
        # verify that given hash == h(m)
        # first, we decrypt the signature to retrieve the data that was signed

        # if(not os.path.exists(self.decryptpath)):
        #     os.makedirs(self.decryptpath)
        # decrypted = self.gpg.decrypt(self.message, output=self.decryptpath + f'{filename}')
        # recevied_decrypted_hash = open(self.decryptpath + f'{filename}', 'rb').read()[:-1]
        
        # h = Hash()
        # calculated_hash = h.hash(open(f'./documents/{filename}', 'rb').read())

        # print(f"The calculated hash is: {calculated_hash}")
        # print(f"The received hash is: {recevied_decrypted_hash}")
        # if(calculated_hash == recevied_decrypted_hash):
        #     print("All verified, data is authentic")
        # else:
        #     print("Data is not authentic!")
    
        # retrieve m. (Actually we needed to decrypt m, but there is not enc-dec here)