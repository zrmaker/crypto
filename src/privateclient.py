import gdax
import numpy as np
from array import *
import json


auth_client = gdax.AuthenticatedClient()
data=json.dumps(auth_client.get_accounts())
data2=json.loads(data)
print('\n')
#print(data2)

ava=np.zeros((4),'f')
for i in range(4):
    ava[i]=data2[i]["available"]
print(ava)



#exit(0)