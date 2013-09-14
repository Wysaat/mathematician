from random import random, randint, choice

class fwrapper(object):
	def __init__(self, function, varnumber):
		self.function = function
		self.varnumber = varnumber

class calcnode(object):
	def __init__(self, fwrapper):
		self.function = fwrapper.function
		self.childnumber = fwrapper.varnumber
		self.children = []

	def evaluate(self, varlist):
		results = [c.evaluate(varlist) for c in self.children]
		return self.function(results)

class numnode(object):
	def __init__(self, value):
		self.value = value

	def evaluate(self, varlist):
		return self.value

class paramnode(object):
	def __init__(self, rank):
		self.rank = rank

	def evaluate(self, varlist):
		return varlist[self.rank]

def add(val):
	return sum(val)

def sub(val):
	return val[0] - val[1]

def mul(val):
	return val[0] * val[1]

# if val[1] == 0 ?
def div(val):
	return val[0] / val[1]

fadd = fwrapper(add, 2)
fsub = fwrapper(sub, 2)
fmul = fwrapper(mul, 2)
fdiv = fwrapper(div, 2)

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

a = makerandomtree(3)
print a.evaluate([2, 3, 4])