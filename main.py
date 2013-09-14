from random import random, randint, choice

class fwrapper(object):
	def __init__(self, function, varnumber):
		self.function = function
		self.varnumber = varnumber

class calcnode(object):
	def __init__(self, fwrapper):
		self.function = fwrapper.function
		self.childnumber = fwrapper.varnumber

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

fadd = fwrapper(add, 2)

newnode = calcnode(fadd)
child1 = numnode(8)
child2 = paramnode(0)
newnode.children = [child1, child2]
varlist = [333]
print(newnode.evaluate(varlist))

def makerandomnode():
	top = 1
	if random() < 0.7 and top == 1:
		tree = calcnode(choice(fwrappers))
	pass