from sys import argv
import parser
import utils

utils.IS_DEBUG_MODE = True

try:
	filename = argv[1]
except IndexError:
	filename = input("请输入 *.INS 文件的路径:")

parser.init()
with open(filename, "rb") as f:
	parser.is_valid_ins_file(f)
	parser.parse_insts(f)
	parser.generate_insts_csv_file(f)
	parser.parse_upros(f)
	parser.generate_upros_csv_file(f)
