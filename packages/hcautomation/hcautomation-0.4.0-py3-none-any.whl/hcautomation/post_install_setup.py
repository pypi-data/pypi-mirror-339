import os
import getpass
import rsa
import shutil
import importlib.resources

print('*50', 'Initilizing post install script', '*50')

def create_folder_structure():
    print('Generating required folder structure')
    base_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI')
    keys_dir = os.path.join(base_path, 'Keys')
    try:
        os.makedirs(keys_dir)
        print('Keys directory created')
    except:
        pass

    target_dir = os.path.join('C:', os.sep, 'Users', getpass.getuser(),'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'Keys')
    for filename in ["pub_key.PEM", "priv_key.PEM"]:
        dest_path = os.path.join(target_dir, filename)
        if os.path.exists(dest_path):
            print(f"{filename} already exists at destination. Skipping.")
            continue
        with importlib.resources.path("hcautomation", filename) as src_path:
            shutil.copy(src_path, dest_path)
            print(f"Copied {filename} to {dest_path}")

    base_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI')
    os.chdir(base_path)
    if not os.path.exists(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'ipynb_metadata.xml')):
        print('Writing empty metadata file')
        with open(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'ipynb_metadata.xml'), mode='w+') as f:
            f.write('')
    if not os.path.exists(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'API.log')):
        print('Writing empty LOG file')
        with open(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'API.log'), mode='w+') as f:
            f.write('')

    
def gen_login():

    keys_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'Keys')
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

def post_install():
    create_folder_structure()
    gen_login()

if __name__ == "__main__":
    post_install()