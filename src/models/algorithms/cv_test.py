"""
Test cases for cumulative voting algorithm.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import cv
import unittest


class TestCumulativeVoting(unittest.TestCase):

	def test_empty(self):
		for ballots in [[],[{},{}]]:
			winners = cv.run_cv(ballots, 2)
			self.assertEqual(winners, [])


	def test_simple(self):
		ballots = [
			{'Awesome': 5}
		]
		winners = cv.run_cv(ballots, 1)
		self.assertEqual(winners, ['Awesome'])

	def test_simple_tie(self):
		ballots = [
			{'Awesome': 5, 'Slice': 5}
		]
		winners = cv.run_cv(ballots, 1)
		self.assertSetEqual(set(winners), set(['Awesome', 'Slice']))

	def test_counting(self):
		ballots = [
			{'Awesome': 2},
			{'Slice': 1, 'Awesome': 1},
			{'Awesome': 2},
			{'Slice': 2},
			{'Bluesy': 1},
			{}
		]
		winners = cv.run_cv(ballots, 1)
		self.assertEqual(winners, ['Awesome'])
		winners = cv.run_cv(ballots, 2)
		self.assertSetEqual(set(winners), set(['Awesome', 'Slice']))
		winners = cv.run_cv(ballots, 3)
		self.assertSetEqual(set(winners), set(['Awesome', 'Slice', 'Bluesy']))

	def test_counting_tie(self):
		ballots = [
			{'Awesome': 1, 'Slice': 1},
			{'Slice': 1, 'Bluesy': 1},
			{'Slice': 2},
			{'Awesome': 1, 'Bluesy': 1},
			{'Awesome': 2}
		]
		winners = cv.run_cv(ballots, 1)
		self.assertSetEqual(set(winners), set(['Awesome', 'Slice']))

if __name__ == '__main__':
	unittest.main()