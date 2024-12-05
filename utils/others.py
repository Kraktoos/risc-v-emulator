import tabulate

def parse_input_file(filename: str):
  return parse_input(open(filename, "r").read())

def parse_input(input: str):
  lines = [x.strip() for x in input.strip().splitlines() if x.strip() != ""]
  return (lines, [(x[0], [y.strip() for y in "".join(x[1:]).split(",")]) for x in (line.split() for line in lines)])

def split_binary(binary: str, length: int):
  return [binary[i:i + length] for i in range(0, len(binary), length)]

def print_table(headers: list[str], data: list[list[str]]):
  print(tabulate.tabulate(data, headers=headers, tablefmt="fancy_grid"))