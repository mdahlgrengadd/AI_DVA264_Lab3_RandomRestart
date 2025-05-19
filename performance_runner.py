# language: python
# (no filepath—create this as e.g. Assignment_3_run.py in your workspace)

from Assignment_3_RandomRestartHillClimbing import HillClimbingRandomRestart
from Assignment_3_VariableNeighbour import VariableNeighbourSearch


def run_experiments():
    # --- Random-Restart Hill Climbing (5 restarts) ---
    rrhc_results = []
    print("=== Random-Restart Hill Climbing ===")
    for i in range(3):
        sol, fit = HillClimbingRandomRestart(5)
        print(f"Run {i+1}: fitness = {fit:.2f}")
        rrhc_results.append(fit)
    avg_rrhc = sum(rrhc_results) / len(rrhc_results)
    print(f"Average RRHC fitness over 3 runs: {avg_rrhc:.2f}\n")

    # --- Variable Neighbour Search (max_k=4) ---
    vns_results = []
    print("=== Variable Neighbour Search ===")
    for i in range(3):
        sol, fit = VariableNeighbourSearch(4)
        print(f"Run {i+1}: fitness = {fit:.2f}")
        vns_results.append(fit)
    avg_vns = sum(vns_results) / len(vns_results)
    print(f"Average VNS fitness over 3 runs: {avg_vns:.2f}\n")

    # --- Comparison ---
    better = "RRHC" if avg_rrhc > avg_vns else "VNS"
    print(
        f"On average, {better} performs better ({avg_rrhc:.2f} vs {avg_vns:.2f}).")


if __name__ == "__main__":
    run_experiments()
