from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import random

# The dataset is uploaded
f = open("Assignment 3 medical_dataset.DATA")
dataset_X = []
dataset_y = []
line = " "
while line != "":
    line = f.readline()
    line = line[:-1]
    if line != "":
        line = line.split(",")
        floatList = []
        for i in range(len(line)):
            if i < len(line)-1:
                floatList.append(float(line[i]))
            else:
                value = float(line[i])
                if value == 0:
                    dataset_y.append(0)
                else:
                    dataset_y.append(1)
        dataset_X.append(floatList)
f.close()

# The dataset is splited into training and test.
X_train, X_test, y_train, y_test = train_test_split(
    dataset_X, dataset_y, test_size=0.25, random_state=0)

# The dataset is scaled
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# The model is created
model = KNeighborsClassifier(n_neighbors=3)

# Function that calculates the fitness of a solution


def calculateFitness(solution):
    fitness = 0

    # The features are selected according to solution
    X_train_Fea_selc = []
    X_test_Fea_selc = []
    for example in X_train:
        X_train_Fea_selc.append([a*b for a, b in zip(example, solution)])
    for example in X_test:
        X_test_Fea_selc.append([a*b for a, b in zip(example, solution)])

    model.fit(X_train_Fea_selc, y_train)

    # We predict the test cases
    y_pred = model.predict(X_test_Fea_selc)

    # We calculate the Accuracy
    cm = confusion_matrix(y_test, y_pred)
    TP = cm[0][0]  # True positives
    FP = cm[0][1]  # False positives
    TN = cm[1][1]  # True negatives
    FN = cm[1][0]  # False negatives

    fitness = (TP + TN) / (TP + TN + FP + FN)

    return round(fitness * 100, 2)


MAX_FITNESS_CALCULATIONS = 5000

# TODO: Write your algorithm as a funciton. You can add input parameters if you want.

# Random-Restart Hill Climbing
# Reference: Lecture 6, "Beyond Classical Search", Artificial Intelligence 1 (DVA264), Johan Hjorth
#
# BestSolution <-- None
# Repeat N times:
#   CurrentSolution <-- generateRandomInitialSolution()
#   While True do
#     Neighbors <-- GenerateAllNeighbors(CurrentSolution)
#     BestNeighbor <-- SelectBest(Neighbors)
#     If BestNeighbor is better than CurrentSolution then
#         CurrentSolution <-- BestNeighbor
#     Else
#         Break
#   If BestSolution is None or CurrentSolution is better than BestSolution then
#       BestSolution <-- CurrentSolution
# FinalSolution <-- BestSolution


def HillClimbingRandomRestart(N=5):
    FITNESS_CALCULATIONS_COUNTER = 0

    bestSolution = None
    bestSolutionFitness = -1000
    for step in range(N):
        currentSolution = generateRandomInitialSolution()
        currentSolutionFitness = calculateFitness(currentSolution)

        while True:
            neighbours = GenerateAllNeighbours(currentSolution)
            neighboursFitness = [calculateFitness(
                neighbours[i]) for i in range(len(neighbours))]
            FITNESS_CALCULATIONS_COUNTER += len(neighboursFitness)

            bestNeighbourIdx = neighboursFitness.index(max(neighboursFitness))
            bestNeighbour = neighbours[bestNeighbourIdx]
            bestNeighbourFitness = neighboursFitness[bestNeighbourIdx]
            if bestNeighbourFitness > currentSolutionFitness:
                currentSolution = bestNeighbour
                currentSolutionFitness = bestNeighbourFitness
                print(
                    f"Best solution fitness: ({FITNESS_CALCULATIONS_COUNTER} / {MAX_FITNESS_CALCULATIONS})", currentSolutionFitness)
            else:
                break
            if FITNESS_CALCULATIONS_COUNTER >= MAX_FITNESS_CALCULATIONS:
                print("Maximum fitness calculations reached.")
                break

        if bestSolution is None or currentSolutionFitness > bestSolutionFitness:
            bestSolution = currentSolution
            bestSolutionFitness = currentSolutionFitness

    return bestSolution, bestSolutionFitness


def generateRandomInitialSolution(seed=None):
    if seed is not None:
        random.seed(seed)

    return [random.randint(0, 1) for _ in range(len(X_train[0]))]


def GenerateAllNeighbours(currentSolution):
    # Generate all neighbours of the current solution
    # by fliping each bit one at a time

    neighbours = []
    for i in range(len(currentSolution)):
        neighbour = currentSolution.copy()
        neighbour[i] = 1 - neighbour[i]
        neighbours.append(neighbour)

    return neighbours


def main():
    results = []
    for i in range(3):
        print(f"\nRun {i+1}:")
        solution, fitness = HillClimbingRandomRestart(5)
        print(f"Solution fitness: {fitness}")
        print(f"Solution: {solution}")
        results.append(fitness)

    # Calculate and display average
    average_fitness = sum(results) / len(results)
    print("\n" + "-"*50)
    print(f"Average fitness: {average_fitness:.2f}")


if __name__ == "__main__":
    main()
