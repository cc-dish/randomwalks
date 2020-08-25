import numpy as np
from itertools import permutations

# calculating some special moore-penrose-defined resistances for directed graphs

class network:

	def __init__(self, A):										# A is the adjacency matrix; it must be square		
		self.A = A

		if (A.shape[0] != A.shape[1]):
			raise Exception("SquareMatrixError")
		else:
			self.n = A.shape[0]

		self.L = np.zeros((self.n,self.n))						# L is out-Laplacian
		self.M = np.zeros((self.n,self.n))						# M is in-Laplacian
		self.Li = np.zeros((self.n, self.n))					# Li & Mi are pseudoinverses
		self.Mi = np.zeros((self.n, self.n))					

		self.makeLaps()																			

	def makeLaps(self):																			# generates the laplacians
		one = np.ones((self.n,1))

		self.L = np.diagflat(np.matmul(A, one)) - A
		self.M = np.diagflat(np.matmul(np.transpose(A), one)) - A

		self.Li = np.linalg.pinv(self.L)
		self.Mi = np.linalg.pinv(self.M)

		print("L:")
		print(self.L)
		print("Linv:")
		print(self.Li)
		print("M:")
		print(self.M)
		print("Minv:")
		print(self.Mi)



	def resistanceformula(self, formula=1):														# returns resistance matrix given inverted matrix and choice of formula

		O = np.zeros((self.n,self.n))						# O is resistance matrix
		
		for i in range(self.n):
			for j in range(self.n):
				O[i,j] = {

# INSERT FORMULAS HERE

					1: self.Li[i,i] + self.Li[j,j] - 2*self.Li[i,j],
					2: self.Li[i,i] - self.Li[i,j] + self.Mi[j,j] - self.Mi[j,i],
					3: self.Li[i,i] - self.Mi[i,j] + self.Mi[j,j] - self.Li[j,i]
				}[formula]

		print("Resistances:")
		print(np.round(O,3))

		self.checktriangle(O)

	def checktriangle(self, O):

		EPSILON = 0.00001 									# account for float imprecision


		fails = 0
		for perm in permutations(range(self.n), 3):
			if (O[perm[0], perm[1]] + O[perm[1], perm[2]] + EPSILON < O[perm[0], perm[2]]):
				fails = 1
				print("Triangle FAILS at " + str((perm[0] + 1, perm[1] + 1, perm[2] + 1)) + " [indexing starts from 1]" )
				break

		if (fails==0):
			print("Triangle HOLDS.")


# SET INCEDENCE MATRIX HERE

A = np.array([
	[0, 1, 0],
	[0, 0, 3], 
	[0, 0, 0]
	])


# CHOOSE FORMULA HERE

network(A).resistanceformula(2)

