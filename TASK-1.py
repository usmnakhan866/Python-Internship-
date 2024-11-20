def add(a, b):
 return a + b

def subtract(a, b):
 return a - b

def multiply(a, b):
 return a * b

def divide(a, b):
  if b == 0:
   return "Error! Division by zero."
  return a / b

def calculator():
 print("Welcome to Python Calculator")
    
 while True:
   
   print("1. Addition")
   print("2. Subtraction")
   print("3. Multiplication")
   print("4. Division")
   print("E. END")
        
   choice = input("Chose Number to Perfome Operation (1/2/3/4): ")
        
   if choice == 'E':
     print("Exiting the calculator. Goodbye!")
     break
        
   if choice in['1','2','3','4']:
    n1 = float(input("Enter first num: "))
    n2 = float(input("Enter second num: "))
        
    if choice == '1':
     print(n1, "+", n2, "=", add(n1, n2))
    elif choice == '2':
     print(n1, "-", n2, "=", subtract(n1, n2))
    elif choice == '3':
     print(n1, "*", n2, "=", multiply(n1, n2))
    elif choice == '4':
     print(n1, "/", n2, "=", divide(n1, n2))
   else:
       print("Invalid Input")
   print("\n")
 

calculator()