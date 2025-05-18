from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import random

from utils import pretty_print_neighbours

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


def yourAlgorithm():
    FITNESS_CALCULATIONS_COUNTER = 0
    # Every time that you calculate the fitness value of a solution/combination you have to add one to FITNESS_CALCULATIONS_COUNTER. Example
    currentSolution = [random.randint(0, 1) for _ in range(X_train[0].size)]
    print("Initial solution array:", currentSolution)
    print("Initial solution fitness:", calculateFitness(currentSolution))
    print("-" * 50)

    bestSolution = currentSolution
    bestSolutionFitness = calculateFitness(currentSolution)
    fitness = calculateFitness(currentSolution)
    # find the best solution in the neighborhood
    # Generate all neighbors by flipping one bit at a time
    neighbours = generate_neighbours(currentSolution)
    neighboursFitness = [calculateFitness(
        neighbours[i]) for i in range(len(neighbours))]
    pretty_print_neighbours(currentSolution, neighbours,
                            fitness, neighboursFitness)

    while False:
        FITNESS_CALCULATIONS_COUNTER += 1

        currentSolutionFitness = fitness

        if currentSolutionFitness > bestSolutionFitness:
            bestSolution = currentSolution
            bestSolutionFitness = currentSolutionFitness
            print("Best solution fitness ( ", FITNESS_CALCULATIONS_COUNTER,
                  "/", MAX_FITNESS_CALCULATIONS, "):", bestSolutionFitness)
        else:
            if FITNESS_CALCULATIONS_COUNTER % 100 == 0:
                print("Current solution fitness ( ", FITNESS_CALCULATIONS_COUNTER,
                      "/", MAX_FITNESS_CALCULATIONS, "):", currentSolutionFitness)

        # Condition to stop the algorithm
        if FITNESS_CALCULATIONS_COUNTER >= MAX_FITNESS_CALCULATIONS:
            print("Maximum fitness calculations reached.")
            return bestSolution, bestSolutionFitness
    return bestSolution, bestSolutionFitness


def generate_neighbours(currentSolution):
    neighbours = []
    for i in range(len(currentSolution)):
        neighbour = currentSolution.copy()
        neighbour[i] = 1 - neighbour[i]  # Flip the bit at position i
        neighbours.append(neighbour)

    return neighbours

# Function to pretty print the neighbours with colors.
# Made by ChatGPT only for the better visualization of the neighbours


bestSolution, bestSolutionFitness = yourAlgorithm()

print("Best solution fitness (best):", bestSolutionFitness)
print("Best solution (best):", bestSolution)
