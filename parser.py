from inst import Inst
from utils import *

"""
主要的操作模块
"""

# 保存当前已解析的指令
insts = []

# 操作数的编码映射
op_num_map = {
	b'\x00': '',
	b'\x01': 'A',
	b'\x02': 'R?',
	b'\x03': '@R?',
	b'\x04': '#II',
	b'\x05': 'MM'
}


def init():
	"""初始化本模块状态"""
	insts.clear()


def is_valid_ins_file(f):
	"""判断是否为合法的 .INS 文件"""

	# FIXME:当前仅跳过文件前面的固定部分
	f.seek(0x75)
	pass


def parse_insts(f):
	"""
		从文件中解析出所有的指令，生成 Inst 对象并加入到 insts 列表中
		假设 ins 文件中指令系统部分不会出现 \xff，故以此为循环结束条件
	"""
	tmp_data = handle_00_byte(f)
	log(f"开始解析 Inst 文件，当前文件指针的位置为 {f.tell()}")
	while tmp_data != b'\xff':
		try:
			mnemonic_len = read(f)[0]
			tmp_mnemonic = ''.join([
				read(f).decode('ascii') for _ in range(mnemonic_len)
			])
			tmp_addr = read(f)[0]
			op_num1 = op_num_map[read(f)]
			op_num2 = op_num_map[read(f)]
			tmp_inst = Inst(tmp_mnemonic, tmp_addr, op_num1, op_num2)

			log(f"解析出指令 {tmp_inst}")
			insts.append(tmp_inst)
			handle_int_inst(f, tmp_mnemonic)
			tmp_data = handle_00_byte(f)
		except Exception as err:
			error(f"解析失败，原因 {err}")
	log("Inst 文件解析结束")


def parse_upros(f):
	"""从文件中解析出所有的微指令，并 4 个一组送给 insts 的 Inst"""
	pass


def generate_insts_csv_file(fp):
	with open(fp.name + ".csv", 'w') as f:
		f.write(
			"助记符,机器码1,机器码2,指令说明\n" +
			"_FATCH_,000000xx 00-03,," +
			"实验机占用，不可修改。复位后，所有寄存器清0，首先执行_FATCH_指令取指。\n"
		)
		for inst in insts:
			f.write(",".join([
				inst.get_mnemonic(),
				inst.get_addr_str(),
				inst.get_op_num1(),
				inst.get_comment()
			]))
	log("INS.CSV 文件写入完成")


def generate_upros_csv_file():
	"""生成 微程序 的 csv 文件"""
	pass


def handle_int_inst(f, mnemonic):
	"""处理模拟器自动生成的 _INT_ 指令"""
	if mnemonic == "_INT_":
		read(f, 60)
