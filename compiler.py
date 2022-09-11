import string
from pprint import pprint

KeyWords = ["left","rigth","forward","backward","mission","endmission","loop","endloop","print"]

#FIXME 
class Error_Handler:
	TypeErr = None
	NotDefErr = None
	EndofErr = None



class Lexer:
	
	def __init__(self,code):
		self.tokens = []
		self.code = code

	def tokenize(self):
		current = 0
		while current < len(self.code) - 1:
			if self.code[current] == "\n":
				self.tokens.append({
					"type":"seprateur",
					"value":"NewLine"
					})
				current += 1

			elif self.code[current] == " ":
				current += 1

			elif self.code[current] == '"':
				token = ""
				current += 1
				while self.code[current] != '"':
					token += self.code[current]
					current += 1
				current += 1

				self.tokens.append({
					"type":"string",
					"value":token
					})

			elif self.code[current] in string.ascii_letters:
				token = ""
				while self.code[current] in string.ascii_letters:
					token += self.code[current]
					current += 1
				
				if token in KeyWords:
					self.tokens.append({
						"type":"key_word",
						"value":token
						})

				else:
					self.tokens.append({
						"type":"unknown_word",
						"value":token
						})

			elif self.code[current] in string.digits:
				token = ""
				while self.code[current] in string.digits:
					token += self.code[current]
					current += 1
					if current == len(self.code):
						break

				self.tokens.append({
					"type":"int",
					"value":token
					})

			elif self.code[current] in ['+','*','/','-']:
				self.tokens.append({
					"type":"math_op",
					"value":self.code[current]
					})
				current += 1

			elif self.code[current] in ['>','<','==','!=']: #FIXME == != Not parssed
				self.tokens.append({
					"type":"compare_op",
					"value":self.code[current]
					})
				current += 1

			elif self.code[current] == "=":
				self.tokens.append({
					"type":"eq",
					"value":self.code[current]
					})
				current += 1

			elif self.code[current] == "#":
				token = ""
				while self.code[current] != "\n":
					token += self.code[current]
					current += 1
					if current == len(self.code):
						break

				self.tokens.append({
					"type":"comment",
					"value":token
					})

		return self.tokens


class Parser:
	
	def __init__(self,tokens):
		self.tokens = tokens
		self.current = 0
		self.ast = {
			"type":"programe",
			"body":[]
		}
		self.int_left_arm = None
		self.parse()
		pprint(self.ast)

	def parse(self):
		while self.current < len(self.tokens):
			walk = self.walk()
			if  walk['type'] != None and walk['type'] != 'Seprateur':
				self.ast['body'].append(walk)

	def walk(self):
		if self.current < len(self.tokens):
			token = self.tokens[self.current]
			if token['type'] == "comment":
				self.current += 2
				return({
					"type":"Comment",
					"value":token['value']
					})

			elif token['type'] == "int":
				if self.current + 1 < len(self.tokens):
					if self.tokens[self.current + 1]['type'] == "math_op" or \
							self.tokens[self.current + 1]['type'] == "compare_op":
						self.int_left_arm = {
						"type":"Int",
						"value":token['value']
						}
						self.current += 1
						return({
							"type":None
						})

				self.current += 1
				return({
					"type":"Int",
					"value":token['value']
					})

			elif token['type'] == "string":
				self.current += 1
				return({
					"type":"String",
					"value":token['value']
					})

			elif token['type'] == "key_word":
				self.current += 1
				ret = {
					"type":None,
					"value":None
				}
				if token['value'] == 'mission':
					Node = {
					'type':'FunDef',
					'value':None,
					'params':[]
					}

					while ret["value"] != "endmission":
						ret = self.walk()
						if ret["type"] == "FunName":
							Node['value'] = ret['value']

						if ret["value"] != "endmission" and ret["type"] != "FunName" and ret["type"] != "Seprateur":
							Node['params'].append(ret)

				elif token['value'] == 'loop':
					Node = {
					'type':'LoopStart',
					'value':None,
					'params':[]
					}

					while ret["value"] != "endloop":
						ret = self.walk()
						if ret["type"] == "Int":
							Node['value'] = ret['value']

						if ret["value"] != "endloop" and ret["type"] != "FunName" and ret["type"] != "Seprateur":
							Node['params'].append(ret)

				else:
					Node = {
					'type':'Command',
					'value':token['value'],
					'params':[]
					}
					
					while ret["type"] != "Seprateur" and ret["type"] != "Math_Op":
						ret = self.walk()
						if ret["type"] != "Seprateur":
							Node['params'].append(ret)
				return Node

			elif token['type'] == "unknown_word":
				if self.current + 1 < len(self.tokens):
					if self.tokens[self.current + 1]['type'] == "math_op" or \
							self.tokens[self.current + 1]['type'] == "compare_op":
						self.int_left_arm = {
						"type":"CallExp",
						"value":token['value']
						}
						self.current += 1
						return({
							"type":None
						})

				if self.tokens[self.current - 1]["value"] == "mission":
					Node = {
						'type':'FunName',
						'value':token['value']
					}
					self.current += 1
					return Node

				else:
					Node = {
						'type':'Def',
						'left_arme':token['value'],
						'rigth_arme':[],
					}
					ret = {
						"type":None,
						"value":None
					}
					self.current += 1
					while ret["type"] != "Seprateur" and ret["type"] != "Math_Op":
						#pprint(ret)
						ret = self.walk()
						if ret["type"] != "Seprateur" and ret["type"] != "Eq" and ret["type"] != None:
								Node['rigth_arme'].append(ret)
					if len(Node['rigth_arme']) < 1:
						Node = {
							'type':'CallExp',
							'value':token['value']
						}
					return Node

			elif token['type'] == "eq":
				self.current += 1
				return({
					"type":"Eq",
					"value":token['value']
					})

			elif token['type'] == "compare_op":
				Node = {
						'type':'Compare_Op',
						'value':self.tokens[self.current]["value"],
						'left_arme':self.int_left_arm,
						'rigth_arme':[],
					}

				ret = {
						"type":None,
						"value":None
					}

				self.current += 1
				while ret["type"] != "Seprateur" and ret["type"] != "Compare_Op":
					ret = self.walk()
					if ret["type"] != "Seprateur" and ret["type"] != None:
						Node['rigth_arme'].append(ret)
				return Node

			elif token['type'] == "math_op":
				Node = {
						'type':'Math_Op',
						'value':self.tokens[self.current]["value"],
						'left_arme':self.int_left_arm,
						'rigth_arme':[],
					}
				#self.ast['body'].pop(self.current - 1)
				ret = {
						"type":None,
						"value":None
					}

				self.current += 1
				while ret["type"] != "Seprateur" and ret["type"] != "Math_Op":
					ret = self.walk()
					if ret["type"] != "Seprateur" and ret["type"] != None:
						Node['rigth_arme'].append(ret)
				return Node

			elif token['type'] == "seprateur":
				self.current += 1
				return({
					"type":"Seprateur",
					"value":token['value']
					})
		return({
			"type":"Seprateur"
				})






class Eval:
	def __init__(self,ast):
		pass


def Compile(code):
	tokens = Lexer(code).tokenize()
	ast = Parser(tokens)
	Eval(ast)
