import argparse
import utils.lib as lib
import utils.others as others

parser = argparse.ArgumentParser(description="Run RISC-V assembly code")
parser.add_argument("filename", type=str, help="The (binary) file to run")
parser.add_argument("--verbose", "-v", action="store_true", help="Print the executed instructions", default=True)

if __name__ == "__main__":
  args = parser.parse_args()
  lines, commands = others.parse_input_file(args.filename)

  registers = {f"x{i}": 0 for i in range(32)}
  memory = {}