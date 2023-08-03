from flask import Flask, request, render_template
from constraints_fourbyfour import constraintsFour
from sudoku_constraints import constraintsNine
import copy

fourPuzzle = [[1, None, None, None], [None, 2, None, None], [None, None, 3, None], [None, None, None, 4]]

puzzle1 = [[7,None,None,4,None,None,None,8,6],
            [None,5,1,None,8,None,4,None,None],
            [None,4,None,3,None,7,None,9,None],
            [3,None,9,None,None,6,1,None,None],
            [None,None,None,None,2,None,None,None,None],
            [None,None,4,9,None,None,7,None,8],
            [None,8,None,1,None,2,None,6,None],
            [None,None,6,None,5,None,9,1,None],
            [2,1,None,None,None,3,None,None,5]]

puzzle2 = [[1,None,None,2,None,3,8,None,None],
            [None,8,2,None,6,None,1,None,None],
            [7,None,None,None,None,1,6,4,None],
            [3,None,None,None,9,5,None,2,None],
            [None,7,None,None,None,None,None,1,None],
            [None,9,None,3,1,None,None,None,6],
            [None,5,3,6,None,None,None,None,1],
            [None,None,7,None,2,None,3,9,None],
            [None,None,4,1,None,9,None,None,5]]

puzzle3 = [[1,None,None,8,4,None,None,5,None],
            [5,None,None,9,None,None,8,None,3],
            [7,None,None,None,6,None,1,None,None],
            [None,1,None,5,None,2,None,3,None],
            [None,7,5,None,None,None,2,6,None],
            [None,3,None,6,None,9,None,4,None],
            [None,None,7,None,5,None,None,None,6],
            [4,None,1,None,None,6,None,None,7],
            [None,6,None,None,9,4,None,None,2]]

puzzle4 = [[None,None,None,None,9,None,None,7,5],
            [None,None,1,2,None,None,None,None,None],
            [None,7,None,None,None,None,1,8,None],
            [3,None,None,6,None,None,9,None,None],
            [1,None,None,None,5,None,None,None,4],
            [None,None,6,None,None,2,None,None,3],
            [None,3,2,None,None,None,None,4,None],
            [None,None,None,None,None,6,5,None,None],
            [7,9,None,None,1,None,None,None,None]]

puzzle5 = [[None,None,None,None,None,6,None,8,None],
            [3,None,None,None,None,2,7,None,None],
            [7,None,5,1,None,None,6,None,None],
            [None,None,9,4,None,None,None,None,None],
            [None,8,None,None,9,None,None,2,None],
            [None,None,None,None,None,8,3,None,None],
            [None,None,4,None,None,7,8,None,5],
            [None,None,2,8,None,None,None,None,6],
            [None,5,None,9,None,None,None,None,None]]


# Part 1
# Create a CSP class to specify a sudoku puzzle
class CSP:

    def __init__(self, puzzle, constraints):
        
        # puzzleSize holds the number of rows/columns of the puzzle
        puzzleSize = len(puzzle)

        # Initialize variables as a dictionary
        variables = {}

        # Loops through each cell in the puzzle
        for row in range(puzzleSize):
            for col in range(puzzleSize):

                # position on the board is the key
                key = "C" + str(row+1) + str(col+1)

                # the values in the dictionary are arrays of ints
                variables[key] = []

                # if the cell is empty, then the domain of ints 
                # are added as the value for that variable
                if(puzzle[row][col] == None):
                    for i in range(puzzleSize+1):
                        if(i == 0):
                            continue
                        variables[key].append(i)
                # if the cell has a number in it, then that single int
                # is added as the value for that variable 
                else:
                    variables[key].append(puzzle[row][col])


        # Sorts the dictionary alphabetically by keys
        myKeys = variables.keys()
        sorted_keys = sorted(myKeys)
        mySortedVars = {}
        for key in sorted_keys:
            mySortedVars[key] = variables[key]
 
     
        self.variablesCSP = variables
        self.constraintsCSP = constraints
        self.puzzleSizeCSP = puzzleSize
        self.answers = []


# getAssignments() is a helper function that takes in a CSP
# and returns a dictionary of assignments for each variable
def getAssignments(CSP):
    myAssignment = {}
    for key in CSP.variablesCSP:
        if len(CSP.variablesCSP[key]) == 1:
            myAssignment[key] = CSP.variablesCSP[key][0]
        else:
            myAssignment[key] = None

    return myAssignment 
    

# Part 2
# revise() function takes in a CSP and the names of two variables
# and modifies the CSP, removing any value in the first variable's
# domain where there isn't a corresponding value in the other variable's
# domain that satisfies the constraint between the variables
# And returns a boolean indicating whether or not any values were removed
def revise(CSP, varA, varB):


    # Boolean to check if number in the domain needs to be removed
    hasDeletedVal = False

    # Boolean to check if there us at least 1 mapping that exists for a given number
    atLeastOneMapping = False



    # Gets variable name of VarA and saves the board position as an int
    numA = int(varA[1:])

    # Gets variable name of VarB and saves the board position as an int
    numB = int(varB[1:])

    #Gets current constraints from the given 2 variables
    currConstraints = []
    if(numA < numB):
        currConstraints = CSP.constraintsCSP[varA, varB]
    else:
        currConstraints = CSP.constraintsCSP[varB, varA]
    

    # Loops through the numbers in domainA and domainB
    for intA in CSP.variablesCSP[varA]:        

        for intB in CSP.variablesCSP[varB]:

            # Creates a pair given a num in domainA and domainB
            pair = [intA, intB]

            # If the pair exists in the constraints, 
            # then there exists at least 1 mapping, 
            # thus the current number in domainA should not be removed
            if (pair in currConstraints):
                atLeastOneMapping = True
        
        # If at least 1 mapping from pairing the nums of domainA and domainB
        # does not exist, then the current number in domainA should be removed
        if atLeastOneMapping == False:
            CSP.variablesCSP[varA].remove(intA)

            hasDeletedVal = True
        
        # Resets atLeastOneMapping to false
        atLeastOneMapping = False


    return hasDeletedVal


# Part 3
# AC3func() function takes in a CSP and modified it such that any 
# inconsistent values across all domains are removed
# Retusn a boolean indicating wheather or not any values were removed
def AC3func(CSP):

    # Boolean that tracks if a variable has at least 
    # 1 value left in its domain
    atLeast1ValLeft = True

    # Array called queue that holds the constraints
    queue = []
    for constraint in CSP.constraintsCSP:
        queue.append(constraint)


    # Loops through while queue is not empty
    while queue != []:

        # Saves the first constraint in the queue
        currConst = queue.pop()

        # Finds the constraint's 2 cells and saves it as varA and varB
        varA = currConst[0]
        varB = currConst[1]

        
        # Calls the revise function and paseses in the CSP, varA, varB
        if revise(CSP, varA, varB) or revise(CSP, varB, varA):

            # If the domain of varA is empty, then there are 
            # no values left in the domain
            if len(CSP.variablesCSP[varA]) == 0 or len(CSP.variablesCSP[varB]) == 0:
                return False
                #atLeast1ValLeft = False

            # Loops through the all the constraints and 
            # adds the constraint in the queue if the variable is found 
            for cons in CSP.constraintsCSP:
                if varA in cons or varB in cons:
                    queue.append(cons)
    
        
    return atLeast1ValLeft



# Part 4
# minimumRemainingValues() function which takes in a CSP and a set of assigned variables
# And returns the vairbale with the fewest values in its domain among the unassigned
# variables in the CSP
def minimumRemainingValues(CSP, assignedVars):
    
    # Initializes the variable with the fewest number of values in its domain
    varFewestVals =  None

    # Loops through the assignedVars
    for key in assignedVars:

        # If the variable is unassigned, meaning its value is empty
        if assignedVars[key] == None:

            # Handles the initial varFewestVal since it is set to None
            if varFewestVals == None:
                # Sets the variable with the fewest number of values
                # in its domain to be the current key
                varFewestVals = key
            
            # If the length of the current variable's domain is less than
            # the length of varFewestVals's domain
            elif len(CSP.variablesCSP[key]) < len(CSP.variablesCSP[varFewestVals]):

                # Sets the variable with the fewest number of values
                # in its domain to be the current key
                varFewestVals = key


    # Returns the variable with the fewest number of values in its domain    
    return varFewestVals



# backtrack() function that takes in a CSP and assignment
def backtrack(CSP, assignment):
    
    # Returns the assignment dictionary if all the values are assigned
    if None not in assignment.values():
        return assignment 

    # Calls the minimumRemainingValues() function to choose a variable
    myVariable = minimumRemainingValues(CSP, assignment)

    myDomain = copy.deepcopy(CSP.variablesCSP)

    for num in myDomain[myVariable]:

        # Assigns the current variable to the num
        assignment[myVariable] = num

        # Assigns the variables's domain to be the num
        CSP.variablesCSP[myVariable] = [num]

        # Calls the AC3func() and returns if all variables have 
        # at least one value left in their domains
        inferences = AC3func(CSP)

        if inferences:

            CSP.answers.append(myVariable)

            # Recursively calls backtrack
            result = backtrack(CSP, assignment)

            # Returns the result if it did not fail
            if result != 'failure': 
                
                return result

        # Resets the variables to be the deepcopy of the domains
        CSP.variablesCSP = myDomain

    # Returns failure if a valid assignment was not created
    return 'failure'


# Part 5
# backtrackingSearch() takes in a CSP
# finds a valid assignment for all the variables in the CSP, if one exists
def backtrackingSearch(CSP):

    # Calls AC3func()
    AC3vars = AC3func(CSP)

    # Gets the dictionary of assignments given initial CSP
    assignment = getAssignments(CSP)

    # Calls backtrack() function and 
    # Returns final solution of assignments for soduko puzzle
    return backtrack(CSP, assignment)

def main():
    print('Start-----------------------------------------------------------------------------------------------------------------')

    #-----------------------------------------------------------------------------------------------------------------
    # Part 1
    # CSP for a 4x4 suduko puzzle
    print('')
    print('Part1: CSP()-----------------------------------------------------------------------------------------------------------------')
    part1CSP = CSP(fourPuzzle, constraintsFour)
    print('Variables: ')
    print(part1CSP.variablesCSP)
    print('Constraints: ')
    print(part1CSP.constraintsCSP)

    #-----------------------------------------------------------------------------------------------------------------
    # Part 2
    # Calls revise() function
    print('')
    print('Part2: revise()-----------------------------------------------------------------------------------------------------------------')
    part2CSP = CSP(fourPuzzle, constraintsFour)
    resultRevise1 = revise(part2CSP, 'C11', 'C12')
    print(resultRevise1)
    print("It is " + str(resultRevise1) + " that a value was removed from the domain")
    resultRevise2 = revise(part2CSP, 'C12', 'C11')
    print(resultRevise2)
    print("It is " + str(resultRevise2) + " that a value was removed from the domain")

    print('ResultRevise2: ')
    print(part2CSP.variablesCSP)
    print('One value was removed from C12')

    #-----------------------------------------------------------------------------------------------------------------
    # Part 3
    # Calls AC3func() function
    print('')
    print('Part3: AC3func()-----------------------------------------------------------------------------------------------------------------')
    part3CSP = CSP(fourPuzzle, constraintsFour)
    myPart3AC3 = AC3func(part3CSP)
    print(myPart3AC3)
    print("It is " + str(myPart3AC3) + " that each variable has at least 1 value in its domain")

    print('Altered CSP: ')
    print(part3CSP.variablesCSP)

    #-----------------------------------------------------------------------------------------------------------------
    # Part 4
    # Calls minimumRemainingValues() function
    print('')
    print('Part4: minimumRemainingValues()-----------------------------------------------------------------------------------------------------------------')
    part4CSP = CSP(fourPuzzle, constraintsFour)
    myPart4AC3 = AC3func(part4CSP)
    testAssignedVars = {'C11': 1, 'C12': None, 'C13': None, 'C14': None,
                        'C21': None, 'C22': 2, 'C23': None, 'C24': None,
                        'C31': None, 'C32': None, 'C33': 3, 'C34': None,
                        'C41': None, 'C42': None, 'C43': None, 'C44': 4,}
    varFewestVals = minimumRemainingValues(part4CSP, testAssignedVars)
    print('Variable with smallest domain: ')
    print(varFewestVals)
    print('Chooses the first instance of the variable with the smallest domain')




    #-----------------------------------------------------------------------------------------------------------------
    # Part 5
    # Calls backtrackingSearch() function
    print('')
    print('Part5-----------------------------------------------------------------------------------------------------------------')
    part5ACSP = CSP(fourPuzzle, constraintsFour)
    part5BCSP = CSP(puzzle2, constraintsNine)

    
    result = backtrackingSearch(part5ACSP)
    print('')
    print('Final 4x4 sudoku board results: ')
    print(result)


    result2 = backtrackingSearch(part5BCSP)
    print('')
    print('Final 9x9 sudoku board results (Puzzle 2): ')
    print(result2)
   

    


    print('')
    print('End-----------------------------------------------------------------------------------------------------------------')



# Creates an array to hold the ordered cells
order = []
for i in range(1,10):
    for j in range(1,10):
        order.append("C"+str(i)+str(j))

#-----------------------------------------------------------------------------------------------------------------
# Part 6: Web-Based Visualization of Backtracking Search
# Web-based  visualization of backtracking search
# Allows user to specify a Sudoku puzzple
# Shows solution for the final board
app = Flask(__name__)
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":

        # Gets all 81 input values from the user
        C11 = request.form.get("a11")
        C12 = request.form.get("a12")
        C13 = request.form.get("a13")
        C14 = request.form.get("a14")
        C15 = request.form.get("a15")
        C16 = request.form.get("a16")
        C17 = request.form.get("a17")
        C18 = request.form.get("a18")
        C19 = request.form.get("a19")
        C21 = request.form.get("a21")
        C22 = request.form.get("a22")
        C23 = request.form.get("a23")
        C24 = request.form.get("a24")
        C25 = request.form.get("a25")
        C26 = request.form.get("a26")
        C27 = request.form.get("a27")
        C28 = request.form.get("a28")
        C29 = request.form.get("a29")
        C31 = request.form.get("a31")
        C32 = request.form.get("a32")
        C33 = request.form.get("a33")
        C34 = request.form.get("a34")
        C35 = request.form.get("a35")
        C36 = request.form.get("a36")
        C37 = request.form.get("a37")
        C38 = request.form.get("a38")
        C39 = request.form.get("a39")
        C41 = request.form.get("a41")
        C42 = request.form.get("a42")
        C43 = request.form.get("a43")
        C44 = request.form.get("a44")
        C45 = request.form.get("a45")
        C46 = request.form.get("a46")
        C47 = request.form.get("a47")
        C48 = request.form.get("a48")
        C49 = request.form.get("a49")
        C51 = request.form.get("a51")
        C52 = request.form.get("a52")
        C53 = request.form.get("a53")
        C54 = request.form.get("a54")
        C55 = request.form.get("a55")
        C56 = request.form.get("a56")
        C57 = request.form.get("a57")
        C58 = request.form.get("a58")
        C59 = request.form.get("a59")
        C61 = request.form.get("a61")
        C62 = request.form.get("a62")
        C63 = request.form.get("a63")
        C64 = request.form.get("a64")
        C65 = request.form.get("a65")
        C66 = request.form.get("a66")
        C67 = request.form.get("a67")
        C68 = request.form.get("a68")
        C69 = request.form.get("a69")
        C71 = request.form.get("a71")
        C72 = request.form.get("a72")
        C73 = request.form.get("a73")
        C74 = request.form.get("a74")
        C75 = request.form.get("a75")
        C76 = request.form.get("a76")
        C77 = request.form.get("a77")
        C78 = request.form.get("a78")
        C79 = request.form.get("a79")
        C81 = request.form.get("a81")
        C82 = request.form.get("a82")
        C83 = request.form.get("a83")
        C84 = request.form.get("a84")
        C85 = request.form.get("a85")
        C86 = request.form.get("a86")
        C87 = request.form.get("a87")
        C88 = request.form.get("a88")
        C89 = request.form.get("a89")
        C91 = request.form.get("a91")
        C92 = request.form.get("a92")
        C93 = request.form.get("a93")
        C94 = request.form.get("a94")
        C95 = request.form.get("a95")
        C96 = request.form.get("a96")
        C97 = request.form.get("a97")
        C98 = request.form.get("a98")
        C99 = request.form.get("a99")


        
        # Create a 2D array as the start board
        startBoard = [[C11, C12, C13, C14, C15, C16, C17, C18, C19], 
                      [C21, C22, C23, C24, C25, C26, C27, C28, C29], 
                      [C31, C32, C33, C34, C35, C36, C37, C38, C39], 
                      [C41, C42, C43, C44, C45, C46, C47, C48, C49], 
                      [C51, C52, C53, C54, C55, C56, C57, C58, C59], 
                      [C61, C62, C63, C64, C65, C66, C67, C68, C69], 
                      [C71, C72, C73, C74, C75, C76, C77, C78, C79], 
                      [C81, C82, C83, C84, C85, C86, C87, C88, C89], 
                      [C91, C92, C93, C94, C95, C96, C97, C98, C99]]
    

        # Loop through the startBoard
        for row in range(9):
            for col in range(9):
                if startBoard[row][col] == '':
                    # If the value is empty, it is set to None
                    startBoard[row][col] = None
                else:
                    # Set the given numbers from str to int
                    startBoard[row][col] = int(startBoard[row][col])


        # Creates a CSP given the startBoard and 9x9 constraints
        myCSP = CSP(startBoard, constraintsNine)

        # Calls the backtrackingSearch() function, passing in myCSP
        # Returns the assignments as a dictionary in result
        result = backtrackingSearch(myCSP)

        # Array that holds the spots on the board after being filled
        filledSpot = []


        # Returns the solution board for the soduko puzzle
        # return render_template("solved.html", solutions = result)

        # Returns all the steps and the final solution board for the sudoko puzzle
        return render_template("final.html", solutions = result, series = myCSP.answers, order = order, filledSpot = filledSpot)
    
    # Returns the inital soduko board that takes in user input
    return render_template("sudoku.html")

if __name__=='__main__':
    main()
    app.run()
