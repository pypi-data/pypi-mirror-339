import rsa
import getpass
import os

keys_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'Keys')

with open(os.path.join(keys_path, 'priv_key.PEM'), mode='rb') as priv_key:
    privateKey = priv_key.read()
    privateKey = rsa.PrivateKey.load_pkcs1(privateKey)
with open(os.path.join(keys_path, 'pub_key.PEM'), mode='rb') as pub_key:
    publicKey = pub_key.read()
    publicKey = rsa.PublicKey.load_pkcs1(publicKey)

qv_usrname = str(input('Please enter QV username:'))
qv_pswd = getpass.getpass('Enter QV password')
qv = qv_usrname + '###' + qv_pswd
er_usrname = str(input('Please enter ER username:'))
er_pswd = getpass.getpass('Enter ER password')
er = er_usrname+ '###' + er_pswd

qv = rsa.encrypt(qv.encode('utf-8'), publicKey)
er = rsa.encrypt(er.encode('utf-8'), publicKey)

with open(os.path.join(keys_path, 'qv_login.txt'), mode='wb') as f:
    f.write(qv)
with open(os.path.join(keys_path, 'er_login.txt'), mode='wb') as f:
    f.write(er)