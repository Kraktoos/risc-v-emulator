import argparse
from utils.lib import to_dec, to_bin
import utils.others as others
import disassemble

parser = argparse.ArgumentParser(description="Run RISC-V assembly code")
parser.add_argument("filename", type=str, help="The (binary) file to run")
parser.add_argument("--verbose", "-v", action="store_true", help="Print the executed instructions", default=True)

if __name__ == "__main__":
  args = parser.parse_args()

  lines, commands = others.parse_input("\n".join(disassemble.disassemble(args.filename)))
  registers = {f"x{i}": "00000000" for i in range(32)}
  memory = ["00000000" for _ in range(1024)]
  program_counter = 0

  def routine_actions():
    global program_counter, registers, memory
    # if args.verbose:
    others.print_table(["PC", "Command"], [[program_counter, commands[program_counter]]])
    program_counter += 1
    registers["x0"] = "00000000"

  while program_counter < len(commands):
    command = commands[program_counter]
    routine_actions()
    inst, args = command

    match inst:
      case "add":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) + to_dec(registers[rs2]))
      case "addi":
        rd, rs1, imm = args
        registers[rd] = to_bin(to_dec(registers[rs1]) + int(imm))
      case "sub":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) - to_dec(registers[rs2]))
      case "mul":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) * to_dec(registers[rs2]))
      case "div":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) // to_dec(registers[rs2]))
      case "rem":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) % to_dec(registers[rs2]))
      case "and":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) & to_dec(registers[rs2]))
      case "xor":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) ^ to_dec(registers[rs2]))
      case "or":
        rd, rs1, rs2 = args
        registers[rd] = to_bin(to_dec(registers[rs1]) | to_dec(registers[rs2]))
      case "lw":
        rd, rs1, imm = args
        read_from = to_dec(registers[rs1]) + int(imm)
        registers[rd] = memory[read_from]
      case "sw":
        rs1, rs2, imm = args
        write_to = to_dec(registers[rs1]) + int(imm)
        memory[write_to] = registers[rs2]
      # case "beq":
      #   rs1, rs2, imm = args
      #   if registers[rs1] == registers[rs2]:
      #     program_counter += int(imm) // 2 - 1
      # case "bne":
      #   rs1, rs2, imm = args
      #   if registers[rs1] != registers[rs2]:
      #     program_counter += int(imm) // 2 - 1
      case _:
        raise Exception(f"Instruction {inst} not found")
  
  others.print_table(["Non-0 Memory Address", "Value"], [[i, to_dec(memory[i])] for i in range(1024) if memory[i] != "00000000"])
  others.print_table(["Register", "Value"], [[reg, to_dec(registers[reg])] for reg in registers])