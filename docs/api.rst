.. _api:

API Reference
=============

Primary Algebra Constructors
----------------------------

.. autofunction:: finite_algebras.make_finite_algebra

Operator
--------

.. autoclass:: finite_algebras.FiniteOperator
    :members:
    :undoc-members:

FiniteAlgebra
-------------

.. autoclass:: finite_algebras.FiniteAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

SingleElementSetAlgebra
-----------------------

.. autoclass:: finite_algebras.SingleElementSetAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Magma
-----

.. autoclass:: finite_algebras.Magma
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Semigroup
---------

.. autoclass:: finite_algebras.Semigroup
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Monoid
------

.. autoclass:: finite_algebras.Monoid
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Group
-----

.. autoclass:: finite_algebras.Group
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Ring
----

.. autoclass:: finite_algebras.Ring
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Field
-----

.. autoclass:: finite_algebras.Field
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

MultipleElementSetAlgebra
-------------------------

.. autoclass:: finite_algebras.MultipleElementSetAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Module
------

.. autofunction:: finite_algebras.module_sv_mult
.. autofunction:: finite_algebras.module_dot_product

.. autoclass:: finite_algebras.Module
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:
.. autofunction:: finite_algebras.check_module_conditions

NDimensionalModule
------------------

.. autoclass:: finite_algebras.NDimensionalModule
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

VectorSpace
-----------

.. autoclass:: finite_algebras.VectorSpace
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

NDimensionalVectorSpace
-----------------------

.. autoclass:: finite_algebras.NDimensionalVectorSpace
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Algebra Generators
------------------

.. autofunction:: finite_algebras.generate_cyclic_group
.. autofunction:: finite_algebras.generate_symmetric_group
.. autofunction:: finite_algebras.generate_powerset_group
.. autofunction:: finite_algebras.generate_relative_primes_group
.. autofunction:: finite_algebras.generate_commutative_monoid
.. autofunction:: finite_algebras.generate_powerset_ring
.. autofunction:: finite_algebras.generate_algebra_mod_n

Cayley Table
------------

.. autoclass:: cayley_table.CayleyTable
    :members:
    :undoc-members:

Permutations
------------

.. autoclass:: permutations.Perm
    :members:
    :undoc-members:

Examples
--------

.. autoclass:: finite_algebras.Examples
    :members:
    :undoc-members:

Misc Utilities
--------------

.. autofunction:: finite_algebras.is_prime
.. autofunction:: finite_algebras.is_relatively_prime
.. autofunction:: finite_algebras.relative_primes
.. autofunction:: finite_algebras.totient
.. autofunction:: finite_algebras.divisors
.. autofunction:: finite_algebras.delete_row_col
.. autofunction:: finite_algebras.get_name_desc_elements_table
.. autofunction:: finite_algebras.make_cayley_table
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.generate_all_group_tables
.. autofunction:: finite_algebras.get_duplicates
.. autofunction:: finite_algebras.get_int_forms
.. autofunction:: finite_algebras.get_integer_form
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.is_table_associative
.. autofunction:: finite_algebras.make_table_from_xml
.. autofunction:: finite_algebras.partition_into_isomorphic_lists
.. autofunction:: finite_algebras.powerset
.. autofunction:: finite_algebras.tables_to_groups
.. autofunction:: finite_algebras.yes_or_no
