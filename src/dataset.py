import csv
import os

from src.tac_parser import parse_file
from src.liveness import analyze_liveness
from src.interference import build_interference
from src.classical_allocator import allocate_registers
from src.features import extract_features


def generate_dataset(program_files, k, output_file):
    rows = []

    for filename in program_files:
        instructions = parse_file(filename)

        _, _, _, live_out = analyze_liveness(instructions)
        graph = build_interference(instructions, live_out)

        features = extract_features(instructions, graph)
        _, spilled = allocate_registers(graph, k)

        for var, values in features.items():
            rows.append({
                "program": os.path.basename(filename),
                "variable": var,
                "degree": values["degree"],
                "live_range_length": values["live_range_length"],
                "use_frequency": values["use_frequency"],
                "label": int(var in spilled)
            })

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "program",
                "variable",
                "degree",
                "live_range_length",
                "use_frequency",
                "label"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset saved to {output_file}")
    print(f"Total examples: {len(rows)}")
    print(f"Spill examples: {sum(row['label'] for row in rows)}")


if __name__ == "__main__":
    program_files = [
    "data/test/program1.tac",
    "data/test/program2.tac",
    "data/test/program3.tac",
    "data/test/program4.tac",
    "data/test/program5.tac"
]

    generate_dataset(
        program_files,
        k=3,
        output_file="data/train/dataset.csv"
    )