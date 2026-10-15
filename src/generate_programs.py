import os
import random


def generate_program(program_id, num_vars=12):
    lines = []
    vars = []

    first = random.randint(10, 100)
    lines.append(f"v0 = {first}")
    vars.append("v0")

    for i in range(1, num_vars):
        dest = f"v{i}"
        left = random.choice(vars)

        if random.random() < 0.3:
            right = random.randint(1, 20)
        else:
            right = random.choice(vars)

        op = random.choice(["+", "-", "*"])

        lines.append(f"{dest} = {left} {op} {right}")
        vars.append(dest)

    lines.append(f"print {random.choice(vars)}")

    return lines


def main():
    random.seed(42)

    output_dir = "data/generated"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, 101):
        lines = generate_program(i, random.randint(8, 20))

        filename = os.path.join(
            output_dir,
            f"program{i}.tac"
        )

        with open(filename, "w") as file:
            file.write("\n".join(lines) + "\n")

    print("Generated 100 TAC programs in", output_dir)


if __name__ == "__main__":
    main()