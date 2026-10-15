def validate_allocation(graph, registers, spilled):
    errors = []

    for var, neighbors in graph.items():
        if var in spilled and var in registers:
            errors.append(
                f"{var} is both assigned a register and spilled"
            )

        if var not in spilled and var not in registers:
            errors.append(
                f"{var} has no register assignment and is not spilled"
            )

        if var in registers:
            for neighbor in neighbors:
                if neighbor in registers:
                    if registers[var] == registers[neighbor]:
                        errors.append(
                            f"{var} and {neighbor} interfere "
                            f"but share register R{registers[var] + 1}"
                        )

    if errors:
        print("Allocation INVALID:")
        for error in errors:
            print("-", error)
        return False

   # print("Allocation VALID")
    return True