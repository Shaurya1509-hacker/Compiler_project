import re


def parse_line(line):
    line = line.strip()

    if not line:
        return None

    if line.startswith("print "):
        var = line[6:].strip()

        if not re.fullmatch(r"[a-zA-Z_]\w*", var):
            raise ValueError(f"Invalid print statement: {line}")

        return {
            "type": "print",
            "var": var
        }

    match = re.fullmatch(
        r"([a-zA-Z_]\w*)\s*=\s*(.+)",
        line
    )

    if not match:
        raise ValueError(f"Invalid TAC instruction: {line}")

    dest, expr = match.groups()
    expr = expr.strip()

    if re.fullmatch(r"-?\d+", expr):
        return {
            "type": "assign",
            "dest": dest,
            "value": int(expr)
        }

    if re.fullmatch(r"[a-zA-Z_]\w*", expr):
        return {
            "type": "copy",
            "dest": dest,
            "src": expr
        }

    match = re.fullmatch(
        r"([a-zA-Z_]\w*|-?\d+)\s*([+\-*/])\s*([a-zA-Z_]\w*|-?\d+)",
        expr
    )

    if match:
        left, op, right = match.groups()

        return {
            "type": "binary",
            "dest": dest,
            "left": int(left) if re.fullmatch(r"-?\d+", left) else left,
            "op": op,
            "right": int(right) if re.fullmatch(r"-?\d+", right) else right
        }

    raise ValueError(f"Unsupported TAC expression: {expr}")


def parse_file(filename):
    instructions = []

    with open(filename, "r") as file:
        for line_no, line in enumerate(file, start=1):
            try:
                instruction = parse_line(line)

                if instruction is not None:
                    instructions.append(instruction)

            except ValueError as e:
                raise ValueError(f"Line {line_no}: {e}") from e

    return instructions


if __name__ == "__main__":
    program = parse_file("data/test/program1.tac")

    for instruction in program:
        print(instruction)