# Abstract Algebra

A Python implementation of **Finite Algebras**: Magma, Semigroup, Monoid, Group, Ring, and Field

## Summary

The ``finite_algebras`` module contains class definitions, methods, and functions for working with algebras that only have a **finite number of elements**.

* The primary constructor of algebras is the function, ``make_finite_algebra``. It examines the properties of the input table and returns the appropriate instance of an algebra.
* Algebras can be input from, or output to, JSON files/strings or Python dictionaries.
* Each algebra is defined by name (``str``), a description (``str``), a list of *element names* (``str``) and a square, 2-dimensional table that defines a binary operation (``list`` of ``lists`` of ``int``).  Rings & Fields have two such tables.
* Each algebra has methods for examining its properties (e.g., ``is_associative()``, ``is_commutative()``)
* Algebraic elements can be "added" (or "multiplied") via their binary operations (e.g., ``v4.op('h','v') ==> 'r'``).
* Inverses & identities can be obtained, if the algebra supports them (e.g., ``z3.inv('a') = 'a^2'``, ``z3.identity ==> 'e'``).
* Direct products of two or more algebras can be computed using Python's multiplication operator (e.g., ``z4 * v4``).
* If two algebras are isomorphic, the mapping between their elements can be determined (e.g., ``v4.isomorphic(z2 * z2) ==> {'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}``)
* Autogeneration of some types of algebras, of arbitrary order, is supported (e.g., symmetric, cyclic).
* Subalgebras (e.g., subgroups) can be determined, along with related functionality (e.g, ``is_normal()``).

## Installation

This module runs under Python 3.7+ and requires **NumPy**.

Clone the github repository to install:
$ git clone https://github.com/alreich/abstract_algebra.git
## Documentation

See full documentation at [ReadTheDocs](https://abstract-algebra.readthedocs.io/en/latest/index.html).

## Quick Look

**Create an algebra:**


```python
>>> from finite_algebras import make_finite_algebra

>>> v4 = make_finite_algebra('V4',
                             'Klein-4 group',
                             ['e', 'h', 'v', 'r'],
                             [[0, 1, 2, 3],
                              [1, 0, 3, 2],
                              [2, 3, 0, 1],
                              [3, 2, 1, 0]])
>>> v4
```




    Group(
    'V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



**Look at the algebra's properties:**


```python
>>> v4.about(use_table_names=True)
```

    
    Group: V4
    Instance ID: 140551598863952
    Description: Klein-4 group
    Identity: e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       h       h       2
          2       v       v       2
          3       r       r       2
    Cayley Table (showing names):
    [['e', 'h', 'v', 'r'],
     ['h', 'e', 'r', 'v'],
     ['v', 'r', 'e', 'h'],
     ['r', 'v', 'h', 'e']]


**Autogenerate a small cyclic group:**


```python
>>> from finite_algebras import generate_cyclic_group

>>> z2 = generate_cyclic_group(2)

>>> z2.about()
```

    
    Group: Z2
    Instance ID: 140551336627216
    Description: Autogenerated cyclic Group of order 2
    Identity: e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a       a       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


**Compute the Direct Product of the cyclic group with itself:**


```python
>>> z2_sqr = z2 * z2

>>> z2_sqr.about(use_table_names=True)
```

    
    Group: Z2_x_Z2
    Instance ID: 140551336626960
    Description: Direct product of Z2 & Z2
    Identity: e:e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0     e:e     e:e       1
          1     e:a     e:a       2
          2     a:e     a:e       2
          3     a:a     a:a       2
    Cayley Table (showing names):
    [['e:e', 'e:a', 'a:e', 'a:a'],
     ['e:a', 'e:e', 'a:a', 'a:e'],
     ['a:e', 'a:a', 'e:e', 'e:a'],
     ['a:a', 'a:e', 'e:a', 'e:e']]


**Are z2_sqr & v4 isomorphic?**

**Yes, and here's the mapping between their elements:**


```python
>>> v4.isomorphic(z2_sqr)
```




    {'e': 'e:e', 'h': 'e:a', 'v': 'a:e', 'r': 'a:a'}


