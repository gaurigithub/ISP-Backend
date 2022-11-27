import gnupg
import os
from message.hash import Hash

class Encryptor:
    def __init__(self):
        dir = os.getcwd()
        self.documentspath = dir + '/documents/'
        self.encryptpath = dir + '/documents/encrypted/'
        self.gpg = gnupg.GPG(gnupghome='/home/kushal-joseph/.gnupg')
        self.gpg.encoding = 'utf-8'

    def encrypt(self, filename, key_id, passphrase):
        # read message
        print(self.documentspath)
        
        stream = open(self.documentspath + filename.filename, 'rb')
        self.message = stream.read()

        # calculate hash
        self.hash = Hash().hash(self.message)
        print(self.hash)
        stream.close()

        # sign the hashed value
        output_path = self.encryptpath + filename.filename + '.sig'
        print(output_path)
        if(not os.path.exists(self.encryptpath)):
            os.makedirs(self.encryptpath)
        
        self.gpg.sign(self.hash, output=output_path, keyid=key_id, passphrase=passphrase)

        # now, we (simulate) transfer of [FILE + signed(hash(FILE))] over an unsafe network
        # note that, normally we would transfer: 
        #                             [encrypt(FILE) + signed(hash(FILE))]
        # but in this simplistic scenario, we are not encrypting the file


        
