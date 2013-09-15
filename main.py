from random import random, randint, choice

class fwrapper(object):
    def __init__(self, function, funcname, varnumber):
        self.function = function
        self.funcname = funcname
        self.varnumber = varnumber

class calcnode(object):
    def __init__(self, fwrapper):
        self.function = fwrapper.function
        self.name = fwrapper.funcname
        self.childnumber = fwrapper.varnumber
        self.children = []

    def evaluate(self, varlist):
        try:
            varlist = [float(var) for var in varlist]
            results = [c.evaluate(varlist) for c in self.children]
            return self.function(results)
        except ZeroDivisionError:
            print "ZeroDivisionError\n"
            varlist = [randint(1, 100) for i in range(len(varlist))]
            return self.evaluate(varlist)

    def draw(self, indent=0):
        print(indent * " " + self.name)
        indent += 1
        [c.draw(indent) for c in self.children]

class numnode(object):
    def __init__(self, value):
        self.value = value
        self.name = str(value)

    def evaluate(self, varlist):
        return float(self.value)

    def draw(self, indent=0):
        print(indent * " " + self.name)

class paramnode(object):
    def __init__(self, rank):
        self.rank = rank
        self.name = "param_" + str(rank)

    def evaluate(self, varlist):
        return varlist[self.rank]

    def draw(self, indent=0):
        print(indent * " " + self.name)

def add(val):
    return sum(val)

def sub(val):
    return val[0] - val[1]

def mul(val):
    return val[0] * val[1]

# if val[1] == 0 ?
def div(val):
    return val[0] / val[1]

fadd = fwrapper(add, "add", 2)
fsub = fwrapper(sub, "sub", 2)
fmul = fwrapper(mul, "mul", 2)
fdiv = fwrapper(div, "div", 2)

fwrappers = [fadd, fsub, fmul, fdiv]

newnode = calcnode(fadd)
child1 = numnode(8)
child2 = paramnode(0)
newnode.children = [child1, child2]
varlist = [333]
print(newnode.evaluate(varlist))

def makerandomtree(varnumber, depth=4):
    if (random() < 0.7):
        if (depth <= 1):
            if random() > 0.5:
                return numnode(randint(1, 10))
            else:
                return paramnode(randint(0, varnumber - 1))
        tree = calcnode(choice(fwrappers))
        depth -= 1
        tree.children = [makerandomtree(varnumber, depth) for i in range(tree.childnumber)]
        return tree
    elif (random() > 0.9):
        return numnode(randint(1, 10))
    else:
        return paramnode(randint(0, varnumber - 1))

# test function: f(x, y, z) = 5*x**3 - 7*y**2 + 6*z + 8
def testfunction(x, y, z):
    return 5*x**3 - 7*y**2 + 6*z + 8

def maketestdata(varnumber, size=20):
    

a = makerandomtree(3)
print a.evaluate([2, 3, 4])
a.draw()