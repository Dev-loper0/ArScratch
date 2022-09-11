#C:\Users\Fritz\AppData\Roaming\Sublime Text\Packages\User

import argparse
import compiler


def Info():
	print("ARScratch 1.0")
	print("Devloped by Cheriet Noureddine under MIT Licenses \n")

def start():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p","--path",help="source code file path")
	parser.add_argument("-c","--incode",help="compile inline code")
	args = parser.parse_args()

	if args.path:
		try:
			with open(args.path,"r") as f:
				return f.read()
		except Exception as e:
			print(e)
			exit(1)
	elif args.incode:
		return(args.incode)


if __name__ == "__main__":
	Info()
	code = start()
	if code:
		print(code + "\n")
		compiler.Compile(code)

	else:
		while True:
			code = str(input('>>> '))
			compiler.Compile(code + "\n")