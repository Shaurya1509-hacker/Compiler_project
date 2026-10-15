import csv
import os

from src.tac_parser import parse_file
from src.liveness import analyze_liveness
from src.interference import build_interference
from src.features import extract_features


def generate_dataset(program_files, output_file):
    rows = []

    for filename in program_files:
        instructions = parse_file(filename)

        _, _, _, live_out = analyze_liveness(instructions)
        graph = build_interference(instructions, live_out)
        features = extract_features(instructions, graph)

        for var, values in features.items():
            degree = values["degree"]
            live_range = values["live_range_length"]
            frequency = values["use_frequency"]

            spill_cost = (frequency + 1) / (degree + 1)
            spill_cost *= (live_range + 1)

            rows.append({
                "program": os.path.basename(filename),
                "variable": var,
                "degree": degree,
                "live_range_length": live_range,
                "use_frequency": frequency,
                "spill_cost": round(spill_cost, 4)
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
                "spill_cost"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset saved to {output_file}")
    print(f"Total examples: {len(rows)}")


if __name__ == "__main__":
    program_files = [
        f"data/generated/program{i}.tac"
        for i in range(1, 101)
    ]

    generate_dataset(
        program_files,
        output_file="data/train/spill_cost_dataset.csv"
    )