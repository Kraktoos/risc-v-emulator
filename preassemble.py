import argparse
import utils.lib as lib
import utils.others as others

parser = argparse.ArgumentParser(description="Preassemble RISC-V assembly code (remove pseudoinstructions)")
parser.add_argument("filename", type=str, help="The file to preassemble")
parser.add_argument("--output", "-o", type=str, help="The output file to write to", default=None)

def preassemble(input_filename: str, output_filename: str | None):
  lines, commands = others.parse_input_file(input_filename)

  final_commands = []
  for command, i in enumerate(commands):
    t_inst, t_args = command
    if t_inst not in lib.pseudoinstructions:
      final_commands.append(lines[i])
    else:
      for pseudoinstruction in lib.pseudoinstructions[t_inst]:
        inst = pseudoinstruction["inst"]
        args = pseudoinstruction["args"]
        if len(t_args) != len(lib.pseudoinstructions_arguments[t_inst]):
          raise Exception(f"Instruction {inst} takes {len(lib.pseudoinstructions_arguments[t_inst])} arguments, got {len(t_args)}")
        final_commands.append(" ".join([inst] + [t_args[lib.pseudoinstructions_arguments[t_inst].index(x)] for x in args]))

  if output_filename is not None:
    open(output_filename, "w").write("\n".join(final_commands))
    
    print(f"Output written to {output_filename}\n")

if __name__ == "__main__":
  args = parser.parse_args()
  preassemble(args.filename, args.output)