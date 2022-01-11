#!/usr/bin/ruby
# course: cmps3500
# CLASS Project (Group 11)
# RUBY IMPLEMENTATION OF A CUSTOM MATRIX CALCULATOR
# date: 5/21/21
# Student 1: Dat Pham 
# description: Implementation of a scientific calculator ...
require 'csv'

$matrixA = []
$matrixB = []

  def swap(m1,m2)
    $matrixA = m2
    $matrixB = m1
  end

  def transpose(m1)
    # build a same-sized array
    arr = Array.new(m1[0].length){Array.new(m1.length)}
    
    # switch rows and columns
    for i in 0..m1[0].length-1 
      for j in 0..m1.length-1  
        arr[i][j] = m1[j][i]
      end
    end 
    return arr 
  end

# scalar n * m[row][col]
  def scalar(n,m)
    
    # iterate through every 1D array in the 2D array, then iterate through 
    # every number in the 1D array, and perform operation
    arr = m.map { |v| v.map{|k| k.to_i * n}}
    return arr
  end

# m1[row][col] + m2[row][col]
  def add(m1,m2)
    temp = []
    if m1.length != m2.length or m1[0].length != m2[0].length
      puts "Error: matrices are not the same dimensions"
      return temp
    end        

    #arr = m1.zip(m2).map { |v1,v2| (v1.is_a? Array) ? add(v1,v2) : v1.to_i + v2.to_i } 
    
    # build a same-sized array
    arr = Array.new(m1.length){Array.new(m1[0].length)}
    
    # iterate through every index of both matrices and add 
    for i in 0..m1.length-1 
      for j in 0..m1[0].length-1  
        arr[i][j] = m1[i][j].to_i + m2[i][j].to_i
      end
    end 
    return arr
  end

# m1[row][col] - m2[row][col] 
  def sub(m1,m2) 
    temp = []
    if m1.length != m2.length or m1[0].length != m2[0].length
      puts "Error: matrices not same dimensions"
      return temp
    end
    
    # build a same-sized array
    arr = Array.new(m1.length){Array.new(m1[0].length)}
    
    # iterate through every index of both matrices and subtract
    for i in 0..m1.length-1 
      for j in 0..m1[0].length-1  
        arr[i][j] = m1[i][j].to_i - m2[i][j].to_i
      end
    end 
    return arr
  end

  def dot_product(a1,a2)
    # zip is like hashing, every element now has a neighbor
    # inject(0) is declaring an outside scope variable with an initial value of 0
    arr = a1.zip(a2).inject(0){ |sum,n| sum.to_i + n[0].to_i * n[1].to_i }
    return arr
  end

#m1[row][col] * m2[row][col]
  def matrix_mult(m1,m2) 
    temp = []
    for i in 0..m1.length-1
      if m1[i].length != m2.length
        puts "Error: matrix1 row do not match matrix2 column"
        return temp
      end
    end
    
    # build an array size of matrix1 row * matrix2 column 
    arr = Array.new(m1.length){Array.new(m2[0].length)}
    
    m2_T = transpose(m2)  # transpose to get matrix2 columns as rows 
    # iterate through every index of both matrices and subtract
    for i in 0..m1.length-1 
      for j in 0..m2_T.length-1  
        arr[i][j] = dot_product(m1[i],m2_T[j])
      end
    end 
    return arr
  end
 
  def pow(n,m)
    temp = []
    if n < 1 || n > 10
      puts "Error: power is outside range (only 1 <= n <= 10 are accepted)"
      return temp
    end
    
    # recusion, keep multiplying matrix by itself until stop condition
    if n == 1
      return m
    else
      return matrix_mult(m,pow(n-1,m))
    end
  end

  def identity(m)
    temp = []
    if m.length != m[0].length
      print "Error: not a square matrix"
      return temp
    end

    # build 2D array of 0's
    arr = Array.new(m.length){Array.new(m[0].length, 0)} 
    
    # set diagonal to 1
    for i in 0..m.length-1
      arr[i][i] = 1
    end
    return arr
  end

  def menu()
    system "clear" # clearing screen

    puts("         MATRIX CALCULATOR           ")
    puts("***************************************")
    puts("0) input new A,B  11) A * B  ")
    puts("1) A <=> B        12) B * A  ")
    puts("2) A = B (copy)   13) A^n, 1 <= n >= 10")  
    puts("3) B = A (copy)   14) B^n, 1 <= n >= 10")
    puts("4) A^T            15) det(A) ")
    puts("5) B^T            16) det(B) ")
    puts("6) A + B          17) A^-1 (inverse) ")
    puts("7) A - B          18) B^-1 (inverse) ")
    puts("8) B - A          19) A = I  ")
    puts("9) n * A          20) B = I  ")  
    puts("10) n * B         Enter 'x' to exit ")
    puts
    puts "matrixA: "
    $matrixA.each do |row|
      puts row.inspect
    end
    puts "matrixB: "
    $matrixB.each do |row|
      puts row.inspect
    end
    puts
  end

  def fileIO()
    while(1)
      begin
        alphabet = ('A'..'Z').to_a + ('a'..'z').to_a        
        file = $stdin.gets.chomp
        temp = CSV.read(file)
        temp.map { |v| 
          v.map { |k| 
            if alphabet.include? k[0]
              puts
              puts "Error: matrix contains a string"
              print "Enter another file: "
              temp = fileIO()
              break
             
            elsif k.include? '.'
              puts
              puts "Error: matrix contains a float"
              print "Enter another file: "
              temp = fileIO()
              break
            end
          }
        }
        temp = temp.map {|v| v.map{|k| k.to_i}}
        return temp
      rescue
        puts
        puts "Error: file not found or invalid matrix"
        print "Enter another file: "
        retry
      else
        break
      end
    end
  end

print "Enter file1: "
$matrixA = fileIO()
print "Enter file2: "
$matrixB = fileIO()

menu()
while(1)
  print "Enter operation number: "
  op = $stdin.gets.chomp
  
  if op  == 'x' or op == 'X'
    puts "exiting... "
    exit
  elsif op == '0'
    puts "(0) inputing new matrices... "
    puts
    print "Enter file1: "
    $matrixA = fileIO()
    print "Enter file2: "
    $matrixB = fileIO()
    menu()
  elsif op == '1'
    swap($matrixA,$matrixB)
    menu()
    puts "(1) A <=> B " 
    puts "matrixA and matrixB swapped!"
    puts
  elsif op == '2'
    $matrixA = $matrixB
    menu()
    puts "(2) matrixB is copied into matrixA!"
    puts
  elsif op == '3'
    $matrixB = $matrixA
    menu()
    puts "(3) matrixA is copied into matrixB!"
    puts 
  elsif op == '4'
    menu()
    puts "(4) matrixA Transpose: "
    trans = transpose($matrixA)
    trans.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '5'
    menu()
    puts "(5) matrixB Transpose: "
    trans = transpose($matrixB)
    trans.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '6'
    menu()
    puts "(6) matrixA + matrixB ="
    add = add($matrixA,$matrixB)
    add.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '7'
    menu()
    puts "(7) matrixA - matrixB ="
    sub = sub($matrixA,$matrixB)
    sub.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '8'
    menu()
    puts "(8) matrixB - matrixA ="
    sub = sub($matrixB,$matrixA)
    sub.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '9'
    menu()
    while(1)
      begin
        print "Enter a number (scalor): "
        n = $stdin.gets.chomp 
        puts "(9) n * matrixA = "
        scalarA = scalar(n.to_i,$matrixA)
        scalarA.each do |row|
          puts row.inspect
        end
      rescue
        puts "Error: invalid number (must be an integer)"
        puts
        retry
      else
        break
      end
    end
    puts 
  elsif op == '10'
    menu()
    while(1)
      begin
        print "Enter a number (scalor): "
        n = $stdin.gets.chomp
        puts "(10) n * matrixB = "
        scalarB = scalar(n.to_i,$matrixB)
        scalarB.each do |row|
          puts row.inspect
        end
      rescue
        puts "Error: invalid number (must be an integer)"
        puts
        retry
      else
        break
      end
    end
    puts
  elsif op == '11'
    menu()
    puts "(11) A * B = "
    mult = matrix_mult($matrixA,$matrixB)
    mult.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '12'
    menu()
    puts "(12) B * A = "
    mult = matrix_mult($matrixB,$matrixA)
    mult.each do |row|
      puts row.inspect
    end
    puts
  elsif op == '13'
    menu()
    while(1)
      begin
        print "Enter a number (power): "
        n = $stdin.gets.chomp
        puts "(13) A^n ="
        powA = pow(n.to_i,$matrixA)
        powA.each do |row|
          puts row.inspect
        end
      rescue
        puts "Error: invalid number (must be an integer)"
        puts
        retry
      else
        break
      end
    end
    puts
  elsif op == '14'
    menu()
    while(1)
      begin
        puts "(14) B^n ="
        print "Enter a number (power): "
        n = $stdin.gets.chomp 
        powB = pow(n.to_i,$matrixB)
        powB.each do |row|
          puts row.inspect
        end
      rescue
        puts "Error: invalid number (must be an integer)"
        puts
        retry
      else
        break
      end
    end
    puts
  elsif op == '19'
    $matrixA = identity($matrixA)
    menu()
    puts "(19) A = I"
    puts
  elsif op == '20'
    $matrixB = identity($matrixB)
    menu()
    puts "(20) B = I"
    puts 
  else
    puts "Error: invalid number"
  end
end


