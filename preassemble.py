import argparse
import utils.lib as lib
import utils.others as others

parser = argparse.ArgumentParser(description="Preassemble RISC-V assembly code (remove pseudoinstructions)")
parser.add_argument("filename", type=str, help="The file to preassemble")
parser.add_argument("--output", "-o", type=str, help="The output file to write to", default=None)

def preassemble(input_filename: str, output_filename: str | None):
  lines, commands = others.parse_input_file(input_filename)

  final_commands = []
  for i, command in enumerate(commands):
    t_inst, t_args = command
    if t_inst not in lib.pseudoinstructions:
      final_commands.append(lines[i])
    else:
      for pseudoinstruction in lib.pseudoinstructions[t_inst]:
        new_inst = pseudoinstruction["inst"]
        current_arguments = lib.pseudoinstructions_arguments[t_inst]
        new_arguments = pseudoinstruction["args"]

        updated_args = []
        for arg in new_arguments:
          if arg in current_arguments:
            updated_args.append(t_args[current_arguments.index(arg)])
          else:
            updated_args.append(arg)

        final_commands.append(new_inst + " " + ", ".join(updated_args))

  if output_filename is not None:
    open(output_filename, "w").write("\n".join(final_commands))
    
    print(f"Output written to {output_filename}\n")

if __name__ == "__main__":
  args = parser.parse_args()
  preassemble(args.filename, args.output)