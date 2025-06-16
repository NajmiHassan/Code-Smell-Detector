# This function is long and has too many parameters
def too_many_params_and_long(a, b, c, d, e, f, g):
    x = a + b
    y = c + d
    z = e + f
    total = x + y + z + g
    print("Step 1")
    print("Step 2")
    print("Step 3")
    print("Step 4")
    print("Step 5")
    print("Step 6")
    print("Step 7")
    return total

# A small, clean function (should be fine)
def add(a, b):
    return a + b

# Duplicated code block starts here
def example_one():
    print("Loading data...")
    print("Processing data...")
    print("Saving results...")

def example_two():
    print("Loading data...")
    print("Processing data...")
    print("Saving results...")
