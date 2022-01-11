# course: cmps3500
# CLASS Project (group 11)
# PYTHON IMPLEMENTATION OF A CUSTOM MATRIX CALCULATOR
# date: 5/21/21
# Student 1: Dat Pham
# description: Implementation of a scientific calculator ...
 
import os
import sys
import csv
import string
import numpy as np

matrixA = []
matrixB = []

def swap(m1,m2):
    global matrixA 
    matrixA = m2
    global matrixB
    matrixB = m1

# matrix1[row][col] + matrix2[row][col]
def add(m1,m2):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        print("Error: Matrix A and Matrix B is not same size")
        return 

    # use nested list comprehension to iterate through all indexes of passed in 
    # matrices and add
    matrix = [[m1[i][j] + m2[i][j] for j in range(len(m1))] for i in range(len(m1[0]))]
    return matrix

# matrix1[row][col] - matrix2[row][col]
def sub(m1,m2):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        print("Error: Matrix A and Matrix B is not same size")
        return
    
    # use nested list comprehension to iterate through all indexes of passed in 
    # matrices and subtract
    matrix = [[m1[i][j] - m2[i][j] for j in range(len(m1))] for i in range(len(m1[0]))] 
    return matrix

# scalor n * matrix[row][col]
def scalor_mult(n,m):
    
    # use nested list comprehension to iterate through the indexes of the passed  
    # in matrix and multiply by the scalor
    matrix = [[n * m[i][j] for j in range(len(m))] for i in range(len(m[0]))]
    return matrix

def transpose(m):
    # use nested list comprehension to switch rows and columns 
    matrix = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    return matrix

def dot_product(a1,a2):
    sum1 = 0
    for i in range(len(a1)):
        sum1 = sum1 + a1[i] * a2[i]
    return sum1

# matrix1[row][col] * matrix2[row][col]
def multiply(m1,m2):
    for i in range(len(m1)):
        if len(m1[i])!= len(m2): 
            print("Error: matrix1 row does not equal matrix2 column")  
            return
    
    m2_T = transpose(m2)    # get columns of m2 as rows
    # use nested list comprehension to iterate and perform the dot product
    matrix = [[dot_product(m1[i],m2_T[j]) for j in range(len(m2_T))] for i in range(len(m1))]
    return matrix 

def power(n,m):
    if n < 1 or n > 10:
        print("Error: power is outside range (only 1 <= n <= 10 is accepted)")
        return
    
    # recusion, continue multiplying matrix by itself until stop condition
    if n == 1:
        return m
    else:
        return multiply(m,power(n-1,m))

def identity(m):
    temp = []
    if len(m) != len(m[0]):
        print("Error: not a square matrix")
        return temp
    
    # create an empty array of 0's
    matrix = [[0 for j in range(len(m))] for i in range(len(m[0]))] 
    
    # set diagonal to 1
    for i in range(len(matrix)):
        matrix[i][i] = 1
    return matrix

    
# get inside matrix after removing i-th row, j-th col
def inner_matrix(m, i, j):
    m = np.array(m)
    m = m.tolist()
    return [row[: j] + row[j+1:] for row in (m[: i] + m[i+1:])] 
 
def deternminant(m):
    if len(m) != len(m[0]):
        print()
        print("Error: not a square matrix")
        return 

    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1]- m[0][1] * m[1][0]

    determinant = 0
    # column
    for i in range(len(m)):
        determinant += (-1**i)*m[0][i]* deternminant(inner_matrix(m,0,i))
    return determinant

def inverse(m):
    temp = []
    if len(m) != len(m[0]):
        print("Error: not a square matrix")
        return temp

    determinant = deternminant(m)
    # base case for 2x2 matrix
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant], [-1*m[1][0]/determinant, m[0][0]/determinant]]

    # find matrix of cofactors
    arr = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)):
            small_mat = inner_matrix(m,i,j)
            row.append(((-1)**(i + j)) * deternminant(small_mat))
        arr.append(row)
    arr = transpose(arr)
    for i in range(len(arr)):
        for j in range(len(arr)):
            arr[i][j] = arr[i][j]/determinant
    return arr
 
def menu():
    os.system( 'clear' ) # clearing screen

    print("         MATRIX CALCULATOR           ")
    print("***************************************")
    print("0) input new A,B  11) A * B  ")
    print("1) A <=> B        12) B * A  ")
    print("2) A = B (copy)   13) A^n, 1 <= n >= 10")  
    print("3) B = A (copy)   14) B^n, 1 <= n >= 10")
    print("4) A^T            15) det(A) ")
    print("5) B^T            16) det(B) ")
    print("6) A + B          17) A^-1 (inverse) ")
    print("7) A - B          18) B^-1 (inverse) ")
    print("8) B - A          19) A = I  ")
    print("9) n * A          20) B = I  ")  
    print("10) n * B         Enter 'x' to exit ")
    print()
    print("matrixA:")
    print(matrixA)
    print("matrixB:")
    print(matrixB)
    print() 

def fileIO():
    while(1):
        try:    
            temp = []
            # create a dictionary
            lowercase = dict.fromkeys(string.ascii_lowercase, 0)
            uppercase = dict.fromkeys(string.ascii_uppercase, 0) 
            f = input()
            with open(f, "r", encoding = "utf-8-sig", newline='') as csvfile:
                for row in csv.reader( csvfile, delimiter = ','):
                    temp.append(row)
                    #print(row)
                    for n in row:
                        if '.' in n:
                            print()
                            print("Error: matrix contains a float")
                            print("Enter another file: ", end = "")
                            temp = fileIO()
                            break
                        if n[0] in uppercase or n[0] in lowercase:
                            print()
                            print("Error: matrix contains a string")
                            print("Enter another file: ", end = "")
                            temp = fileIO()
                            break
            temp = np.array(temp, dtype=int)
            return temp
        except Exception:
            print()
            print("Error: file not found or invalid matrix")
            print("Enter another file: ")
            continue
        else:
            break
        
print("Enter file1: ", end = "")
matrixA = fileIO()
print()
print("Enter file2: ", end = "")
matrixB = fileIO()

menu()
while(1):
    print()
    op = input("Enter operation number: ")
    if op == 'x' or op == 'X':
        print("exiting...")
        sys.exit()
    elif op == '0':
        os.system( 'clear' ) 
        print("(0) inputing new matrices...")
        print("Enter file1: ", end = "")
        matrixA = fileIO()
        print("Enter file2: ", end = "")
        matrixB = fileIO()
        menu()
    elif op == '1':
        swap(matrixA, matrixB)
        menu()
        print("(1) matrixA and matrixB swapped!")
    elif op == '2':
        menu()
        print("(2) matrixB copied into matrixA!")
        matrixA = matrixB
        menu()
    elif op == '3':
        menu()
        print("(3) matrixA copied into matrixB!")
        matrixB = matrixA
        menu()
    elif op == '4': 
        menu()
        #matrixA = matrixA.T
        print("(4) A^T (transpose):")
        Ta = np.array(transpose(matrixA))
        print(Ta)
    elif op == '5':
        menu()
        print("(5) B^T (transpose):")
        Tb = np.array(transpose(matrixB))
        print(Tb)
    elif op == '6':
        menu()
        print("(6) A + B =")
        add = np.array(add(matrixA,matrixB))
        print(add)
    elif op == '7':
        menu()
        print("(7) A - B = ")
        sub1 = np.array(sub(matrixA,matrixB))
        print(sub1)
    elif op == '8':
        menu()
        print("(8) B - A = ")
        sub2 = np.array(sub(matrixB,matrixA))
        print(sub2)    
    elif op == '9':
        menu()
        while(1):
            try:
                n = input("Enter a number (scalor): ") 
                print("(9) scalar n * A = ")
                nA = np.array(scalor_mult(int(n),matrixA))
                print(nA)
            except Exception:
                print("Error: invalid number (must be integer)")
                print()
                continue
            else:
                break

    elif op == '10':
        menu()
        while(1):
            try:
                n = input("Enter a number (scalor): ") 
                print("(10) scalar n * B = ")
                nB = np.array(scalor_mult(int(n),matrixB))
                print(nB)
            except Exception:
                print("Error: invalid number (must be integer)")
                print()
                continue
            else:
                break

    elif op == '11':
        menu()
        print("(11) A * B =")
        #mul = np.matmul(matrixA, matrixB)
        mult1 = np.array(multiply(matrixA,matrixB))
        print(mult1)
    elif op == '12':
        menu()
        print("(12) B * A =")
        mult2 = np.array(multiply(matrixB,matrixA))
        print(mult2)
    elif op == '13':
        menu()
        while(1):
            try:
                n = input("Enter a number (power): ") 
                print("(13) A^n = ")
                powA = power(int(n),matrixA)
                if powA == None:
                    break

                print("[",end = "")
                for row in powA:
                    if row == powA[len(powA)-1]:
                        print(row, end = "]\n")   
                        break
                    print(row)
            except Exception:
                print("Error: invalid number (must be integer)")
                print()
                continue
            else:
                break

    elif op == '14':
        menu()
        while(1):
            try:
                n = input("Enter a number (power): ") 
                print("(14) B^n = ")
                powB = power(int(n),matrixB) 
                if powB == None:
                    break

                print("[",end = "")                
                for row in powB:
                    if row == powB[len(powB)-1]:
                        print(row, end = "]\n")   
                        break
                    print(row)
            except Exception:
                print("Error: invalid number (must be integer)")
                print()
                continue
            else:
                break

    elif op == '15':
        menu()
        print("(15) det(A) = ", end = "")
        #det = np.linalg.det(matrixA)
        detA = np.array(deternminant(matrixA))
        print(detA)
    elif op == '16':
        menu()
        print("(16) det(B) = ", end = "")
        detB = np.array(deternminant(matrixB))
        print(detB)
    elif op == '17':
        menu()
        print("(17) A^-1 (inverse)  ~ around 1 min to caculate for large matrices:") 
        invA = np.round(inverse(matrixA),5)
        if len(invA) != 0:
            print(invA)
    elif op == '18':
        menu()
        print("(18) B^-1 (inverse)  ~ around 1 min to caculate for large matrices:") 
        invB = np.round(inverse(matrixB),5)
        
        #invB = np.array(inverse(matrixB))
        #invB = np.round(invB)
        if len(invB) != 0:
            print(invB)           
    elif op == '19':
        idA = np.array(identity(matrixA))
        if len(idA) != 0:
            matrixA = idA
            menu()
        else:
            menu()
            print("Error: not a square matrix")
        print("(19) A = I")
    elif op == '20':
        idB = np.array(identity(matrixB))
        if len(idB) !=  0:
            matrixB = idB
            menu()
        else:
            menu()
            print("Error: not a square matrix") 
        print("(20) B = I")
    else:
        print("Error: invalid number")
    
    








