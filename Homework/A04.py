# Name : Siarhei Hancharou
# Assignment #: 4
# Submission Date : 11/ /2020
#
# Description of program "More Fun With Functions & Python Lists.":
# The program demonstrates the capabilities of programs 1, 2, 3
# with the ability to enter data automatically and manually.
# Also, a demonstration of all three programs with randomly selected data.
# Program 1: Dot Product Between Two Vectors.
# Program 2: The Transpose of a Matrix (2D List).
# Program 3: Scalar Matrix (i.e. 2D list) Multiplication.

import random

# Create random values that will be used as constants.
# ROW - number of row.
# COL - number of columns.
# VAL_MIN = The minimum value of a number in the matrix.
# VAL_MAX = The maximum value of a number in the matrix.
# V - is used in multiply(two_dim_list, v) to multiply a given matrix by this
# scalar value V.
# manually_def - just a string later in the code if it is equal = "m",
# you will be prompted to enter data manually.
# one_dimensional - dimension value of the list.
# two_dimensional - dimension value of the list.
ROW = random.randint(5, 10)
COL = random.randint(5, 10)
VAL_MIN = random.randint(-100, 0)
VAL_MAX = random.randint(0, 100)
V = random.randint(-3, 10)
manually_def = "any"
one_dimensional = 1
two_dimensional = 2


# This function starts the program.
def main(manually):
    print("*******************************************************")
    print("Welcome to More Fun With Functions & Python Lists.")
    print("*******************************************************")
    print("Program 1: Dot Product Between Two Vectors.")
    print("Program 2: The Transpose of a Matrix (2D List).")
    print("Program 3: Scalar Matrix (i.e. 2D list) Multiplication.")
    print("********************************************************")

    # Infinite loop, exit it only if "exit" is entered
    while True:
        print("-----------------------------------------")
        print("To run the program #1.........enter '1'")
        print("To run the program #2.........enter '2'")
        print("To run the program #3.........enter '3'")
        print("Launch and display all \n"
              "programs with random values...enter '4'")
        print("To exit the program ..........enter 'exit'")
        print("------------------------------------------")
        try:
            # Program selection.
            num_pr = input("Enter: ")
            print()

            # Exit the loop and program.
            if num_pr == "exit":
                break

            # If the program is 1, 2, 3, you are prompted to select
            # manually or automatically add data
            if int(num_pr) == 1 or int(num_pr) == 2 or int(num_pr) == 3:
                # If the value "manually" is equal to "m",
                # the user will enter the data manually.
                manually = input("If you want to enter vector values "
                                 "manually enter 'm',\nfor random create "
                                 "vectors enter any character: \n")

            if int(num_pr) == 1:
                logic_program_1(manually, one_dimensional)

            if int(num_pr) == 2:
                logic_program_2(manually, two_dimensional)

            if int(num_pr) == 3:
                logic_program_3(manually, two_dimensional)

            if int(num_pr) == 4:
                logic_program_4(manually)

        except ValueError:
            print("Enter a number, not a character!")


# Program 1: Dot Product Between Two Vectors.
# function dot_product(list_a, list_b) scalar product.
# return the dot product of two vectors
def dot_product(list_a, list_b):
    total_dot_product = 0
    for a_i in range(len(list_a)):
        for b_j in range(len(list_b)):
            if a_i == b_j:
                # the dot product of two vectors is added to dot_product.
                # dot_product += (a[0] * b[0] + a[1] * b[1] +....+ a[i] * b[j])
                total_dot_product += list_a[a_i] * list_b[b_j]

    return total_dot_product


# Program 2: The Transpose of a Matrix (2D List).
# The function gets a two dimensional list "two_dim_list"
# converts it to transpose two dimensional list "transpose_two_dim_list".
# returns a transposed list.
def transpose(two_dim_list):
    transpose_two_dim_list = []
    # iterate over list two_dim_list to the length of an item.
    for i in range(len(two_dim_list[0])):
        row = []
        for item in two_dim_list:
            # appending to list row[] with values and index positions
            # i contains index position and item contains values
            row.append(item[i])
        transpose_two_dim_list.append(row)

    return transpose_two_dim_list


# Program 3: Scalar Matrix (i.e. 2D list) Multiplication.
# The function gets a two dimensional list "two_dim_list"
# A matrix A can be multiplied by a scalar value v to create a
# new matrix B = scalar multiply(v;A) where each element of A is multiplied
# by the scalar value v.
# returns a multiply list.
def multiply(two_dim_list, v):
    multiply_two_dim_list = []
    for i in range(len(two_dim_list)):
        row = []
        for j in range(len(two_dim_list[i])):
            row.append(two_dim_list[i][j] * v)
        multiply_two_dim_list.append(row)

    return multiply_two_dim_list


# This function is called when the user chooses to manually
# enter values in the matrix. Accepts the dimension of the
# list and the number of columns and rows.
# Returns a list with manually entered data.
def creat_list_manually(n_dimensional, n_col, n_row):
    my_list = []
    if n_dimensional == 1:
        count = 0
        for i in range(n_row):
            new_val = int(input("index[" + str(count) + "]\n"))
            my_list.append(new_val)
            print(my_list)
            count += 1

    if n_dimensional == 2:
        for i in range(n_col):
            count = 0
            row = []
            for j in range(n_row):
                new_val = int(input("List index [" + str(i) + "][" +
                                    str(count) + "]\n"))
                row.append(new_val)
                count += 1

            my_list.append(row)

    return my_list


# The function displays the matrix for the user,
# but aligns all cells depending on the maximum value "absolute_value".
# absolute_value - the absolute value of the given number(n_dim_list[i][j]).
def print_matrix(n_dim_list, n_dimensional):
    if n_dimensional == 2:
        absolute_value = 0
        for i in n_dim_list:
            for j in i:
                if abs(j) > absolute_value:
                    absolute_value = abs(j)
        p = "{:2d}"
        if absolute_value < 10:
            p = "{:2d}"
        if 100 > absolute_value >= 10:
            p = "{:3d}"
        if 1000 > absolute_value >= 100:
            p = "{:4d}"
        if 10000 > absolute_value >= 1000:
            p = "{:5d}"
        if absolute_value > 10000:
            p = "{:6d}"
        for i in n_dim_list:
            for j in i:
                print(p.format(j), end=" ")
            print()


# The logic of the sequence program 1.
def logic_program_1(manually, n_dimensional):
    print("Program 1: Dot Product Between Two Vectors.")
    # If the value "manually" is equal to "m",
    # the user will enter the data manually.
    if manually == 'm':
        col = int(input("Enter len(list): "))
        while col == 0:
            print("Enter a any number, but not a 0.")
            col = int(input("Enter len(list): "))
        row = col // col
        print("Enter values for vector_a")
        vector_a = creat_list_manually(n_dimensional, row, col)
        print("Enter values for vector_b")
        vector_b = creat_list_manually(n_dimensional, row, col)

    # Automatic creation of matrices.
    else:
        # initializing two lists vector_a, vector_b with random
        # int value,length = n.
        vector_a = [random.randint(VAL_MIN, VAL_MAX) for i in range(COL)]
        vector_b = [random.randint(VAL_MIN, VAL_MAX) for i in range(COL)]

    print("vector_a: ", vector_a, sep="")
    print("vector_b: ", vector_b, sep="")
    print("dot_product = vector_a * vector_b")
    print("dot_product = ", dot_product(vector_a, vector_b))
    print()


# The logic of the sequence program 2.
def logic_program_2(manually, n_dimensional):
    print("Program 2: The Transpose of a Matrix (2D List).")
    if manually == 'm':
        col = int(input("Enter the length of the matrix column: "))
        row = int(input("Enter the length of the matrix row: "))
        my_two_dim_list = creat_list_manually(n_dimensional, row, col)

    else:
        # initializing a two-dimensional list with random values.
        my_two_dim_list = [[random.randint(VAL_MIN, VAL_MAX)
                            for i in range(COL)] for i in range(ROW)]

    print("Matrix A: ")
    print_matrix(my_two_dim_list, n_dimensional)
    print()
    print("Transpose(A): ")
    print_matrix(transpose(my_two_dim_list), n_dimensional)
    print()


# The logic of the sequence program 3.
def logic_program_3(manually, n_dimensional):
    print("Program 3: Scalar Matrix (i.e. 2D list) Multiplication.")
    if manually == 'm':
        v = int(input("Enter scalar value v: "))
        col = int(input("Enter the length of the matrix column: "))
        row = int(input("Enter the length of the matrix row: "))
        my_two_dim_list = creat_list_manually(n_dimensional, row, col)

    else:
        # initializing a two-dimensional list with random values.
        my_two_dim_list = [[random.randint(VAL_MIN, VAL_MAX)
                            for i in range(COL)] for i in range(ROW)]
        v = V

    print("Scalar value: v = ", v, sep='')
    print("Matrix B = scalar_multiply(v, Matrix A)")
    print("Matrix A: ")
    print_matrix(my_two_dim_list, n_dimensional)
    print()
    print("Matrix B: ")
    print_matrix(multiply(my_two_dim_list, v), n_dimensional)
    print()


# The logic of the sequence programs 1, 2, 3.
# With random values of matrices, scalar value v.
def logic_program_4(manually):
    logic_program_1(manually, one_dimensional)
    logic_program_2(manually, two_dimensional)
    logic_program_3(manually, two_dimensional)


main(manually_def)
