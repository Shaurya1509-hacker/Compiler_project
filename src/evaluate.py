import time
import pandas as pd
from src.tac_parser import parse_file
from src.liveness import analyze_liveness
from src.interference import build_interference
from src.features import extract_features
from src.classical_allocator import allocate_registers
from src.ml_allocator import allocate_ml
import joblib


def evaluate(programs, k=3):
    model = joblib.load("models/spill_model.pkl")
    results = []

    for program in programs:
        instructions = parse_file(program)
        _, _, _, live_out = analyze_liveness(instructions)
        graph = build_interference(instructions, live_out)
        features = extract_features(instructions, graph)

        start = time.perf_counter()
        _, classical_spills = allocate_registers(graph, k)
        classical_time = time.perf_counter() - start

        start = time.perf_counter()
        _, ml_spills = allocate_ml(graph, features, model, k)
        ml_time = time.perf_counter() - start

        results.append({
            "Program": program,
            "Registers": k,
            "Classical Spills": len(classical_spills),
            "ML Spills": len(ml_spills),
            "Classical Time (ms)": round(classical_time * 1000, 4),
            "ML Time (ms)": round(ml_time * 1000, 4)
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    df.to_csv("results/evaluation.csv", index=False)
    print("\nResults saved to results/evaluation.csv")


if __name__ == "__main__":
    programs = [
        "data/test/program1.tac",
        "data/test/program4.tac",
        "data/test/program5.tac"
    ]

    evaluate(programs, k=3)