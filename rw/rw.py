import numpy as np
import random
import visualize
from matplotlib import pyplot as plt

ROUND = 4													# decimal places to round norm till
DIMFROM = 5
TILL = 36
SAMPLE = 10000

class rwalk():
	def __init__(self, dim = 2, n = 5000):
		self.dim = dim
		self.n = n
		self.current = np.zeros(dim, int)
		self.visited = {tuple((self.current).tolist()):1}	# storing visited locations as tuples (nd array not hashable) and storing number of visits to it
		
		self.path = [tuple((self.current).tolist())]		# storing the path traversed as tuples
		self.normpath = [0.0]								# storing the path of norms
		self.linnormpath = [0]								# storing the path of lattice distances
		self.distinctcount = [1]							# storing the number of distinct points visited 

		self.maxnorm = 0.0


		self.possible = []									# possible vectors of movement (simple)
		for i in range(dim):								# creating this possible list
			a = np.zeros(dim, int)
			b = np.zeros(dim, int)
			a[i] = 1
			self.possible.append(a)
			b[i] = -1
			self.possible.append(b)


	def next(self):											# moves to next position, calls recorder function
		available = [(self.current + s) for s in self.possible]
		new = random.choice(available)
		self.current = new
		self.__record(tuple((self.current).tolist()))


	def __record(self, cur):								# records visited location as tuple:visitcount in visited dictionary
		norm = round(np.linalg.norm(cur), ROUND)			# and records visited norms as norm:visitcount in normvisited dictionary

		if cur in self.visited:								# stores visitedlocations&count and stores into distinctcount 
			self.visited[cur] += 1
			self.distinctcount.append(self.distinctcount[-1])
		else:
			self.visited[cur] = 1
			self.distinctcount.append(self.distinctcount[-1] + 1)

		self.path.append(cur)								# stores path
		self.normpath.append(norm)
		self.linnormpath.append(sum([abs(x) for x in cur]))



	def proceed(self):										# begins(or continues) the random walk
		for i in range(self.n):
			self.next()
		self.__finish()
	

	def __finish(self):										# finish off by printing/storing required details
		#print(self.current)									# printing final point
		#self.plotsdistinct()
		#print(self.distinctcount[-1])
		pass


	def plotsdistinct(self):								# plots number of distinct points visited vs number of points visited until some time
		self.proceed()
		plt.title("Number of distinct points visited (dim = " + str(self.dim) + ")")
		plt.ylabel('Distinct points visited')
		plt.xlabel('Steps talken')
		plt.plot(list(range(len(self.distinctcount))), self.distinctcount)
		plt.show()

	def returndistinct(self):								# returns number of distinct points visited
		self.proceed()
		return self.distinctcount[-1]

	def plotoccupation(self):								# plots occupation measure as histogram (choice of buckets is arbitrary)
		self.proceed()

		plt.title("Time spent at distance from start (dim = " + str(self.dim) + ")")
		plt.ylabel('Number of steps at distance range')
		plt.xlabel('Distance from origin (along lattice)')
		plt.hist(self.linnormpath,10)
		plt.show()





# MY OWN THINGS

def distvsdimfn(x):												# this is what the curve seems to look like
	return ((2*x-4)/(2*x-3))

def distinctvsdim():

	frac = []
	numbers = []
	for i in range(DIMFROM,TILL):
		frac.append(rwalk(i,SAMPLE).returndistinct()/SAMPLE)
		numbers.append(i)

	finputs = list(np.linspace(DIMFROM,TILL, 1000))							# my hypothesis curve

	plt.title('Dimension vs (number of distinct points visited after ' + str(SAMPLE) + ' steps)/' + str(SAMPLE))
	plt.ylabel('Fraction of new points')
	plt.xlabel('Dimension')
	

	data = plt.plot(numbers, frac, 'ro', label="Simulation")
	hyp = plt.plot(finputs, [distvsdimfn(i) for i in finputs], color = 'black', label="f(d) = (2d-4)/(2d-3))")	# showing hypothesis curve

	plt.legend(loc='lower right')
	plt.show()

distinctvsdim()
#rwalk(5,SAMPLE).plotsdistinct()
#rwalk(2,SAMPLE).plotoccupation()

