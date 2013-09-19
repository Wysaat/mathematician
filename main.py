from random import random, randint, choice
from copy import deepcopy

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
        varlist = [float(var) for var in varlist]
        results = [c.evaluate(varlist) for c in self.children]
        return self.function(results)

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

def makerandomtree(varnumber, depth=4, top=1):
    randnum = random()
    if top == 1:
        tree = calcnode(choice(fwrappers))
        top = 0
        tree.children = [makerandomtree(varnumber, depth, top) for i in range(tree.childnumber)]
        return tree
    elif randnum < 0.7:
        if (depth <= 1):
            if random() > 0.5:
                return numnode(randint(1, 10))
            else:
                return paramnode(randint(0, varnumber - 1))
        tree = calcnode(choice(fwrappers))
        depth -= 1
        tree.children = [makerandomtree(varnumber, depth, top) for i in range(tree.childnumber)]
        return tree
    elif randnum > 0.9:
        return numnode(randint(1, 10))
    else:
        return paramnode(randint(0, varnumber - 1))

# test function: f(x, y, z) = 5*x**3 - 7*y**2 + 6*z + 8
def testfunction(varlist):
    return 5*varlist[0]**3 - 7*varlist[1]**2 + 6*varlist[2] + 8

def maketestdata(testfunction, varnumber, size=20):
    data = []
    while True:
        if size == 0:
            return data
        varlist = [randint(1, 100) for i in range(varnumber)]
        result = testfunction(varlist)
        dataitem = varlist + [result]
        if dataitem not in data:
            data.append(dataitem)
            size -= 1

def scoretree(tree, data):
    total = 0
    datasize = len(data)
    for dataitem in data:
        try:
            total += (tree.evaluate(dataitem[:-1]) - dataitem[-1]) ** 2
        except ZeroDivisionError:
            datasize -= 1
    return total / datasize

def exchange(tree1, tree2):
    tree = deepcopy(tree1)
    if (random() > 0.8):
        tree.children[randint(0, tree.childnumber - 1)] = tree2
    else:
        alters = [c for c in tree.children if isinstance(c, calcnode)]
        if alters == []:
            tree.children[randint(0, tree.childnumber - 1)] = tree2
        else:
            alter = choice(alters)
            alternum = tree.children.index(alter)
            tree.children[alternum] = exchange(tree.children[alternum], tree2)
    return tree

def change(tree, varnum, depth):
    randnum = random()
    if isinstance(tree, calcnode) and random < 0.9:
        change(choice(tree.children), varnum, depth)
    else:
        tree = makerandomtree(varnum, depth)

#def change(tree, varnum, depth):
#    randnum = random()
#    if isinstance(tree, calcnode) and randnum < 0.9:
#        chosennum = choice(range(tree.childnumber))
#        tree.children[chosennum] = change(tree.children[chosennum], varnum, depth)
#    else:
#        tree = makerandomtree(varnum, depth)
#    return tree

a = makerandomtree(3, 4)

data = maketestdata(testfunction, 3)
for dataitem in data:
    print(dataitem)

score = scoretree(a, data)
print score

b = makerandomtree(3, 4)
c = exchange(a, b)

for tree in [a, b, c]:
    print("---------------------------------------------------------")
    tree.draw()
    print("---------------------------------------------------------")
    print

print("--------------------------------------------------------------------")

tom = makerandomtree(3, 2)
tom.draw()
change(tom, 3, 2)
print("------------------------------------------------")
tom.draw()