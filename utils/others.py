import tabulate

def parse_input_file(filename: str):
  lines = [x.strip() for x in open(filename, "r").read().strip().splitlines() if x.strip() != ""]
  return (lines, [(x[0], [y.strip() for y in "".join(x[1:]).split(",")]) for x in (line.split() for line in lines)])

def print_table(headers: list[str], data: list[list[str]]):
  print(tabulate.tabulate(data, headers=headers, tablefmt="fancy_grid"))