# This file is part of pydd package.

# pydd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pydd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pydd. If not, see <http://www.gnu.org/licenses/>.

#! /usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../pyddlib/'))

from pyddlib.bdd import BDD

import unittest

class TestBDD(unittest.TestCase):

	@classmethod
	def setUp(cls):
		# terminal nodes
		cls.one = BDD.one()
		cls.zero = BDD.zero()
		# variables
		cls.x1 = BDD.variable(1)
		cls.x2 = BDD.variable(2)
		cls.x3 = BDD.variable(3)

	def test_terminal_one_node(self):
		self.assertTrue(self.one.is_one())
		self.assertFalse(self.one.is_zero())
		self.assertTrue(self.one.is_terminal())
		self.assertFalse(self.one.is_variable())
		self.assertTrue(self.one._high == self.one._low == None)
		self.assertTrue(self.one._value)
		self.assertEqual(self.one._index, -1)

	def test_terminal_zero_node(self):
		self.assertTrue(self.zero.is_zero())
		self.assertFalse(self.zero.is_one())
		self.assertTrue(self.zero.is_terminal())
		self.assertFalse(self.zero.is_variable())
		self.assertTrue(self.zero._high == self.zero._low == None)
		self.assertFalse(self.zero._value)
		self.assertEqual(self.zero._index, -1)

	def test_variable_node(self):
		vars = [ self.x1, self.x2, self.x3 ]
		for index, var in enumerate(vars):
			self.assertTrue(var.is_variable())
			self.assertFalse(var.is_terminal())
			self.assertFalse(var.is_one())
			self.assertFalse(var.is_zero())
			self.assertEqual(var._index, index+1)
			self.assertTrue(var._high._value)
			self.assertFalse(var._low._value)
			self.assertTrue(var._value is None)

	def test_reduce(self):
		one  = self.one
		zero = self.zero
		self.assertEqual(BDD.reduce(one),  one)
		self.assertEqual(BDD.reduce(zero), zero)

		vars = [ self.x1, self.x2, self.x3 ]
		self.assertEqual([BDD.reduce(var) for var in vars], vars)

		# Reference [1] - Figure 5
		dd1 = BDD(-1, None, None, True)
		dd2 = BDD(-1, None, None, False)
		dd3 = BDD(-1, None, None, True)
		dd4 = BDD(-1, None, None, False)
		dd5 = BDD(3, dd2, dd1, None)
		dd6 = BDD(3, dd2, dd3, None)
		dd7 = BDD(2, dd6, dd5, None)
		dd8 = BDD(2, dd4, dd6, None)
		dd9 = BDD(1, dd8, dd7, None)
		rdd9 = BDD.reduce(dd9)
		expected = [ 1, 2, False, 3, True ]
		for dd, val in zip(rdd9, expected):
			if dd.is_terminal():
				self.assertEqual(val, dd._value)
			else:
				self.assertEqual(val, dd._index)

	def test_restrict(self):
		one = self.one
		zero = self.zero
		x1, x2, x3 = self.x1, self.x2, self.x3

		valuation = { 1: True, 2: False, 3: True }
		self.assertEqual(BDD.restrict(one, valuation),  one)
		self.assertEqual(BDD.restrict(zero, valuation), zero)

		vars = [ x1, x2, x3 ]
		for i, var in enumerate(vars):
			if valuation[i+1]:
				self.assertEqual(BDD.restrict(var, valuation), one)
			else:
				self.assertEqual(BDD.restrict(var, valuation), zero)

		f1 = x1 & (-x2)
		val1 = [ (1, False), (2, False) ]
		self.assertEqual(BDD.restrict(f1, dict(val1[:1])), zero)
		self.assertEqual(BDD.restrict(f1, dict(val1[1:])), x1)
		self.assertEqual(BDD.restrict(f1, dict(val1)), zero)
		val2 = [ (1, False), (2, True)  ]
		self.assertEqual(BDD.restrict(f1, dict(val2[:1])), zero)
		self.assertEqual(BDD.restrict(f1, dict(val2[1:])), zero)
		self.assertEqual(BDD.restrict(f1, dict(val2)), zero)
		val3 = [ (1, True),  (2, False) ]
		self.assertEqual(BDD.restrict(f1, dict(val3[:1])), -x2)
		self.assertEqual(BDD.restrict(f1, dict(val3[1:])), x1)
		self.assertEqual(BDD.restrict(f1, dict(val3)), one)
		val4 = [ (1, True),  (2, True)  ]
		self.assertEqual(BDD.restrict(f1, dict(val4[:1])), -x2)
		self.assertEqual(BDD.restrict(f1, dict(val4[1:])), zero)
		self.assertEqual(BDD.restrict(f1, dict(val4)), zero)

		f2 = x2 & (-x3)
		val0 = [ (1, False), (4, False) ]
		self.assertEqual(BDD.restrict(f2, dict(val0)), f2)
		val0 = [ (1, False), (4, True) ]
		self.assertEqual(BDD.restrict(f2, dict(val0)), f2)
		val0 = [ (1, True), (4, False) ]
		self.assertEqual(BDD.restrict(f2, dict(val0)), f2)
		val0 = [ (1, True), (4, True) ]
		self.assertEqual(BDD.restrict(f2, dict(val0)), f2)

		f3 = -x2 | x3
		val1 = [ (1, False), (2, False), (3, False), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val1)), one)
		val2 = [ (1, True), (2, False), (3, False), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val2)), one)
		val3 = [ (1, False), (2, True), (3, False), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val3)), zero)
		val4 = [ (1, True), (2, True), (3, False), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val4)), zero)
		val5 = [ (1, False), (2, False), (3, True), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val5)), one)
		val6 = [ (1, True), (2, False), (3, True), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val6)), one)
		val7 = [ (1, False), (2, True), (3, True), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val7)), one)
		val8 = [ (1, True), (2, True), (3, True), (4, False) ]
		self.assertEqual(BDD.restrict(f3, dict(val8)), one)
		val9 = [ (1, False), (2, False), (3, False), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val9)), one)
		val10 = [ (1, True), (2, False), (3, False), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val10)), one)
		val11 = [ (1, False), (2, True), (3, False), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val11)), zero)
		val12 = [ (1, True), (2, True), (3, False), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val12)), zero)
		val13 = [ (1, False), (2, False), (3, True), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val13)), one)
		val14 = [ (1, True), (2, False), (3, True), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val14)), one)
		val15 = [ (1, False), (2, True), (3, True), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val15)), one)
		val16 = [ (1, True), (2, True), (3, True), (4, True) ]
		self.assertEqual(BDD.restrict(f3, dict(val16)), one)

	def test_not(self):
		one = -self.zero
		one.is_one()
		zero = -self.one
		zero.is_zero()

		vars = [ -self.x1, -self.x2, -self.x3 ]
		for index, var in enumerate(vars):
			self.assertFalse(var.is_terminal())
			self.assertEqual(var._index, index+1)
			self.assertFalse(var._high._value)
			self.assertTrue(var._low._value)
			self.assertTrue(var._value is None)

		dd1 = BDD.zero()
		dd2 = BDD.one()
		dd3 = BDD(3, dd1, dd2, None)
		dd4 = BDD(2, dd1, dd3, None)
		dd5 = BDD(1, dd4, dd3, None)
		negdd5 = -dd5
		expected = [ 1, 2, True, 3, False ]
		for dd, val in zip(negdd5, expected):
			if dd.is_terminal():
				self.assertEqual(val, dd._value)
			else:
				self.assertEqual(val, dd._index)

	def test_and(self):
		# idempotency
		one = self.one
		self.assertEqual(one, one & one)
		zero = self.zero
		self.assertEqual(zero, zero & zero)
		x1 = self.x1
		self.assertEqual(x1, x1 & x1)
		x2 = self.x2
		self.assertEqual(x2, x2 & x2)
		x3 = self.x3
		self.assertEqual(x3, x3 & x3)
		dd1 = BDD.zero()
		dd2 = BDD.one()
		dd3 = BDD(3, dd1, dd2, None)
		dd4 = BDD(2, dd1, dd3, None)
		dd5 = BDD(1, dd4, dd3, None)
		self.assertEqual(dd5, dd5 & dd5)

		# commutative law
		self.assertEqual(zero & one, one & zero)
		self.assertEqual(x1 & x2, x2 & x1)
		self.assertEqual((x1 & x2) & x3, x3 & (x1 & x2))
		self.assertEqual(dd5 & (x2 & -x3), (x2 & -x3) & dd5)

		# associative law
		self.assertEqual(x1 & (x2 & x3), (x1 & x2) & x3)
		self.assertEqual(-x1 & (x2 & x3), (-x1 & x2) & x3)
		self.assertEqual(x1 & (-x2 & x3), (x1 & -x2) & x3)
		self.assertEqual(x1 & (x2 & -x3), (x1 & x2) & -x3)

		# neutral element
		self.assertEqual(x1, x1 & one)
		self.assertEqual(x2, x2 & one)
		self.assertEqual(x3, x3 & one)
		self.assertEqual(-x1, -x1 & one)
		self.assertEqual(-x2, -x2 & one)
		self.assertEqual(-x3, -x3 & one)
		self.assertEqual(x1 & x2 & x3, (x1 & x2 & x3) & one)
		self.assertEqual(-x1 & -x2 & -x3, (-x1 & -x2 & -x3) & one)
		self.assertEqual(dd5, dd5 & one)

		# opposite element
		self.assertEqual(zero, x1 & -x1)
		self.assertEqual(zero, -x2 & x2)
		self.assertEqual(zero, -x3 & x3)
		self.assertEqual(zero, dd5 & -dd5)
		self.assertEqual(zero, -(x1 & -x3 & x2) & (x1 & -x3 & x2))
		self.assertEqual(zero, -x1 & --x1)
		self.assertEqual(zero, -(-x2) & -x2)
		self.assertEqual(zero, -(-x3) & -x3)
		self.assertEqual(zero, -dd5 & --dd5)
		self.assertEqual(zero, --(x1 & -x3 & x2) & -(x1 & -x3 & x2))

		# distributivity law AND over OR
		self.assertEqual(x1 & (x2 | x3), (x1 & x2) | (x1 & x3))
		self.assertEqual(dd5 & (x2 | x3), (dd5 & x2) | (dd5 & x3))
		self.assertEqual(x1 & (dd5 | x3), (x1 & dd5) | (x1 & x3))
		self.assertEqual(x1 & (x2 | dd5), (x1 & x2) | (x1 & dd5))

	def test_or(self):
		# idempotency
		one = self.one
		self.assertEqual(one, one | one)
		zero = self.zero
		self.assertEqual(zero, zero | zero)
		x1 = self.x1
		self.assertEqual(x1, x1 | x1)
		x2 = self.x2
		self.assertEqual(x2, x2 | x2)
		x3 = self.x3
		self.assertEqual(x3, x3 | x3)
		dd1 = BDD.zero()
		dd2 = BDD.one()
		dd3 = BDD(3, dd1, dd2, None)
		dd4 = BDD(2, dd1, dd3, None)
		dd5 = BDD(1, dd4, dd3, None)
		self.assertEqual(dd5, dd5 | dd5)

		# commutative law
		self.assertEqual(zero | one, one | zero)
		self.assertEqual(x1 | x2, x2 | x1)
		self.assertEqual((x1 | x2) | x3, x3 | (x1 | x2))
		self.assertEqual(dd5 | (x2 | -x3), (x2 | -x3) | dd5)

		# associative law
		self.assertEqual(x1 | (x2 | x3), (x1 | x2) | x3)
		self.assertEqual(-x1 | (x2 | x3), (-x1 | x2) | x3)
		self.assertEqual(x1 | (-x2 | x3), (x1 | -x2) | x3)
		self.assertEqual(x1 | (x2 | -x3), (x1 | x2) | -x3)

		# neutral element
		self.assertEqual(x1, x1 | zero)
		self.assertEqual(x2, x2 | zero)
		self.assertEqual(x3, x3 | zero)
		self.assertEqual(-x1, -x1 | zero)
		self.assertEqual(-x2, -x2 | zero)
		self.assertEqual(-x3, -x3 | zero)
		self.assertEqual(x1 | x2 | x3, (x1 | x2 | x3) | zero)
		self.assertEqual(-x1 | -x2 | -x3, (-x1 | -x2 | -x3) | zero)
		self.assertEqual(dd5, dd5 | zero)

		# opposite element
		self.assertEqual(one, x1 | -x1)
		self.assertEqual(one, -x2 | x2)
		self.assertEqual(one, -x3 | x3)
		self.assertEqual(one, dd5 | -dd5)
		self.assertEqual(one, -(x1 | -x3 | x2) | (x1 | -x3 | x2))
		self.assertEqual(one, -x1 | --x1)
		self.assertEqual(one, -(-x2) | -x2)
		self.assertEqual(one, -(-x3) | -x3)
		self.assertEqual(one, -dd5 | --dd5)
		self.assertEqual(one, --(x1 | -x3 | x2) | -(x1 | -x3 | x2))

		# distributivity law OR over AND
		self.assertEqual(x1 | (x2 & x3), (x1 | x2) & (x1 | x3))
		self.assertEqual(dd5 | (x2 & x3), (dd5 | x2) & (dd5 | x3))
		self.assertEqual(x1 | (dd5 & x3), (x1 | dd5) & (x1 | x3))
		self.assertEqual(x1 | (x2 & dd5), (x1 | x2) & (x1 | dd5))

	def test_xor(self):
		# idempotency
		one = self.one
		zero = self.zero
		self.assertEqual(zero, one ^ one)
		self.assertEqual(zero, zero ^ zero)
		x1 = self.x1
		self.assertEqual(zero, x1 ^ x1)
		x2 = self.x2
		self.assertEqual(zero, x2 ^ x2)
		x3 = self.x3
		self.assertEqual(zero, x3 ^ x3)
		dd1 = BDD.zero()
		dd2 = BDD.one()
		dd3 = BDD(3, dd1, dd2, None)
		dd4 = BDD(2, dd1, dd3, None)
		dd5 = BDD(1, dd4, dd3, None)
		self.assertEqual(zero, dd5 ^ dd5)

		# commutative law
		self.assertEqual(zero ^ one, one ^ zero)
		self.assertEqual(x1 ^ x2, x2 ^ x1)
		self.assertEqual((x1 ^ x2) ^ x3, x3 ^ (x1 ^ x2))
		self.assertEqual(dd5 ^ (x2 ^ -x3), (x2 ^ -x3) ^ dd5)

		# associative law
		self.assertEqual(x1 ^ (x2 ^ x3), (x1 ^ x2) ^ x3)
		self.assertEqual(-x1 ^ (x2 ^ x3), (-x1 ^ x2) ^ x3)
		self.assertEqual(x1 ^ (-x2 ^ x3), (x1 ^ -x2) ^ x3)
		self.assertEqual(x1 ^ (x2 ^ -x3), (x1 ^ x2) ^ -x3)

		# neutral element
		self.assertEqual(x1, x1 ^ zero)
		self.assertEqual(x2, x2 ^ zero)
		self.assertEqual(x3, x3 ^ zero)
		self.assertEqual(-x1, -x1 ^ zero)
		self.assertEqual(-x2, -x2 ^ zero)
		self.assertEqual(-x3, -x3 ^ zero)
		self.assertEqual(x1 ^ x2 ^ x3, (x1 ^ x2 ^ x3) ^ zero)
		self.assertEqual(-x1 ^ -x2 ^ -x3, (-x1 ^ -x2 ^ -x3) ^ zero)
		self.assertEqual(dd5, dd5 ^ zero)

		# opposite element
		self.assertEqual(one, x1 ^ -x1)
		self.assertEqual(one, -x2 ^ x2)
		self.assertEqual(one, -x3 ^ x3)
		self.assertEqual(one, dd5 ^ -dd5)
		self.assertEqual(one, -(x1 ^ -x3 ^ x2) ^ (x1 ^ -x3 ^ x2))
		self.assertEqual(one, -x1 ^ --x1)
		self.assertEqual(one, -(-x2) ^ -x2)
		self.assertEqual(one, -(-x3) ^ -x3)
		self.assertEqual(one, -dd5 ^ --dd5)
		self.assertEqual(one, --(x1 ^ -x3 ^ x2) ^ -(x1 ^ -x3 ^ x2))


if __name__ == '__main__':
	unittest.main(verbosity=2)