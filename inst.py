class Inst:
	"""
	指令对象
	"""

	def __init__(self, op, addr, num1='', num2=''):
		self.__op = op
		self.__addr = addr
		self.__num1 = num1
		self.__num2 = num2
		self.upros = []
		pass

	def get_mnemonic(self):
		"""获取助记符"""
		return self.__str__()

	def get_addr_str(self):
		"""获取地址的字符串形式"""
		ret_addr = bin(self.__addr)[2:].rjust(8, '0')[:-2] + 'xx'
		return f"{ret_addr} {hex(self.__addr)[2:]}-{hex(self.__addr+4)[2:]}"

	def get_op_num1(self):
		"""获取操作码1"""
		return self.__num1

	def get_op_num2(self):
		"""获取操作码2"""
		return self.__num2

	def get_comment(self):
		"""获取指令注释"""
		if self.__op != "_INT_":
			return " \n"
		else:
			return "实验机占用，不可修改。进入中断时，实验机硬件产生 _INT_ 指令。\n"

	def __str__(self):
		return f"{self.__op} {self.__num1}，{self.__num2}"
		pass
	pass
