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

from pyddlib.dd import DD

class BDD(DD):
	"""
	Reduced Ordered Binary Decision Diagram class.

	:param index: root vertex variable index (-1 if terminal vertex)
	:type  index: int
	:param low:   low child vertex of BDD (None if terminal vertex)
	:type  low:   pydd.BDD
	:param high:  high child vertex of BDD (None if terminal vertex)
	:type  high:  pydd.BDD
	:param value: terminal boolean value (None if non-terminal vertex)
	:type  type:  bool or None
	"""

	__one  = None  # singleton object for terminal node True
	__zero = None  # singleton object for terminal node False

	__nextid = 1

	def __init__(self, index, low, high, value):
		self._index = index
		self._low   = low
		self._high  = high
		self._value = value
		self._id    = BDD.__nextid
		BDD.__nextid += 1

	def __repr__(self):
		"""
		Return tree-like representation of pydd.BDD object.

		:rytpe: str
		"""
		ddrepr = ''
		stack = [(self, 0, None)]
		while stack:
			(vertex, indentation, child_type) = stack.pop()
			for i in range(indentation):
				ddrepr += '|  '
			prefix = '@'
			if child_type is not None:
				prefix = child_type
			ddrepr += prefix
			if vertex.is_terminal():
				ddrepr += ' (value={}, id={})'.format(vertex._value, vertex._id) + '\n'
			else:
				ddrepr += ' (index={}, id={})'.format(vertex._index, vertex._id) + '\n'
				stack.append((vertex._high, indentation+1, '+'))
				stack.append((vertex._low,  indentation+1, '-'))
		return ddrepr

	def is_terminal(self):
		"""
		Return True if BDD function represents a constant value.
		Otherwise, return False.

		:rtype: bool
		"""
		return  self._low  is None and \
				self._high is None and \
				self._value in [ True, False ]

	def is_one(self):
		"""
		Return True if BDD function represents boolean value True.
		Otherwise, return False.

		:rtype: bool
		"""
		return self.is_terminal() and self._value == True

	def is_zero(self):
		"""
		Return True if BDD function represents boolean value False.
		Otherwise, return False.

		:rtype: bool
		"""
		return self.is_terminal() and self._value == False

	def is_variable(self):
		"""
		Return True if BDD function represents the function
		of a single boolean variable. Otherwise, return False.

		:rtype: bool
		"""
		return  (self._low  and self._low.is_zero()) and \
				(self._high and self._high.is_one())

	def __neg__(self):
		"""
		Return a new BDD representing the negation of the boolean function.

		:rtype: pydd.BDD
		"""
		if self.is_one():
			return self.zero()
		if self.is_zero():
			return self.one()
		return BDD(self._index, -self._low, -self._high, None)

	def __and__(self, other):
		"""
		Return a new BDD representing the conjunction of boolean functions.

		:param other: BDD
		:type other: pydd.BDD
		:rtype: pydd.BDD
		"""
		return BDD.apply(self, other, bool.__and__)

	def __or__(self, other):
		"""
		Return a new BDD representing the disjunction of boolean functions.

		:param other: BDD
		:type other: pydd.BDD
		:rtype: pydd.BDD
		"""
		return BDD.apply(self, other, bool.__or__)

	def __xor__(self, other):
		"""
		Return a new BDD representing the XOR of boolean functions.

		:param other: BDD
		:type other: pydd.BDD
		:rtype: pydd.BDD
		"""
		return BDD.apply(self, other, bool.__xor__)

	def __eq__(self, other):
		"""
		Return True if both BDDs represent the same boolean function.

		:param other: BDD
		:type other: pydd.BDD
		:rtype: bool
		"""
		return BDD.apply(self, other, bool.__eq__).is_one()

	def __neq__(self, other):
		"""
		Return True if both BDDs do not represent the same boolean function.

		:param other: BDD
		:type other: pydd.BDD
		:rtype: bool
		"""
		return not self == other

	@classmethod
	def terminal(cls, value):
		"""
		Return a terminal node with a given boolean `value`.

		:param value: True or False
		:type value: bool
		:rtype: pydd.BDD
		"""
		assert(type(value) == bool)
		return BDD(-1, None, None, value)

	@classmethod
	def one(cls):
		"""
		Return the BDD representing the constant function True.

		:rtype: pydd.BDD
		"""
		if BDD.__one:
			return BDD.__one
		BDD.__one = BDD(-1, None, None, True)
		return BDD.__one

	@classmethod
	def zero(cls):
		"""
		Return the BDD representing the constant function False.

		:rtype: pydd.BDD
		"""
		if BDD.__zero:
			return BDD.__zero
		BDD.__zero = BDD(-1, None, None, False)
		return BDD.__zero

	@classmethod
	def variable(cls, index):
		"""
		Return the BDD representing the function of a
		single boolean variable with given `index`.

		:param index: variable index
		:type index: int
		:rtype: pydd.BDD
		"""
		return BDD(index, cls.zero(), cls.one(), None)
