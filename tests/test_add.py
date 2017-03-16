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

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../pyddlib/'))

import unittest

from pyddlib.add import ADD

class TestADD(unittest.TestCase):

	@classmethod
	def setUp(cls):
		# constant ndoes
		cls.c0 = ADD.constant(0.0)
		cls.c1 = ADD.constant(1.0)
		cls.c2 = ADD.constant(2.0)
		cls.c3 = ADD.constant(3.0)
		cls.c4 = ADD.constant(4.0)
		cls.c5 = ADD.constant(5.0)
		cls.constants = [cls.c0, cls.c1, cls.c2, cls.c3, cls.c4, cls.c5]

		# variables
		cls.x1 = ADD.variable(1)
		cls.x2 = ADD.variable(2)
		cls.x3 = ADD.variable(3)
		cls.variables = [cls.x1, cls.x2, cls.x3]

	def test_constant(self):
		self.assertTrue(self.c1.is_constant())
		self.assertEqual(self.c1.value, 1.0)

	def test_variable(self):
		for i, var in enumerate(self.variables):
			self.assertFalse(var.is_constant())
			self.assertTrue(var.is_variable())
			self.assertEqual(var.index, i+1)

	def test_reduce(self):
		for c in self.constants:
			self.assertTrue(c, ADD.reduce(c))

		for var in self.variables:
			self.assertTrue(var, ADD.reduce(var))

		c01 = ADD.constant(-1.0)
		c02 = ADD.constant(-1.0)
		c21 = ADD.constant(2.0)
		c22 = ADD.constant(2.0)
		c23 = ADD.constant(2.0)
		c24 = ADD.constant(2.0)
		c51 = ADD.constant(5.0)
		c52 = ADD.constant(5.0)

		add1 = ADD(3, c01, c21, None)
		add2 = ADD(3, c23, c22, None)
		add3 = ADD(3, c02, c24, None)
		add4 = ADD(3, c52, c51, None)
		add5 = ADD(2, add1, add2, None)
		add6 = ADD(2, add3, add4, None)
		add7 = ADD(1, add5, add6, None)

		radd7 = ADD.reduce(add7)
		self.assertEqual(radd7, ADD.reduce(radd7))

		c0 = ADD.constant(-1.0)
		c2 = ADD.constant(2.0)
		c5 = ADD.constant(5.0)
		add1 = ADD(3, c0, c2, None)
		add2 = ADD(2, add1, c2, None)
		add3 = ADD(2, add1, c5, None)
		add4 = ADD(1, add2, add3, None)
		self.assertEqual(radd7, add4)
		self.assertEqual(radd7, ADD.reduce(add4))

	def test_restrict(self):
		valuation = { 1: True, 2: False, 3: True }
		for c in self.constants:
			self.assertEqual(c.restrict(valuation), c)

		for i, var in enumerate(self.variables):
			if valuation[var.index]:
				self.assertEqual(var.restrict(valuation), self.c1)
			else:
				self.assertEqual(var.restrict(valuation), self.c0)

		add1 = self.x1 * self.x2 + self.x3 * self.c2
		self.assertTrue(add1.restrict(valuation).is_constant())
		self.assertEqual(add1.restrict(valuation).value, 2.0)

		add2 = self.x1 * (self.x2 + self.x3) * self.c2
		self.assertTrue(add2.restrict(valuation).is_constant())
		self.assertEqual(add2.restrict(valuation).value, 2.0)

		add3 = -self.x1 * self.x2 + self.x3 * -self.c2
		self.assertTrue(add3.restrict(valuation).is_constant())
		self.assertEqual(add3.restrict(valuation).value, -2.0)

		add4 = -(self.x1 * self.x2 + self.x3) * -self.c2
		self.assertTrue(add4.restrict(valuation).is_constant())
		self.assertEqual(add4.restrict(valuation).value, 2.0)

		add5 = -(self.x1 * ~self.x2 + self.x3) * -self.c2
		self.assertTrue(add5.restrict(valuation).is_constant())
		self.assertEqual(add5.restrict(valuation).value, 4.0)

		add6 = -(self.x1 * ~self.x2 + self.x3) + -self.c1 * -self.c2
		self.assertTrue(add6.restrict(valuation).is_constant())
		self.assertEqual(add6.restrict(valuation).value, 0.0)

	def test_not(self):
		not_c0 = ~self.c0
		self.assertTrue(not_c0.is_constant())
		self.assertEqual(not_c0.value, 1.0)
		not_c1 = ~self.c1
		self.assertTrue(not_c1.is_constant())
		self.assertEqual(not_c1.value, 0.0)
		not_c2 = ~self.c2
		self.assertTrue(not_c2.is_constant())
		self.assertEqual(not_c2.value, 0.0)

		not_x1 = ~self.x1
		self.assertEqual(not_x1.index, self.x1.index)
		self.assertEqual(not_x1._low.value, 1.0)
		self.assertEqual(not_x1._high.value, 0.0)
		not_x2 = ~self.x2
		self.assertEqual(not_x2.index, self.x2.index)
		self.assertEqual(not_x2._low.value, 1.0)
		self.assertEqual(not_x2._high.value, 0.0)

		dd1 = ADD(2, self.c0, self.c2, None)
		dd2 = ADD(1, self.c0, dd1, None)
		not_dd2 = ~dd2
		actual = []
		for node in not_dd2:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 1.0, 2, 0.0]
		self.assertEqual(actual, expected)

	def test_addition(self):
		for c in self.constants[1:]:
			self.assertTrue(c + self.c0, c)

		self.assertEqual(sum(self.constants, self.c0), ADD.constant(15.0))

		add_sum = sum(self.variables, self.c0)
		actual = []
		for node in add_sum:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 2, 3, 0.0, 1.0, 3, 2.0, 2, 3, 3.0]
		self.assertEqual(actual, expected)

		add1 = self.x1 + ~self.x2 * self.c3
		add2 = (~self.x2 + self.c2) * self.c3
		add3 = (self.c3 + self.x1) * ~self.x3 * ~self.x2 * self.c2 + self.c1
		add4 = (self.c3 + ~self.x1) * self.x3 * ~self.x2 * ~(self.c2 + self.c1)

		# commutative law
		self.assertEqual(add1 + add2, add2 + add1)
		self.assertEqual(add2 + add3, add3 + add2)
		self.assertEqual(add4 + add2, add2 + add4)
		self.assertEqual(add1 + add4, add4 + add1)

		# associative law
		self.assertEqual((add1 + add2) + add3, add1 + (add2 + add3))
		self.assertEqual((add2 + add4) + add3, add2 + (add4 + add3))
		self.assertEqual((add3 + add2) + add4, add3 + (add2 + add4))
		self.assertEqual((add2 + add1) + add4, add2 + (add1 + add4))

		# neutral element
		self.assertEqual(add1 + self.c0, add1)
		self.assertEqual(add2 + self.c0, add2)
		self.assertEqual(add3 + self.c0, add3)
		self.assertEqual(add4 + self.c0, add4)

		# opposite element
		for c in self.constants:
			self.assertEqual(c + -c, self.c0)
			self.assertEqual(-c + c, self.c0)
			self.assertEqual(-c + --c, self.c0)
			self.assertEqual(--c + -c, self.c0)
		for var in self.variables:
			self.assertEqual(var + -var, self.c0)
			self.assertEqual(-var + var, self.c0)
			self.assertEqual(-var + --var, self.c0)
			self.assertEqual(--var + -var, self.c0)
		self.assertEqual(add1 + -add1, self.c0)
		self.assertEqual(-add2 + add2, self.c0)
		self.assertEqual(add3 + -add3, self.c0)
		self.assertEqual(-add4 + add4, self.c0)

	def test_subtraction(self):
		for c in self.constants:
			self.assertEqual(c - c, self.c0)
			self.assertEqual(c - self.c0, c)

		add0 = sum(self.variables, self.c0) - self.c1
		actual = []
		for node in add0:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 2, 3, -1.0, 0.0, 3, 1.0, 2, 3, 2.0]
		self.assertEqual(actual, expected)

		add1 = self.x1 + ~self.x2 * self.c3
		add2 = (~self.x2 + self.c2) * self.c3
		add3 = (self.c3 + self.x1) * ~self.x3 * ~self.x2 * self.c2 + self.c1
		add4 = (self.c3 + ~self.x1) * self.x3 + ~self.x2 * ~(self.c2 + self.c1)

		self.assertEqual(add1 - self.x1, ~self.x2 * self.c3)
		self.assertEqual(add2 - ~self.x2 * self.c3, self.c2 * self.c3)
		self.assertEqual(add3 - self.c1, (self.c3 + self.x1) * ~self.x3 * ~self.x2 * self.c2)
		self.assertEqual(add4 - (self.c3 + ~self.x1) * self.x3, ~self.x2 * ~(self.c2 + self.c1))

		self.assertEqual(add1 - add2, -(add2 - add1))
		self.assertEqual(add2 - add3, -(add3 - add2))
		self.assertEqual(add4 - add2, -(add2 - add4))
		self.assertEqual(add1 - add4, -(add4 - add1))

		self.assertEqual(add1 - self.c0, add1)
		self.assertEqual(add2 - self.c0, add2)
		self.assertEqual(add3 - self.c0, add3)
		self.assertEqual(add4 - self.c0, add4)

		self.assertEqual(self.c0 - add1, -add1)
		self.assertEqual(self.c0 - add2, -add2)
		self.assertEqual(self.c0 - add3, -add3)
		self.assertEqual(self.c0 - add4, -add4)

	def test_multiplication(self):
		for var in self.variables:
			for c in self.constants:
				add = var * c
				if c.value == 0.0:
					self.assertTrue(add.is_constant())
					self.assertEqual(add.value, 0.0)
				else:
					self.assertFalse(add.is_constant())
					self.assertEqual(add._low.value,  c.value * var._low.value)
					self.assertEqual(add._high.value, c.value * var._high.value)

		add1 = self.x1 * self.x2 * self.c2
		actual = []
		for node in add1:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 0.0, 2, 2.0]
		self.assertEqual(actual, expected)

		# commutative law
		add2 = self.x1 * self.x3 * self.c3
		self.assertEqual(add1 * add2, add2 * add1)

		# associative law
		add3 = self.x2 * ~self.x1 * self.c2
		add4 = ~self.x1 * self.c2 * self.x2
		add5 = self.c2 * self.x2 * ~self.x1
		self.assertEqual(add3, add4)
		self.assertEqual(add3, add5)
		self.assertEqual(add4, add5)

		# neutral element
		self.assertEqual(add1, add1 * self.c1)
		self.assertEqual(add1 * self.c1, add1)
		self.assertEqual(add1, add1 * self.c1)
		self.assertEqual(add2 * self.c1, add2)
		self.assertEqual(add2, add2 * self.c1)
		self.assertEqual(add3 * self.c1, add3)

		# distributivity law * over +
		self.assertEqual(add1 * (add2 + add3), add1 * add2 + add1 * add3)
		self.assertEqual((add2 + add3) * add1, add1 * add2 + add1 * add3)
		self.assertEqual(add1 * (add4 + add3 + add5), add1 * add4 + add1 * add3 + add1 * add5)
		self.assertEqual((add4 + add3 + add5) * add1, add1 * add4 + add1 * add3 + add1 * add5)

	def test_division(self):
		for var in self.variables:
			for c in self.constants[1:]:
				add = var / c
				self.assertFalse(add.is_constant())
				self.assertEqual(add._low.value,  var._low.value / c.value)
				self.assertEqual(add._high.value, var._high.value / c.value)

		add1 = self.x1 * self.x2 * self.c3 / self.c2
		actual = []
		for node in add1:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 0.0, 2, 1.5]
		self.assertEqual(actual, expected)

		add2 = self.x1 * self.x3 * self.c3
		add3 = self.x2 * ~self.x1 * self.c2
		add4 = ~self.x1 * self.c2 * self.x2
		add5 = self.c2 * self.x2 * ~self.x1

		self.assertEqual(add1, add1 / self.c1)
		self.assertEqual(add1 / self.c1, add1)
		self.assertEqual(add1, add1 / self.c1)
		self.assertEqual(add2 / self.c1, add2)
		self.assertEqual(add2, add2 / self.c1)
		self.assertEqual(add3 / self.c1, add3)

	def test_marginalize(self):
		for c in self.constants:
			for var in self.variables:
				self.assertTrue(c.marginalize(var) == c)
		for var1 in self.variables:
			for var2 in self.variables:
				result = var1.marginalize(var2)
				if var1 == var2:
					self.assertTrue(result.is_terminal())
					self.assertTrue(result.value == 1.0)
				else:
					self.assertEqual(var1.marginalize(var2), var1)

		add1 = self.x1 + self.x2
		result1 = self.x1 * self.c3 + ~self.x1 * self.c1
		result2 = self.x2 * self.c3 + ~self.x2 * self.c1
		self.assertEqual(add1.marginalize(self.x2), result1)
		self.assertEqual(add1.marginalize(self.x1), result2)
		self.assertEqual(add1.marginalize(self.x1).marginalize(self.x2), add1.marginalize(self.x2).marginalize(self.x1))

		add2 = self.x1 * self.x2 * self.c5 + self.c2 * (~self.x2 * self.x3 + ~self.x1 * self.x2)
		m1 = add2.marginalize(self.x1)
		actual = []
		for node in m1:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [2, 3, 0.0, 4.0, 7.0]
		self.assertEqual(actual, expected)

		m2 = add2.marginalize(self.x2)
		actual = []
		for node in m2:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 3, 2.0, 4.0, 3, 5.0, 7.0]
		self.assertEqual(actual, expected)

		m3 = add2.marginalize(self.x3)
		actual = []
		for node in m3:
			if node.is_terminal():
				actual.append(node.value)
			else:
				actual.append(node.index)
		expected = [1, 2.0, 2, 5.0]
		self.assertEqual(actual, expected)


if __name__ == '__main__':
	unittest.main(verbosity=2)
