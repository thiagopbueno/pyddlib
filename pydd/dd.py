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

import sys

class DD(object):
	""" Decision Diagram abstract base class. """

	def __iter__(self):
		"""
		Initialize and return an iterator for pydd.DD objects.

		:rtype: pydd.DD
		"""
		self.__traversed = set()
		self.__fringe = [self]
		return self

	def __next__(self):
		"""
		Implement a graph-based traversal algorithm for pydd.DD objects.
		Each vertex is visited exactly once. Low child is visited before
		high child. Return the next vertex in the sequence.

		:rtype: pydd.DD
		"""
		if not self.__fringe:
			raise StopIteration()
		vertex = self.__fringe.pop()
		if not vertex.is_terminal():
			low  = vertex._low
			high = vertex._high
			if id(high) not in self.__traversed:
				self.__fringe.append(high)
				self.__traversed.add(id(high))
			if id(low) not in self.__traversed:
				self.__fringe.append(low)
				self.__traversed.add(id(low))
		return vertex

	@classmethod
	def reduce(cls, v):
		"""
		Reduce in place a pydd.DD object rooted in `v` by
		removing duplicate nodes and redundant sub-trees.
		Return the canonical representation of the pydd.DD object.

		:param v: root vertex
		:type v: pydd.DD
		:rtype: pydd.DD
		"""
		if v.is_terminal():
			return v

		vlist = {}
		subgraph = {}
		for vertex in v:
			index = vertex._index
			vlist[index] = vlist.get(index, [])
			vlist[index].append(vertex)

		nextid = 0

		index_lst = [-1] + sorted(list(vlist), reverse=True)[:-1]
		for i in index_lst:
			Q = []
			for u in vlist[i]:
				if u.is_terminal():
					Q.append((u._value, u))
				elif u._low._id == u._high._id:
					u._id = u._low._id
				else:
					Q.append(((u._low._id, u._high._id), u))

			oldkey = None
			for key, u in sorted(Q, key=lambda x: x[0]):
				if key == oldkey:
					u._id = nextid
				else:
					nextid += 1
					u._id = nextid
					subgraph[nextid] = u
					if not u.is_terminal():
						u._low = subgraph[u._low._id]
						u._high = subgraph[u._high._id]
					oldkey = key

		return subgraph[v._id]

	@classmethod
	def apply(cls, v1, v2, op):
		"""
		Return a new canonical representation of the
		pydd.DD object for the result of `v1` `op` `v2`.

		:param v1: root vertex of left operand
		:type v1: pydd.DD
		:param v2: root vertex of right operand
		:type v2: pydd.DD
		:param op: a binary operator
		:type op: callable object or function
		:rtype: pydd.DD
		"""
		T = {}
		return cls.reduce(cls.__apply_step(v1, v2, op, T))

	@classmethod
	def __apply_step(cls, v1, v2, op, T):
		"""
		Private auxiliary method used in pydd.DD.apply method.
		Recursively computes `v1` `op` `v2`. If the result was
		already computed as an intermediate result, it returns
		the cached result stored in `T`.

		:param v1: root vertex of left operand
		:type v1: pydd.DD
		:param v2: root vertex of right operand
		:type v2: pydd.DD
		:param op: a binary operator
		:type op: callable object or function
		:param T: cached intermediate results
		:type T: dict( (int,int), pydd.DD )
		:rtype: pydd.DD
		"""
		u = T.get((v1._id, v2._id))
		if u is not None:
			return u

		if v1.is_terminal() and v2.is_terminal():
			result = v1.__class__.terminal(op(v1._value, v2._value))
		else:
			v1index = v2index = sys.maxsize
			if not v1.is_terminal():
				v1index = v1._index
			if not v2.is_terminal():
				v2index = v2._index
			index_min = min(v1index, v2index)

			if v1._index == index_min:
				vlow1  = v1._low
				vhigh1 = v1._high
			else:
				vlow1 = vhigh1 = v1

			if v2._index == index_min:
				vlow2  = v2._low
				vhigh2 = v2._high
			else:
				vlow2 = vhigh2 = v2

			low  = cls.__apply_step(vlow1, vlow2, op, T)
			high = cls.__apply_step(vhigh1, vhigh2, op, T)
			result = v1.__class__(index_min, low, high, None)

		T[(v1._id, v2._id)] = result
		return result

	@classmethod
	def restrict(cls, v, valuation):
		return cls.reduce(cls.__restrict_step(v, valuation))

	@classmethod
	def __restrict_step(cls, v, valuation):
		if v.is_terminal():
			return v

		val = valuation.get(v._index, None)
		if val is None:
			low  = cls.__restrict_step(v._low,  valuation)
			high = cls.__restrict_step(v._high, valuation)
			return v.__class__(v._index, low, high, None)
		else:
			if val:
				return cls.__restrict_step(v._high, valuation)
			else:
				return cls.__restrict_step(v._low, valuation)
