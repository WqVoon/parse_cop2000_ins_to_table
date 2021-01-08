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
	log(f"开始解析指令部分，当前文件指针的位置为 {f.tell()}")
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
	log("指令部分解析结束")


def parse_upros(f):
	"""从文件中解析出微指令，并 4 个一组送给 insts 的 Inst"""
	# TODO: 处理 _INT_ 的微指令
	read(f, 3)
	log(f"开始解析微程序部分，当前文件指针的位置为 {f.tell()}")
	for inst in insts:
		inst.add_one_uinst(read(f, 4))
		inst.add_one_uinst(read(f, 4))
		inst.add_one_uinst(read(f, 4))
		inst.add_one_uinst(read(f, 4))
	log("微程序部分解析结束")


def generate_insts_csv_file(fp):
	filename = fp.name + ".inst.csv"
	log(f"开始写入 {filename} 文件")
	with open(filename, 'w') as f:
		f.write(
			"助记符,机器码1,机器码2,指令说明\n" +
			"_FATCH_,000000xx 00-03,," +
			"实验机占用，不可修改。复位后，所有寄存器清0，首先执行_FATCH_指令取指。\n"
		)
		for inst in insts:
			log(f"写入了 {inst} 指令")
			f.write(",".join([
				inst.get_mnemonic(),
				inst.get_mache_code1(),
				inst.get_mache_code2(),
				inst.get_comment()
			]))
	log(f"{filename} 文件写入完成")


def generate_upros_csv_file(fp):
	"""生成 微程序 的 csv 文件"""
	# TODO: 处理 _FATCH_ 的微指令
	filename = fp.name + ".upro.csv"
	log(f"开始写入 {filename} 文件")
	with open(filename, 'w') as f:
		f.write(
			"助记符,状态,微地址,微程序,数据输出,数据打入,地址输出,运算器,移位控制,uPC,PC\n" +
			"_FATCH_,T0,00,CBFFFF,浮空,指令寄存器IR,PC输出,A输出,,写入,+1\n" +
			",,01,FFFFFF,浮空,,浮空,A输出,,+1,\n" +
			",,01,FFFFFF,浮空,,浮空,A输出,,+1,\n" +
			",,01,FFFFFF,浮空,,浮空,A输出,,+1,\n"
		)
	log(f"{filename} 文件写入完成")
	pass


def handle_int_inst(f, mnemonic):
	"""处理模拟器自动生成的 _INT_ 指令"""
	if mnemonic == "_INT_":
		read(f, 60)
