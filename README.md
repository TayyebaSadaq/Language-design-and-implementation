# Custom Language Interpreter

A mini programming language interpreter written in python supporting:
- arithmetic operations
- booleans
- strings
- lists
- conditionals
- loops
- input/outputs

## 🚀 How to run

1. heres how to run the code in the console:
```bash
python interpreter.py
```

2. Type your code in the console and press Enter to execute it.

OR

1. create a file (.txt) with your code to run
2. run the interpreter with the filename as an argument:
```bash
python interpreter.py <filename>
```
*i've provided a sample file `test.txt`*

## 🧠 Language Features and Syntax

### Arithmetic
```bash
x = 10 + 2 * 3
y = (x - 4) / 2
```
### Booleans
```bash
truth = true and not false
print truth
```

### Strings
```bash
greeting = "Hello" + ", " + "world!"
print greeting
```

### Lists
```bash
nums = [1, 2, 3]
nums[0] = 99
print nums[0]
```

### Input/Output
```bash
name = input("Enter your name: ")
print "Welcome, " + name
```

### Print
```bash
print x
print "hello"
print [1, 2, 3]
```

### While Loops
```bash
i = 0
while (i < 3) {
  print i
  i = i + 1
}
```

### If/Else
```bash
if (x > 10) {
  print "big"
} else {
  print "small"
}
```

### Additional Notes
- all numbers are treated as floats
- variables must begin with letter and be alphanumeric
- strings use double quotes, "like this"
- blocks are defined using curly braces, {like this}