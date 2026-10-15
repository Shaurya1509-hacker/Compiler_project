import os
import time
import joblib
import pandas as pd

from src.tac_parser import parse_file
from src.liveness import analyze_liveness
from src.interference import build_interference
from src.features import extract_features
from src.classical_allocator import allocate_registers
from src.ml_allocator import allocate_ml
from src.validate_allocator import validate_allocation


def evaluate():
    model = joblib.load("models/spill_cost_model.pkl")
    results = []

    programs = [
        f"data/generated/program{i}.tac"
        for i in range(1, 101)
    ]

    for program in programs:
        instructions = parse_file(program)

        _, _, _, live_out = analyze_liveness(instructions)
        graph = build_interference(instructions, live_out)
        features = extract_features(instructions, graph)

        for k in [2, 3, 4]:
            start = time.perf_counter()
            classical_registers, classical_spills = allocate_registers(
                graph, k
            )
            classical_time = time.perf_counter() - start

            classical_valid = validate_allocation(
                graph, classical_registers, classical_spills
            )

            start = time.perf_counter()
            ml_registers, ml_spills = allocate_ml(
                graph, features, model, k
            )
            ml_time = time.perf_counter() - start

            ml_valid = validate_allocation(
                graph, ml_registers, ml_spills
            )

            results.append({
                "Program": os.path.basename(program),
                "Registers": k,
                "Classical Spills": len(classical_spills),
                "ML Spills": len(ml_spills),
                "Classical Valid": classical_valid,
                "ML Valid": ml_valid,
                "Classical Time (ms)": round(classical_time * 1000, 4),
                "ML Time (ms)": round(ml_time * 1000, 4)
            })

    df = pd.DataFrame(results)

    os.makedirs("results", exist_ok=True)
    df.to_csv("results/evaluation.csv", index=False)

    summary = df.groupby("Registers").agg({
        "Classical Spills": "mean",
        "ML Spills": "mean",
        "Classical Time (ms)": "mean",
        "ML Time (ms)": "mean"
    }).round(4)

    print("\nAverage Results Across 100 Programs:\n")
    print(summary.to_string())

    print("\nAllocation Validation:")
    print(f"Classical valid: {df['Classical Valid'].all()}")
    print(f"ML valid: {df['ML Valid'].all()}")

    print("\nDetailed results saved to results/evaluation.csv")


if __name__ == "__main__":
    evaluate() 