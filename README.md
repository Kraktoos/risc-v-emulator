# RISC-V Emulator (WIP)

## Description
This is a simple RISC-V emulator that can preassemble, assemble, disassemble and ~~run~~ *(soon?)* a subset of RISC-V instructions.

## Supported Instructions
- Arithmetic: `add`, `addi`, `sub`, `mul`, `div`, `rem`
- Logic: `and`, `xor`, `or`
- Memory: `lw`, `lh`, `lb`, `sw`, `sh`, `sb`
- Control: `beq`, `bne`
- Pseudo Instructions: `mv`, `neg`

## How to setup
1. Clone the repository
2. Install the packages in `requirements.txt`

## Example Usage

### Assembling

#### Prerequisites
`program/main.s`
```
addi x5, x0, 101
addi x6, x0, 202
div x5, x6, x7
beq x0, x0, 0
```

#### Command
```bash
python assemble.py program/main.s -o program/a.out
```

#### Output
```
Output binary written to program/a.out

╒═══════════════╤══════════════════╤══════════════════════════════════╤════════════╕
│ Instruction   │ Command          │                           Binary │ Hex        │
╞═══════════════╪══════════════════╪══════════════════════════════════╪════════════╡
│ addi          │ addi x5, x0, 101 │ 00000110010100000000001010010011 │ 0x06500293 │
├───────────────┼──────────────────┼──────────────────────────────────┼────────────┤
│ addi          │ addi x6, x0, 202 │ 00001100101000000000001100010011 │ 0x0ca00313 │
├───────────────┼──────────────────┼──────────────────────────────────┼────────────┤
│ div           │ div x5, x6, x7   │ 00000010011100110100001010110011 │ 0x027342b3 │
├───────────────┼──────────────────┼──────────────────────────────────┼────────────┤
│ beq           │ beq x0, x0, 0    │ 00000000000000000000000001100011 │ 0x00000063 │
╘═══════════════╧══════════════════╧══════════════════════════════════╧════════════╛
```

`program/a.out`
```
00000110010100000000001010010011000011001010000000000011000100110000001001110011010000101011001100000000000000000000000001100011
```

### Pre-Assembling

#### Prerequisites
`program/main.s`
```
addi x5, x0, 100
mv x6, x5
neg x7, x6
```

#### Command
```bash
python preassemble.py program/main.s -o program/out.s
```

#### Output
```
Output written to programs/out.s
```

`program/out.s`
```
addi x5, x0, 100
addi x6, x5, 0
sub x7, x0, x6
```

### Disassembling (WIP)

### Running (WIP)