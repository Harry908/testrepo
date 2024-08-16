# Huy Ky - 011833522

#------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
import sys


opstack = []  #assuming top of the stack is the end of the list

# Now define the helper functions to push and pop values on the opstack
# (i.e, add/remove elements to/from the end of the Python list)
# Remember that there is a Postscript operator called "pop" so we choose
# different names for these functions.
# Recall that `pass` in python is a no-op: replace it with your code.

def opPop():
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.
    if len(opstack) > 0:
         return opstack.pop()
    return None
    
def opPush(value):
    opstack.append(value)

#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  #assuming top of the stack is the end of the list

# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    if len(dictstack) > 0:
        return dictstack.pop()
    return None
    # dictPop pops the top dictionary from the dictionary stack.

def dictPush(d):
    dictstack.append(d)
    #dictPush pushes the dictionary ‘d’ to the dictstack.
    #Note that, your interpreter will call dictPush only when Postscript
    #“begin” operator is called. “begin” should pop the empty dictionary from
    #the opstack and push it onto the dictstack by calling dictPush.

def define(name, value):
    if dictstack:
        dictstack[-1][name] = value
    else:
        dictPush({name:value})
    #add name:value pair to the top dictionary in the dictionary stack.
    #Keep the '/' in the name constant.
    #Your psDef function should pop the name and value from operand stack and
    #call the “define” function.

def lookup(name):
    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.
    if dictstack:
        key = "/" + name # add '/' (dict store '/name')
        # Look for value in stacks
        for ndict in reversed(dictstack):
            if key in ndict:
                return ndict[key]
        else:
            raise KeyError("{} is not defined!".format(name))
    else:
        raise KeyError("{} is not defined!".format(name))

#--------------------------- 10% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, div, mod, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters
# and types of the parameters are correct.

def add():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        if isNumber(opR) and isNumber(opL):
            opPush(opL + opR)
        else:
            opPush(opL)
            opPush(opR)
            raise TypeError("Both operands must be numbers!")
    else:
        raise ValueError("Insufficient operands!")

def sub():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        if isNumber(opR) and isNumber(opL):
            opPush(opL- opR)
        else:
            opPush(opL)
            opPush(opR)
            raise TypeError("Both operands must be numbers!")
    else:
        raise ValueError("Insufficient operands!")

def mul():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        if isNumber(opR) and isNumber(opL):
            opPush(opL * opR)
        else:
            opPush(opL)
            opPush(opR)
            raise TypeError("Both operands must be numbers!")
    else:
        raise ValueError("Insufficient operands!")

def div():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        if opR == 0:
            opPush(opR)
            raise ValueError("Divided by 0!")
        if isNumber(opR) and isNumber(opL):
            opPush(opL/opR)
        else:
            opPush(opL)
            opPush(opR)
            raise TypeError("Both operands must be numbers!")
    else:
        raise ValueError("Insufficient operands!")

def mod():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        if opR == 0:
            opPush(opR)
            raise ValueError("Divided by 0!")
        if isNumber(opR) and isNumber(opL):
            opPush(opL % opR)
        else:
            opPush(opL)
            opPush(opR)
            raise TypeError("Both operands must be numbers!")
    else:
        raise ValueError("Insufficient operands!")

def eq():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        opPush(opL == opR)
    else:
        raise ValueError("Insufficient operands!")

def lt():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        opPush(opL < opR)
    else:
        raise ValueError("Insufficient operands!")

def gt():
    if len(opstack) >= 2:
        opR = opPop()
        opL = opPop()
        opPush(opL > opR)
    else:
        raise ValueError("Insufficient operands!")

#--------------------------- 15% -------------------------------------
# String operators: define the string operators length, get, getinterval, put
def length():
    if len(opstack) >= 1:
        opStr = opPop()
        if isString(opStr):
            opPush(len(opStr)-2) # minus the parentheses
        else:
            opPush(opStr)
            raise TypeError("Operand is not a string!")
    else:
        raise ValueError("Insufficient operands!")

def get():
    if len(opstack) >= 2:
        index = opPop()
        opStr = opPop()
        
        # Error checking
        if not isinstance(index,int):
            opPush(opStr)
            opPush(index)
            raise TypeError("Index must be integer!")
        if not isString(opStr):
            opPush(opStr)
            opPush(index)
            raise TypeError("Operand is not a string!")
        if index < 0 or index >= len(opStr) - 2:
            opPush(opStr)
            opPush(index)
            raise IndexError("Index out of bound!")
        # Remove parentheses.
        string = opStr[1:-1]
        opPush(ord(string[index]))
    else:
        raise ValueError("Insufficient operands!")

def getinterval():
    if len(opstack) >= 3:
        count = opPop()
        index = opPop()
        opStr = opPop()
        
        # Error checking
        if not isinstance(index,int) or not isinstance(count,int):
            opPush(opStr)
            opPush(index)
            opPush(count)
            raise TypeError("Index and count must be integer!")
        if not isString(opStr):
            opPush(opStr)
            opPush(index)
            opPush(count)
            raise TypeError("Operand is not a string!")
        if index < 0 or count < 0 or index + count >= len(opStr) - 2:
            opPush(opStr)
            opPush(index)
            opPush(count)
            raise IndexError("Invalid range!")
        if count == 0:
            opPush("()")
            return
        string = opStr[1:-1]
        interval = string[index:index+count]
        opPush('('+interval+')')
    else:
        raise ValueError("Insufficient operands!")

def put():
    if len(opstack) >= 3:
        ascii = opPop()
        index = opPop()
        opStr = opPop()
        
        # Error checking
        if not isinstance(index,int) or not isinstance(ascii,int):
            opPush(opStr)
            opPush(index)
            opPush(ascii)
            raise TypeError("Index and Ascii value must be integer!")
        if not isString(opStr):
            opPush(opStr)
            opPush(index)
            opPush(ascii)
            raise TypeError("Operand is not a string!")
        if index < 0 or ascii < 0 or index >= len(opStr) - 2:
            opPush(opStr)
            opPush(index)
            opPush(ascii)
            raise IndexError("Invalid range!")
        if not (0<= ascii <= 127):
            raise ValueError("Invalid ascii value!")
        newStr = opStr[1:-1]
        newStr = newStr[:index] + chr(ascii) + newStr[index+1:]
        
        putUpdate('('+newStr+')',opStr)
        
    else:
        raise ValueError("Insufficient operands!")

def putUpdate(newString, oldString):
    oldID = id(oldString)
    for index, item in enumerate(opstack):
        if id(item) == oldID:
            opstack[index] = newString
    if dictstack:
        topDict = dictstack[-1]
        for key,value in topDict.items():
            if id(value) == oldID:
                topDict[key] = newString
                
    

#--------------------------- 25% -------------------------------------
# Define the stack manipulation and print operators: dup, copy, pop, clear, exch, roll, stack
def dup():
    if opstack:
        op = opPop()
        opPush(op)
        opPush(op)
    else:
        raise SystemError("Stack empty!")

def copy():
    if opstack:
        count = opPop()
        if count > len(opstack) or count < 0:
            opPush(count)
            raise ValueError("Range invalid!")
        copyStack= opstack[-count:]
        opstack.extend(copyStack)
    else:
        raise SystemError("Stack empty!")
    

def pop():
    opPop()

def clear():
    opstack.clear()

def exch():
    if len(opstack) >= 2:
        op1 = opPop()
        op2 = opPop()
        opPush(op1)
        opPush(op2)
    else:
        raise SystemError("Stack empty!")

def roll():
    if len(opstack) >= 3:
        i = opPop()
        n = opPop()
        if not isinstance(i,int) or not isinstance(n,int):
            opPush(n)
            opPush(i)
            raise TypeError("n and i value must be integer!")
        if n > len (opstack) or n < 0:
            opPush(n)
            opPush(i)
            raise IndexError("Range invalid")
        if i == 0:
            return
        if i > 0:
            for _ in range(i):
                # Extract the portion needed to be rolled
                elements = opstack[-n:]
                # Rolling element
                rolled_element = elements.pop()
                elements.insert(0, rolled_element)
                # Add rolled list back to opstack
                opstack[-n:] = elements
        elif i < 0:
            for _ in range(abs(i)):
                # Extract the portion needed to be rolled
                elements = opstack[-n:]
                # Roll the first element of the extracted to the last position
                rolled_element = elements.pop(0)
                elements.append(rolled_element)
                # Update the opstack with the rolled elements
                opstack[-n:] = elements
    else:
        raise ValueError("Insufficient operands!")

def stack():
    for op in reversed(opstack):
        print(op)

# Helper functions for type checking
def isNumber(value):
    return isinstance(value,(int,float))

def isString(value):
    return isinstance(value,(str))

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.

def psDict():
    if opstack:
        size = opPop() #ignored python doesn't limit dictionary size.
        newDict = dict()
        opPush(newDict)
    else:
        raise SystemError("Stack empty")
def begin():
    newDict = opPop()
    dictPush(newDict)

def end():
    dictPop()

def psDef():
    value = opPop()
    name = opPop()
    define(name,value)
    
# - Part2

# Condition and loop operators

def psIf():
    if len(opstack) >=2:
        codeBlock = opPop()
        condition = opPop()
        if isinstance(condition, bool):
            if condition:
                # execute code block
                interpretSPS(codeBlock)
        else:
            opPush(condition)
            opPush(codeBlock)
            raise TypeError("Invalid condition!")
    else:
        raise ValueError("Insufficient operands!")

# Ifesle
def psIfelse():
    if len(opstack) >=3:
        elseBlock = opPop()
        trueBlock = opPop()
        condition = opPop()
        if isinstance(condition, bool):
            if condition:
                # execute true block
                interpretSPS(trueBlock)
            else:
                # execute else block
                interpretSPS(elseBlock)
        else:
            opPush(condition)
            opPush(trueBlock)
            opPush(elseBlock)
            raise TypeError("Invalid condition!")
    else:
        raise ValueError("Insufficient operands!")

# For loop also prevent infinite loop.
def psFor():
    if len(opstack) >=4:
        codeBlock = opPop()
        stop = opPop()
        step = opPop()
        start= opPop()
        if step == 0:
            # Postscript would still enter infinite loop
            raise ValueError("Increment cannot be 0!")
        elif step > 0:
            for i in range(start, stop + 1, step):
                opPush(i)
                interpretSPS(codeBlock)
        else:
            for i in range(start, stop - 1, step):
                opPush(i)
                interpretSPS(codeBlock)
    else:
        raise ValueError("Insufficient operands!") 
    

import re
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)


# complete this function
# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code array for the inner
            # paranthesis, it will be appended to the list we are constructing
            # as a whole.
            res.append(groupMatching2(it))
        else:
            res.append(converter(c))
    return False


# Complete this function
# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    L = tokenize(L)
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false since there is
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            res.append(groupMatching2(it))
        else:
            res.append(converter(c))
    return res

# Convert string into number and booleans.
def converter(token):
    try:
        return int(token)  # Try converting to integer
    except ValueError:
        if token == 'true':
            token = True
            return token
        elif token == 'false':
            token = False
            return token
        else:
            return token  # Leave as is for other cases

# Write the necessary code here; again write
# auxiliary functions if you need them. This will probably be the largest
# function of the whole project, but it will have a very regular and obvious
# structure if you've followed the plan of the assignment.

# Handle code array
def interpretSPS(code): # code is a code array
    for item in code:
        if isString(item): # String need to be processed
            if item in functionDict: # Check for function and execute
                try:
                    functionDict[item]()
                except Exception as e:
                    # Print out an error message if something goes wrong during function execution.
                    print(f"Error executing function: --{item}-- ({e})")
            elif not item.startswith(('/','(')): # Load variable
                try:
                    variable = lookup(item)
                    if isinstance(variable,list): # Execute if variable is a code block
                        interpretSPS(variable)
                    else: # Push the value.
                        opPush(variable)
                except Exception as e:
                    print(f"Error: {e}")
            else: # String constants and names
                opPush(item)
        else: # Number and code array doesn't matter
            opPush(item)
    return

# Interpret input
def interpreter(s): # s is a string
    interpretSPS(parse(s))

#clear opstack and dictstack
def clear():
    del opstack[:]
    del dictstack[:]

def psEqual():
    if opstack:
        print(opPop())
    else:
        raise ValueError("Insufficient operands!")

# Functions dictionary
functionDict = {
    # Arithmethic operators:
    'add': add, 'sub': sub, 'mul': mul, 'div': div,
    'mod': mod, 'eq': eq, 'lt': lt, 'gt': gt,
    
    # String operators:
    'length': length, 'get': get, 'getinterval': getinterval, 'put': put,
    
    # Stack operators:
    'dup': dup, 'copy': copy, 'clear': clear, 'exch':exch, 'roll': roll,
    'pop':opPop, '=':psEqual,
    
    # Dictionary operator
    'dict': psDict, 'begin': begin, 'end': end, 'def': psDef,
    
    # Print
    'stack': stack,
    
    # Loop, conditions
    'if': psIf, 'ifelse': psIfelse, 'for': psFor,
}

#testing

input1 = """
        /square {
               dup mul
        } def
        (square)
        4 square
        dup 16 eq
        {(pass)} {(fail)} ifelse
        stack
        """

input2 ="""
    (facto) dup length /n exch def
    /fact {
        0 dict begin
           /n exch def
           n 2 lt
           { 1}
           {n 1 sub fact n mul }
           ifelse
        end
    } def
    n fact stack
    """

input3 = """
        /fact{
        0 dict
                begin
                    /n exch def
                    1
                    n -1 1 {mul} for
                end
        } def
        6
        fact
        stack
    """

input4 = """
        /lt6 { 6 lt } def
        1 2 3 4 5 6 4 -3 roll
        dup dup lt6 {mul mul mul} if
        stack
        clear
    """

input5 = """
        (CptS355_HW5) 4 3 getinterval
        (355) eq
        {(You_are_in_CptS355)} if
         stack
        """

input6 = """
        /pow2 {/n exch def
               (pow2_of_n_is) dup 8 n 48 add put
                1 n -1 1 {pop 2 mul} for
              } def
        (Calculating_pow2_of_9) dup 20 get 48 sub pow2
        stack
        """

debugging = True
def debug(*s):  
    if debugging:  
        print(*s)

debug(tokenize(input1))
debug(parse(input1))
debug(parse(input2))
debug(parse(input3))
debug(parse(input4))
debug(parse(input5))
debug(parse(input6))

# Tests
if debugging:
    interpreter(input1)
    clear()
    interpreter(input2)
    clear()
    interpreter(input3)
    clear()
    interpreter(input4)
    clear()
    interpreter(input5)
    clear()
    interpreter(input6)

    # New Tests
    clear()
    interpreter("3 5 add stack")

    # Postscript interface:
    clear()
    code = input("PS> ")
    while code != 'exit':
        interpreter(code)
        if len(opstack) == 0:
            prompt = "PS> "
        else:
            prompt = f"PS<{len(opstack)}> "
        code = input(prompt)