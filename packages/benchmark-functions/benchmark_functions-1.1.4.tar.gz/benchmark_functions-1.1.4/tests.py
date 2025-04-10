#!/usr/bin/env python3

import unittest as ut
import sys, logging
from benchmark_functions import benchmark_functions as bf

DIFFERENCE_THRESHOLD = 1e-6

FUNCTIONS_TO_TEST = [ # parametric functions are excluded, they will be tested separately
	bf.Hypersphere, 
	bf.Hyperellipsoid, 
	bf.Ackley,
	bf.Rosenbrock,
	bf.Rastrigin,
	bf.Schwefel,
	bf.Griewank,
	bf.Ackley,
	bf.Michalewicz,
	bf.EggHolder, 				# <- bad for t<=1e-7, good for t>=1e-6
	bf.Keane,
	bf.Rana, 							# <- bad for t<=1e-7, good for t>=1e-6
	bf.Easom,
	bf.DeJong5,
	bf.GoldsteinAndPrice,
	bf.PichenyGoldsteinAndPrice,
	bf.StyblinskiTang,
	bf.McCormick,
	bf.MartinGaddy,
	bf.Schaffer2,
	bf.Himmelblau,
	# bf.PitsAndHoles # <- it takes too long
	]
# DeJong3 tested separately (too expensive producing all the optima)


def within_bounds(x, lb, ub):
	return x>=lb and x<=ub

class TestMetadata(ut.TestCase):
	def test_loading(self):
		for c in FUNCTIONS_TO_TEST:
			f = c()
			try:
				f.load_info()
			except Exception as e:
				self.fail(f"In loading metadata of function {f.name()}, found error {e}")		
	# a simple test to see if all the references load properly
	def test_all_references(self):
		for c in FUNCTIONS_TO_TEST:
			f = c()
			try:
				f.reference()
			except Exception as e:
				self.fail(f"In loading the reference of function {f.name()} found error {e}")

class TestOptima(ut.TestCase):
	def test_minima(self):
		log = logging.getLogger("TestOptima")
		for c in FUNCTIONS_TO_TEST:
			f=c()
			f.load_info()
			n_minima = f.n_minima()
			if '*' in n_minima:
				del n_minima['*']
				for i in range(1,11):
					if not i in n_minima:
						n_minima[i]=1
			for k in n_minima:
				if k==2:
					f=c() # this is a workaround for functions defined only for 2 dimensions
				else:
					f=c(n_dimensions=k)
				log.debug(f"Testing minima of {f.name()} for D={k}")
				for m in f.minima():
					res = f.testLocalMinimum(m.position,strict=m.region_type == 'convex', score_threshold=DIFFERENCE_THRESHOLD)
					if not res[0]:
						self.fail(f"In function {f.name()} local minimum {m} is invalid: {res[2]}")
						
	def test_DeJong3(self):
		log = logging.getLogger("TestOptima")
		for k in range(1,4):
			f = bf.DeJong3(n_dimensions=k)
			log.debug(f"Testing minima of {f.name()} for D={k}")
			minima = f.minima()
			self.assertEqual(len(minima),pow(8,k))
			for m in minima:
				lb, ub = f.suggested_bounds()
				for i in range(k):
					self.assertTrue(within_bounds(m[i], lb[i], ub[i]))
				res = f.testLocalMinimum(m.position,strict=m.region_type == 'convex', score_threshold=DIFFERENCE_THRESHOLD)
				if not res[0]:
					self.fail(f"In function {f.name()} local minimum {m} is invalid: {res[2]}")



if __name__=='__main__':
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	ut.main()
