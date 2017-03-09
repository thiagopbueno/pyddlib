pydd
====

pydd is a Python3 library for manipulating decision diagrams (DD).

It is intended to follow (as much as possible) the notation and overall
construction proposed in the following papers:

[1] Bryant, Randal E. **Graph-based algorithms for boolean function
manipulation**. Computers, IEEE Transactions on 100, no. 8 (1986):
677-691.

[2] Brace, Karl S., Richard L. Rudell, and Randal E. Bryant. **Efficient
implementation of a BDD package**. In Proceedings of the 27th ACM/IEEE
design automation conference, pp. 40-45. ACM, 1991.

[3] Bahar, R. Iris, Erica A. Frohm, Charles M. Gaona, Gary D. Hachtel,
Enrico Macii, Abelardo Pardo, and Fabio Somenzi. **Algebraic decision
diagrams and their applications**. Formal methods in system design 10,
no. 2-3 (1997): 171-206.

Usage
-----

Binary Decision Diagrams (BDDs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You create BDDs from constants and variables by composing boolean
functions with logical operations AND (&), OR (\|), XOR (^) and NOT (-).

.. code:: python

    from pydd.BDD import BDD

    one  = BDD.one()
    zero = BDD.zero()
    print("== True ==")
    print(one)
    print("== False ==")
    print(zero)

    x1 = BDD.variable(1)
    x2 = BDD.variable(2)
    x3 = BDD.variable(3)
    print("=== x1 ===")
    print(x1)

    print("=== NOT x1 ===")
    print(-x1)

    print("=== x1 AND x2 ===")
    print(x1 & x2)

    print("=== x1 OR x2 ===")
    print(x1 | x2)

    print("=== x1 XOR x2 ===")
    print(x1 ^ x2)

    bdd1 = -x1 | (x2 ^ -x3)
    if (bdd1 & one) == bdd1:
        print('True is the neutral element for AND operation!')

    bdd2 = --x2 ^ (-(x1 | x3))
    if (bdd2 | zero) == bdd2:
        print('False is the neutral element for OR operation!')

    bdd3 = x1 & -x1
    if bdd3.is_zero():
        print('You can check contradiction with is_zero() funtion!')

    bdd4 = x1 | -x1
    if bdd4.is_one():
        print('You can check tautology with is_one() function!')

    bdd5 = -(x1 | -(x2 & -x3))
    if (bdd5 ^ bdd5).is_zero():
        print('You can check equivalence with XOR!')

    if (x1 & x2) == (x2 & x1):
        print('Commutative law works for boolean functions!')

    if x1 & (x2 & x3) == (x1 & x2) & x3:
        print('Associative law works for boolean functions!')

    if (x1 & (x2 | x3)) == ((x1 & x2) | (x1 & x3)):
        print('Distributivity law works: AND distributes over OR!')

    if (x1 | (x2 & x3)) == ((x1 | x2) & (x1 | x3)):
        print('Distributivity law works: OR distributes over AND!')

    bdd6 = -(x1 & -(-x2 | x3))
    valuation1 = { 1: True, 2: True, 3: False }

    if BDD.restrict(bdd6, valuation1).is_zero():
        print('You can evaluate the function with restrict!')

    valuation2 = { 1: True }
    if BDD.restrict(bdd6, valuation2) == (-x2 | x3):
        print('You can also partially evaluate the function with restrict!')

LICENSE
-------

Copyright (c) 2017 Thiago Pereira Bueno All Rights Reserved.

pydd is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

pydd is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pydd. If not, see http://www.gnu.org/licenses/
