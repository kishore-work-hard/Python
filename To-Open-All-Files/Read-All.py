import os

path = "./path/is/here"
os.chdir(path)

for file in os.listdir():

	if file.endswith(".jpg"):
		file_path = f"{path}\{file}"
		print(file_path)
