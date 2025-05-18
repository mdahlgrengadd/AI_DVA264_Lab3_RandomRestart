def pretty_print_neighbours(currentSolution, neighbours, fitness, neighboursFitness):
    print("Initial solution:     ", currentSolution,
          f"Fitness: {fitness}")

    # ANSI color codes for different colors
    colors = [
        "\033[91m",  # Red
        "\033[92m",  # Green
        "\033[93m",  # Yellow
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
    ]
    reset_color = "\033[0m"  # Reset to default terminal color
    green_color = "\033[92m"

    # Calculate all neighbour fitnesses
    fitnesses = [neighboursFitness[neighbour]
                 for neighbour in range(len(neighbours))]
    max_fitness = max(fitnesses)

    for i, neighbour in enumerate(neighbours):
        # Identify which bit was flipped
        flipped_bit = [j for j in range(
            len(currentSolution)) if currentSolution[j] != neighbour[j]][0]

        # Use color for the flipped bit
        color = colors[i % len(colors)]
        colored_neighbour = []
        for j, bit in enumerate(neighbour):
            if j == flipped_bit:
                colored_neighbour.append(f"{color}{bit}{reset_color}")
            else:
                colored_neighbour.append(str(bit))

        fitness = fitnesses[i]
        # Color the best fitness in green
        if fitness == max_fitness:
            fitness_str = f"{green_color}Fitness: {fitness}{reset_color}"
        else:
            fitness_str = f"Fitness: {fitness}"

        print(
            f"Neighbour {i:2d} (bit {flipped_bit:2d}): [{', '.join(colored_neighbour)}] {fitness_str}")
