import parser
import utils

utils.IS_DEBUG_MODE = True

parser.init()

with open("INST.INS", "rb") as f:
	parser.is_valid_ins_file(f)
	parser.parse_insts(f)
	parser.generate_insts_csv_file(f)
