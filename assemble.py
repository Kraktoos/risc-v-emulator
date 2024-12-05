import argparse
import utils.lib as lib
import utils.others as others

parser = argparse.ArgumentParser(description="Assemble RISC-V assembly code into machine code")
parser.add_argument("filename", type=str, help="The file to assemble")
parser.add_argument("--output", "-o", type=str, help="The output file to write to", default=None)
parser.add_argument("--verbose", "-v", action="store_true", help="Print the assembled code", default=True)

def assemble(input_filename: str, output_filename: str | None, verbose: bool):
  lines, commands = others.parse_input_file(input_filename)

  final_commands = []
  for command in commands:
    t_inst, t_args = command
    if t_inst not in lib.instructions:
      raise Exception(f"Instruction {inst} not found")
    inst = lib.instructions[t_inst]
    if len(t_args) != len(lib.arguments[inst["FMT"]]):
      raise Exception(f"Instruction {inst} takes {len(lib.arguments[inst['FMT']])} arguments, got {len(t_args)}")
    args = {lib.arguments[inst["FMT"]][i]: int(t_args[i].replace("x", "")) for i in range(len(t_args))}
    
    formats = lib.instruction_formats[inst["FMT"]]
    final_command = ""
    for f in formats:
      if f in inst:
        # is something like an opcode or funct3
        final_command += inst[f]
      else:
        # is an argument
        if "-" in f:
          # is a range (ex: imm-11:0)
          instruction, _range = f.split("-")
          end, start = map(int, _range.split(":"))
          binary_num = lib.to_bin(int(args[instruction]), lib.bit_formats[instruction])
          final_command += binary_num[start:end+1]
        else:
          # is a normal argument (ex: rs1, rd, etc)
          final_command += lib.to_bin(args[f], lib.bit_formats[f])
    final_commands.append(final_command)

  if output_filename is not None:
    open(output_filename, "w").write("".join(final_commands))
    print(f"Output binary written to {output_filename}\n")

  if verbose:
    others.print_table(["Instruction", "Command", "Binary", "Hex"], [[commands[i][0], lines[i], final_commands[i], "0x" + lib.to_hex(int(final_commands[i], 2), 8)] for i in range(len(commands))])


if __name__ == "__main__":
  args = parser.parse_args()
  assemble(args.filename, args.output, args.verbose)