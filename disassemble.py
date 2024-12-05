import argparse
import utils.lib as lib
import utils.others as others

parser = argparse.ArgumentParser(description="Disassemble RISC-V machine code into assembly")
parser.add_argument("filename", type=str, help="The binary file to disassemble")
parser.add_argument("--output", "-o", type=str, help="The output file to write to", default=None)
parser.add_argument("--verbose", "-v", action="store_true", help="Print the disassembled code", default=True)

def disassemble(input_filename: str, output_filename: str | None, verbose: bool):
  whole_file = open(input_filename, "r").read().strip()
  binary_instructions = [whole_file[i:i + 32] for i in range(0, len(whole_file), 32)] # split into 32-bit instructions

  disassembled_instructions = []

  for binary_instruction in binary_instructions:
    instruction_decoded = None

    # is there a matching command?
    for inst_name, inst_details in lib.instructions.items():
      inst_format = inst_details["FMT"]
      formats = lib.instruction_formats[inst_format]
      args = {}
      index = 0
      match = True

      # try to decode each field in the format
      for f in formats:
        if f in inst_details:
          # is something like an opcode or funct3
          length = len(inst_details[f])
          if binary_instruction[index:index + length] != inst_details[f]:
            match = False
            break
          index += length
        else:
          # is an argument/variable
          if "-" in f:
            # extract a range
            instruction, _range = f.split("-")
            end, start = map(int, _range.split(":"))
            length = end - start + 1
            args[instruction] = lib.to_dec(binary_instruction[index:index + length], lib.bit_formats[instruction])
            index += length
          else:
            # extract a normal argument
            length = lib.bit_formats[f]
            args[f] = lib.to_dec(binary_instruction[index:index + length], lib.bit_formats[f])
            index += length

      if match:
        instruction_args = [f"x{args[arg]}" if arg in args and arg[0] == "r" else args[arg] for arg in lib.arguments[inst_format]]
        instruction_decoded = f"{inst_name} " + ", ".join(map(str, instruction_args))
        break

    if not instruction_decoded:
      raise Exception(f"Failed to decode binary instruction: {binary_instruction}")

    disassembled_instructions.append(instruction_decoded)

  if output_filename is not None:
    open(output_filename, "w").write("\n".join(disassembled_instructions))
    print(f"Disassembled instructions written to {output_filename}\n")

  if verbose:
    others.print_table(["Binary", "Hex", "Command"], [[binary_instructions[i], "0x" + lib.to_hex(int(binary_instructions[i], 2), 8), disassembled_instructions[i]] for i in range(len(binary_instructions))])

if __name__ == "__main__":
  args = parser.parse_args()
  disassemble(args.filename, args.output, args.verbose)