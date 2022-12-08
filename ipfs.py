import ipfshttpclient

api = ipfshttpclient.connect()
res = api.add('Ipfs-logo.png')
print(res)

#api.cat(res['Hash'])
#QmRACojSdFuqnyyfQZ9Zgiz6zrVCUX1JRkYZyvRGu1MCzG