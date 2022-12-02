import gnupg
from ..env import GNUPG_HOME_GARVIT

class KeyGenerator:
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome=GNUPG_HOME_GARVIT)
        self.gpg.encoding = 'utf-8'

    def generate_key(self, name, email, secretkey, comment='#'):
        # find key associated with email
        list_of_keys = self.listing_key()
        for key in list_of_keys:
            if(name in str(key['uids'][0]) and email in str(key['uids'][0])):
                ######################### delete if expired key #############################
                return key['fingerprint']
        
        # create a new key otherwise
        self.input_data = self.gpg.gen_key_input(
            key_type="RSA", 
            key_length=1024,
            name_real=name,
            name_email=email,
            name_comment=comment,
            key_usage='sign',
            expire_date="1y",
            passphrase=secretkey
        )
        self.key = self.gpg.gen_key(self.input_data)

        list_of_keys = self.listing_key()
        for key in list_of_keys:
            if(name in str(key['uids'][0]) and email in str(key['uids'][0])):
                return key['fingerprint']

    def export_key(self, keyid, pwd=None, private=False):
        if private:
            # passphrase has to be provided while exporting secret key
            return self.gpg.export_keys(keyid, private, passphrase=pwd)
        else:
            # no need for passphrase
            return self.gpg.export_keys(keyid, private)

    def import_key(self, filename):
        return self.gpg.import_keys_file('./publickey/'+filename)

    def listing_key(self, private=False):
        return self.gpg.list_keys(private)
        
    def delete_key(self, finger_print=None):
        self.gpg.delete_keys(fingerprints=finger_print)