def enhance(input):
    return input[0] + input + input[-1]

def reverse(input):
    return input[::-1]

def chop(input):
    if len(input) == 1:
        return input
    return input[:-1]

def trim(input):
    if len(input) <= 2:
        return input
    return input[1:-1]

def split(input):
    return input[:(len(input)-1)//2+1]