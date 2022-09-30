import os
dir = '/home/user/doc'
if os.path.isdir(dir) and os.path.exists(dir):
    if len(os.listdir('/home/user/doc')) == 0:
        print("Directory is empty")
    else:
        print("Directory is not empty")
else:
    print("Directory does not exist")
