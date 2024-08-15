import os

if not os.path.exists('conf.env'):
    with open('conf.env', 'w') as f:
        f.write("token = ''")