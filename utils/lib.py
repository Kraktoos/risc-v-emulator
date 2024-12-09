def to_bin(num, bits=8):
  # if num < 0:
  #   print(num, 2**bits + num)
  #   print(format(2**bits + num, f"0{bits}b"))
  #   return format(2**bits + num, f"0{bits}b")
  # return format(num, f"0{bits}b")
  return format(num, f"0{bits}b")

def to_dec(binary, max_bits=8):
  # if binary.startswith("1"):
  #   return int(binary, 2) - 2**max_bits
  # return int(binary, 2) & (2**max_bits - 1)
  return int(binary, 2)

def to_hex(num, bits):
  return format(num, f"0{bits}x")

instructions = {
  # Arithmetic
  "add": {"FMT": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000"},
  "addi": {"FMT": "I", "opcode": "0010011", "funct3": "000", "funct7": None},
  "sub": {"FMT": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000"},
  "mul": {"FMT": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000001"},
  "div": {"FMT": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000001"},
  "rem": {"FMT": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000001"},
  # Logic
  "and": {"FMT": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000"},
  "xor": {"FMT": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000"},
  "or": {"FMT": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000"},
  # Memory
  "lw": {"FMT": "I", "opcode": "0000011", "funct3": "010", "funct7": None},
  "lh": {"FMT": "I", "opcode": "0000011", "funct3": "001", "funct7": None},
  "lb": {"FMT": "I", "opcode": "0000011", "funct3": "000", "funct7": None},
  "sw": {"FMT": "S", "opcode": "0100011", "funct3": "010", "funct7": None},
  "sh": {"FMT": "S", "opcode": "0100011", "funct3": "001", "funct7": None},
  "sb": {"FMT": "S", "opcode": "0100011", "funct3": "000", "funct7": None},
  # Control
  "beq": {"FMT": "B", "opcode": "1100011", "funct3": "000", "funct7": None},
  "bne": {"FMT": "B", "opcode": "1100011", "funct3": "001", "funct7": None}
}

arguments = {
  "R": ["rd", "rs1", "rs2"],
  "I": ["rd", "rs1", "imm"],
  "S": ["rs1", "rs2", "imm"],
  "B": ["rs1", "rs2", "imm"]
}

bit_formats = {
  "funct7": 7,
  "rs2": 5,
  "rs1": 5,
  "funct3": 3,
  "rd": 5,
  "opcode": 7,
  "imm": 12
}

instruction_formats = {
  "R": ["funct7", "rs2", "rs1", "funct3", "rd", "opcode"],
  "I": ["imm-11:0", "rs1", "funct3", "rd", "opcode"],
  "S": ["imm-11:5", "rs2", "rs1", "funct3", "imm-4:0", "opcode"],
  "B": ["imm-11:11", "imm-9:4", "rs2", "rs1", "funct3", "imm-3:0", "imm-10:10", "opcode"]
}

pseudoinstructions = {
  "mv": [
    {"inst": "addi", "args": ["rd", "rs1", "0"]}
  ],
  "neg": [
    {"inst": "sub", "args": ["rd", "x0", "rs1"]}
  ],
}

pseudoinstructions_arguments = {
  "mv": ["rd", "rs1"],
  "neg": ["rd", "rs1"]
}