from src.tac_parser import parse_file
from src.liveness import analyze_liveness


def build_interference(instructions, live_out):
    graph = {}

    for instruction in instructions:
        if instruction["type"] in ("assign", "copy", "binary"):
            graph[instruction["dest"]] = set()

    for i, instruction in enumerate(instructions):
        if instruction["type"] not in ("assign", "copy", "binary"):
            continue

        dest = instruction["dest"]

        for var in live_out[i]:
            if var != dest:
                graph[dest].add(var)
                graph[var].add(dest)

    return graph


if __name__ == "__main__":
    instructions = parse_file("data/test/program1.tac")

    _, _, live_in, live_out = analyze_liveness(instructions)

    graph = build_interference(instructions, live_out)

    print("\nInterference Graph:")

    for var in sorted(graph):
        print(f"{var}: {sorted(graph[var])}")

    print("\nNode Degrees:")

    for var in sorted(graph):
        print(f"{var}: {len(graph[var])}")