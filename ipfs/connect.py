import ipfshttpclient

class IPFS():
    def __init__(self):
        self.filepath = './documents/'
        # Share TCP connections using a context manager until the client session is closed
        with ipfshttpclient.connect(session=True) as self._client:
            print('Client for IPFS: ', self._client)
            print('Client ID: ', self._client.id())

    def upload(self, filename):
        # upload on ipfs
        content = self._client.add(self.filepath+filename)
        print(content)

        # get hash and return to store in mongodb
        hash = content['hash']
        return 'Uploaded!'

    def download(self, hash):
        # download from ipfs 
        getfile = self._client.cat(hash)
        print(getfile)

        # store it in file and send for download
        return 'Downloaded!'

    def close(self):    # call this when done
        self._client.close()


if __name__ == "__main__":
    obj = IPFS()
    obj.upload('abc.txt')
    