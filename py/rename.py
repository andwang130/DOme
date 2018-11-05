import os
path = './'
count = 1
for file in os.listdir(path):
    print(file)
    os.rename(os.path.join(path,file),os.path.join(path,file.replace(";","&")))