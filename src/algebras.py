"""
@author: Alfred J. Reich

"""

# Standard Library Imports
from itertools import combinations, permutations, product
from json import dump, dumps, load
from os import getenv, path
from collections import Counter
from functools import reduce
from pprint import pprint

# Non-Standard Library Imports
from numpy import array, array_equal, full, int64, where


class Group:
    """A finite group (abstract algebra)

    Internally, the Group object consists of four quantities:

    - `name`: (string) A short name for the Group;
    - `description`: (string) Any additional, useful information about the Group;
    - `element_names`: (list of strings) The Group's element names, where the first element in the list is the Group's
      identity element (usually denoted by 'e');
    - `mult_table`: (list of lists of integers) The Group's multiplication table, where each list in the list
      represents a row of the table, and each integer represents the position of an element in 'element_names'.
      The table must be square, where the row or column length is the same as the number of elements (say, n).
      The first row and column should be the [0, 1, 2, ..., n], in that exact order.  Every row and column should
      contain the same integers, in a different order, as long as no row or column contains the same integer twice.

    A Group object can be instantiated in several ways:

    1. Enter four values corresponding to the quantities described above, in the order shown above.

    2. Enter three values corresponding to `name`, `description`, and `mult_table`, where `mult_table` uses element
       names (strings) instead of integer positions.  The string-based mult_table must follow rules, similar to those
       described above: 1. identity element comes first in the first row and first column, 2. The names in the first
       row and column should be in the same order, and 3. No row or column contains the same element name twice.

    3. Enter a Python dictionary, with keys and values corresponding to either the four value or three value input
       schemes, described above.

    4. Enter a string representing the path to a JSON file that corresponds to the dictionary described above in 3.

    Examples:

    .. code-block:: python

       Group('v_4',
             'Klein-4 group',
             ['e',  'h',  'v', 'hv'],
             [[0, 1, 2, 3],
              [1, 0, 3, 2],
              [2, 3, 0, 1],
              [3, 2, 1, 0]])

       Group('v_4_VERSION2',
             'Klein-4 group again -- defined using element names in the mult_table',
             [[ 'e', 'h' ,  'v', 'hv'],
              [ 'h', 'e' , 'hv', 'v' ],
              [ 'v', 'hv',  'e', 'h' ],
              ['hv', 'v' ,  'h', 'e' ]])

    For more examples of Group instantiation, see the Jupyter Notebook: `ways_to_create_a_group`.

    A final note regarding the interpretation of the multiplication table, the row element is multiplied on the left
    and the column element on the right, e.g., row * col.  Or, assuming functions written on the left, such as
    permutations, this means that the column element is applied first and the row element is applied next,
    e.g., row(col(x)).

    """

    def __init__(self, *args):

        if len(args) == 1:
            if isinstance(args[0], str):
                with open(args[0], 'r') as fin:
                    # Assumes the single argument is a JSON file name string
                    grp_dict = load(fin)
            elif isinstance(args[0], dict):
                # Assumes the single argument is a dictionary
                grp_dict = args[0]
            else:
                # TODO: Allow for just a table to be input (list of lists of element name strings)
                # No other options for single input arguments
                raise Exception("Single argument must be a string or a dictionary.")

        # The following assumes that no element_names list is input, and the table is
        # input using element names instead of indices of the elements.  So, the first
        # row of the table acts as the element_names list.
        elif len(args) == 3:
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2][0],  # top row of table input
                        'mult_table': index_table_from_name_table(args[2])
                        }
        else:
            # Assumes all four possible fields were input
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2],
                        'mult_table': args[3]
                        }
        self.name = grp_dict['name']
        self.description = grp_dict['description']

        if grp_dict.get('element_names'):
            self.element_names = grp_dict['element_names']
        else:
            self.element_names = grp_dict['mult_table'][0]  # First row of table

        tbl = grp_dict['mult_table']
        if isinstance(tbl[0][0], str):
            table = index_table_from_name_table(tbl)
        else:
            table = tbl
        self.mult_table = array(table, dtype=int64)

        self.__dp_delimiter = ':'  # name delimiter used when creating direct products

        if check_inputs(self.element_names, self.mult_table):
            self.__inverse_lookup_dict = self.__make_inverse_lookup_dict()

    def __str__(self):
        """Return a string that identifies the object's class, name, and description."""
        return f"<{self.__class__.__name__}: {self.name}, {self.description}>"

    def __repr__(self):
        """Return a readable representation of the Group.

        NOTE: The method, `pprint`, also does this, but Pretty Prints the Group.
        """
        nm = self.name
        desc = self.description
        elems = self.element_names
        tbl = self.mult_table
        # return f"{self.__class__.__name__}('{nm}', '{desc}', {elems}, {tbl}) "
        return f"{self.__class__.__name__}('{nm}',\n'{desc}',\n{elems},\n{tbl.tolist()}) "

    def __len__(self):
        """Return the order of the Group, i.e., the number of elements in it."""
        return len(self.element_names)

    @property
    def order(self):
        """Return the order of the Group, i.e., the number of elements in it."""
        return len(self.element_names)

    def element_order(self, element):
        """Return the order of a particular element of the Group.

        :param element: An element name
        :type element: str
        """
        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.mult(prod, elem), order + 1)
        return order_aux(element, element, 1)

    def element_orders(self, reverse=False):
        """Return a dictionary where the keys are element names and the values are
        their orders.

        :param reverse: If True, then the dict has orders for keys and element sets for values; defaults to False.
        :type reverse: boolean
        """
        order_dict = {elem: self.element_order(elem) for elem in self.element_names}
        if reverse:
            reverse_dict = {}
            for key, val in order_dict.items():
                reverse_dict.setdefault(val, []).append(key)
            return reverse_dict
        else:
            return order_dict

    def __eq__(self, other):
        """Return True if this Group is identical to the `other` Group."""
        return (self.element_names == other.element_names) and array_equal(self.mult_table, other.mult_table)

    @property
    def identity(self):
        """Return the identity element of the Group"""
        return self.element_names[0]

    def direct_product_delimiter(self, delimiter=None):
        """If no input, then return the current direct product element name delimiter, or set the new delimiter.

        :param delimiter: If None, return current delimiter; otherwise set new delimiter
        :type delimiter: None or str
        """
        if delimiter:
            self.__dp_delimiter = delimiter
            return self.__dp_delimiter
        else:
            return self.__dp_delimiter

    def __make_inverse_lookup_dict(self):
        """(Private Method) Return a dictionary of element names and their inverse names."""
        row_indices, col_indices = where(self.mult_table == 0)
        return {self.element_names[elem_index]: self.element_names[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def to_dict(self):
        """Return a dictionary that represents this Group."""
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'element_names': self.element_names,
                'mult_table': self.mult_table.tolist()}

    def dumps(self):
        """Write the Group to a JSON string."""
        return dumps(self.to_dict())

    def dump(self, json_filename):
        """Write the Group to a JSON file.

        :param json_filename: Complete path to a JSON file
        :type json_filename: str
        """
        with open(json_filename, 'w') as fout:
            dump(self.to_dict(), fout)

    def inverse(self, element_name):
        """Return the name of the inverse element for the input `element_name`.

        :param element_name: An element name
        :type element_name: str
        """
        return self.__inverse_lookup_dict[element_name]

    def mult_table_with_names(self):
        """Return the multiplication table with element names rather than element positions."""
        return [[self.element_names[elem_pos] for elem_pos in row] for row in self.mult_table]

    def mult(self, *args):
        """Multiply zero or more elements using the multiplication table.

        :param args: Zero or more element names separated by commas
        :type args: str
        """
        # If no args, return the identity
        if len(args) == 0:
            return self.element_names[0]
        # If one arg, and it's a valid element name, then just return it
        elif len(args) == 1:
            if args[0] in self.element_names:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid Group element name")
        # If two args, then look up their sum in the multiplication table
        elif len(args) == 2:
            row = self.element_names.index(args[0])
            col = self.element_names.index(args[1])
            index = self.mult_table[row, col]
            return self.element_names[index]
        # If more than two args, then multiply them all together
        else:
            return reduce(lambda a, b: self.mult(a, b), args)

    def pprint(self, use_element_names=False):
        """Pretty print the Group.  This method produces a readable representation of
        the Group.  That is, the output (strings) created by this method can be read back in
        to create a copy of the Group.  By default, the four basic components of the Group
        are printed: Name, Description, Element Names List, and Multiplication Table,
        where the table contains the indices (integers) of elements according to the
        element_names list.  If use_element_names is set to True, then the element names
        list is omitted in the printout and the table is printed using element names.
        """
        print(f"{self.__class__.__name__}('{self.name}',")
        print(f"'{self.description}',")
        if use_element_names:
            pprint(self.mult_table_with_names())
        else:
            print(f"{self.element_names},")
            pprint(self.mult_table.tolist())
        print(")")
        return None

    # def pretty_print_mult_table(self, delimiter=' ', prefix=''):
    #     """Print the multiplication table (Cayley table) using element names."""
    #     field_size = 1 + len(max(self.element_names, key=len))  # 1 + Longest Name Length
    #     for row_index in self.mult_table[:, 0]:  # row index from first column
    #         row_string = f"{prefix}"
    #         for col_index in self.mult_table[0]:  # column index from first row
    #             prod_index = self.mult_table[row_index, col_index]
    #             prod_name = self.element_names[prod_index]
    #             row_string += delimiter + f"{prod_name :>{field_size}}"
    #         print(row_string)

    def associative(self):
        """A brute force test of associativity.  Returns True if the Group is associative."""
        result = True
        for a in self.element_names:
            for b in self.element_names:
                for c in self.element_names:
                    if not (self.mult(self.mult(a, b), c) == self.mult(a, self.mult(b, c))):
                        result = False
                        break
        return result

    # Direct Product Definition
    def __mul__(self, other):
        """Return the direct product of this Group with the `other` Group."""
        dp_name = f"{self.name}_x_{other.name}"
        dp_description = "Direct product of " + self.name + " & " + other.name
        dp_element_names = list(product(self.element_names, other.element_names))  # Cross product
        dp_mult_table = list()
        for a in dp_element_names:
            dp_mult_table_row = list()  # Start a new row
            for b in dp_element_names:
                dp_mult_table_row.append(dp_element_names.index((self.mult(a[0], b[0]), other.mult(a[1], b[1]))))
            dp_mult_table.append(dp_mult_table_row)  # Append the new row to the table
        return self.__class__(dp_name,
                              dp_description,
                              list([f"{elem[0]}{self.__dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                              dp_mult_table)

    def print_info(self, max_size=12, prefix='  '):
        """Pretty print information about the Group."""
        print(f"\n{self.__class__.__name__} : {self.name} : {self.description}")
        print(f"{prefix}Element Names: {self.element_names}")
        print(f"{prefix}Is Abelian? {self.abelian()}")
        # Don't calculate/print the following info if the Group is greater than max_size
        print(f"{prefix}Inverses:  (** - indicates that it is its own inverse)")
        for elem in self.element_names:
            footnote = ''
            inv_elem = self.inverse(elem)
            if elem == inv_elem:
                footnote = '  **'
            print(f"{prefix}  inv({elem}) = {self.inverse(elem)} {footnote}")
        print(f"Element Orders:")
        pprint(self.element_orders(True), indent=2)
        size = len(self.element_names)
        if size <= max_size:
            print(f"{prefix}Is associative? {self.associative()}")
            print(f"{prefix}Cayley Table:")
            # self.pretty_print_mult_table(prefix=prefix)
            pprint(self.mult_table_with_names())
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so no further info calculated/printed.")

    def abelian(self):
        """Returns True if the Group is commutative (abelian)."""
        result = True
        for e1 in self.element_names:
            for e2 in self.element_names:
                if not (self.mult(e1, e2) == self.mult(e2, e1)):
                    result = False
                    break
        return result

    def commutative(self):
        """Returns True if the Group is commutative (abelian)."""
        return self.abelian()

    def closure(self, subset_of_elements):
        """Given a subset (in list form) of the Group's elements, find the smallest possible
        set of elements, containing the subset, that is closed under Group multiplication,
        with inverses."""

        # Make sure inverses are considered
        result = set(subset_of_elements)
        for elem in subset_of_elements:
            result.add(self.inverse(elem))

        # Add the products of all possible pairs
        for pair in product(result, result):
            result.add(self.mult(*pair))

        # If the input set of elements increased, recurse ...
        if len(result) > len(subset_of_elements):
            return self.closure(result)

        # ...otherwise, stop and return the result
        else:
            return list(result)

    def closed_subsets_of_elements(self):
        """Return all unique closed subsets of the Group's elements.
        This returns a list of lists. Each list represents the elements of a subgroup."""
        closed = set()  # Build the result as a set of sets to avoid duplicates
        all_elements = self.element_names
        n = len(all_elements)
        for i in range(2, n - 1):  # avoids trivial closures, {'e'} & set of all elements
            # Look at all combinations of elements: pairs, triples, quadruples, etc.
            for combo in combinations(all_elements, i):
                clo = frozenset(self.closure(combo))  # freezing required to add a set to a set
                if len(clo) < n:  # Don't include closures consisting of all elements
                    closed.add(clo)
        return list(map(lambda x: list(x), closed))

    def subgroup(self, closed_subset_of_elements, name="No name", desc="No description"):
        """Return the Group constructed from the input, closed subset of elements."""
        # Make sure the elements are sorted according to their order in the parent Group (self)
        elements_sorted = sorted(closed_subset_of_elements, key=lambda x: self.element_names.index(x))
        table = []
        for a in elements_sorted:
            row = []
            for b in elements_sorted:
                # The table entry is the index of the product in the sorted elements list
                row.append(elements_sorted.index(self.mult(a, b)))
            table.append(row)
        return Group(name, desc, elements_sorted, table)

    def proper_subgroups(self):
        """Return a list of proper subgroups of the Group"""
        desc = f"Subgroup of: {self.description}"
        count = 0
        list_of_subgroups = []
        for closed_element_set in self.closed_subsets_of_elements():
            name = f"{self.name}_subgroup_{count}"
            count += 1
            list_of_subgroups.append(self.subgroup(closed_element_set, name, desc))
        return list_of_subgroups

    def reorder_elements(self, reordered_elements):
        """Return a new group made from this one with the elements reordered."""
        n = self.order
        new_table = full((n, n), 0)
        for row in range(n):
            for col in range(n):
                prod = self.mult(reordered_elements[row], reordered_elements[col])
                new_table[row, col] = reordered_elements.index(prod)
        new_name = str(self.name) + '_REORDERED'
        new_desc = str(self.description) + ' (elements reordered)'
        return Group(new_name, new_desc, reordered_elements, new_table)

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this group's elements to all possible permutations
        of other's elements, where the identity of this group is always mapped to the identity of other."""
        elems0 = self.element_names
        elems1 = other.element_names
        mappings = [dict(zip(elems0[1:], perm)) for perm in permutations(elems1[1:])]
        for mapping in mappings:
            mapping[elems0[0]] = elems1[0]
        return mappings

    def isomorphic_mapping(self, other, mapping):
        """Returns True if the input mapping from this group to the other group is isomorphic."""
        elems = self.element_names
        return all([mapping[self.mult(x, y)] == other.mult(mapping[x], mapping[y]) for x in elems for y in elems])

    def isomorphic(self, other):
        """If there is a mapping from elements of this group to the other group's elements,
        return it; otherwise return False."""
        maps = self.element_mappings(other)
        for mp in maps:
            if self.isomorphic_mapping(other, mp):
                return mp
        return False


# Group Generators

def generate_cyclic_group(order, identity_name="e", elem_name="a", name=None, description=None):
    """Returns a cyclic Group with the input order, where 'order' is a positive integer."""
    if name:
        nm = name
    else:
        nm = "Z" + str(order)
    if description:
        desc = description
    else:
        desc = f"Autogenerated cyclic group of order {order}"
    elements = [identity_name, elem_name] + [f"{elem_name}^" + str(i) for i in range(2, order)]
    table = [[((a + b) % order) for b in range(order)] for a in range(order)]
    return Group(nm, desc, elements, table)


# Utilities


def duplicates(lst):
    """Return a list of the duplicate items in the input list.

    This function is used by `check_inputs`."""
    return [item for item, count in Counter(lst).items() if count > 1]


def check_inputs(element_names, mult_table):
    """Check that the element_list and mult_table have sizes and contents
    that don't violate the attributes of a group.

    This function is used by the Group constructor."""

    # Check for duplicate element names
    # element_set = set(element_names)
    dups = duplicates(element_names)
    if len(dups) == 0:
        pass
    else:
        raise ValueError(f"Duplicate element names: {dups}")

    # Check that table is square
    rows, cols = mult_table.shape
    if rows == cols:
        pass
    else:
        raise ValueError(f"The table is not square: {rows}x{cols}")

    # Check that the row-col dimensions are the same as the number of elements

    num_elements = len(element_names)
    if rows == num_elements:
        pass
    else:
        raise ValueError(f"Number of elements is {num_elements}, but table size is {rows}x{cols}")

    # Check that each table row contains the correct values for a Cayley table
    correct_indices = set(range(num_elements))  # {0, 1, 2, ..., n-1}
    row_number = -1
    for row in mult_table:
        row_number += 1
        if set(row) == correct_indices:
            pass
        else:
            raise ValueError(f"A row {row_number} does not contain the correct values")

    # Check that each table col contains the correct values for a Cayley table
    for col_number in range(num_elements):
        if set(mult_table[:, col_number]) == correct_indices:
            pass
        else:
            raise ValueError(f"Column {col_number} does not contain the correct values")

    return True


def index_table_from_name_table(name_table):
    """Given a Cayley table using element names, return a table that uses position indices.
    Assumes that the first element in the first row of the table is the identity for the
    table's algebra.

    This function is used by the Group constructor."""
    top_row = name_table[0]
    return [[top_row.index(elem_name) for elem_name in row] for row in name_table]


# def values_in_order(seq):
#     starts_with_zero = (seq[0] == 0)
#     print(f"Starts with zero? {starts_with_zero}")
#     increasing_by_one = all([((seq[i + 1] - seq[i]) == 1) for i in range(len(seq) - 1)])
#     print(f"Increasing by one? {increasing_by_one}")
#     return starts_with_zero and increasing_by_one


def make_table(table_string):
    """This function helps turn the XML-based tables at Groupprops into a
    list of lists for use here.

    Instructions for use:
    1. Copy the table from there and paste it here;
    2. Find & Replace the strings, "<row>" and "</row>", with nothing;
    3. Place triple quotes around the result and give it a variable name;
    4. Then run make_table on the variable.
    """
    return [[int(n) for n in row.strip().split(" ")]
            for row in table_string.splitlines()]


def _no_conflict(p1, p2):
    """Returns True only if no element of p1 equals the corresponding element of p2."""
    return all([p1[i] != p2[i] for i in range(len(p1))])


def _no_conflicts(items):
    """Return True if each possible pair, from a list of items, has no conflicts."""
    return all(_no_conflict(combo[0], combo[1]) for combo in combinations(items, 2))


def _filter_out_conflicts(perms, perm, n):
    """Filter out all permutations in perms that confict with perm,
    and don't have n as the first element."""
    nperms = [q for q in perms if q[0] == n]
    return [p for p in nperms if _no_conflict(p, perm)]


def generate_all_group_tables(order):
    """Return a list of all arrays that correspond to multiplication tables for groups of a specific order """
    row0 = list(range(order))
    row_candidates = [[row0]]
    for row_num in range(1, order):
        row_candidates.append(_filter_out_conflicts(permutations(row0), row0, row_num))
    table_candidates = list(product(*row_candidates))
    return [tbl for tbl in table_candidates if _no_conflicts(tbl)]


def tables_to_groups(tables, identity_name="e", elem_name="a"):
    order = len(tables[0])
    groups = []
    for j in range(len(tables)):
        gname = f"G{j}"
        desc = f"Group {j} of order {order}"
        ename = elem_name + str(j)
        elements = [identity_name + str(j)] + [f"{ename}" + str(i) for i in range(1, order)]
        groups.append(Group(gname, desc, elements, tables[j]))
    return groups

# def swap_list_items(lst, item1, item2):
#     a, b = lst.index(item1), lst.index(item2)
#     lst[b], lst[a] = lst[a], lst[b]
#     return None

# def swap_rows(arr, i, j):
#     """Swap the i_th and j_th rows of a numpy array.
#
#     This function is not used yet."""
#     arr[[i, j], :] = arr[[j, i], :]
#     return arr


# def swap_cols(arr, i, j):
#     """Swap the i_th and j_th columns of a numpy array.
#
#     This function is not used yet."""
#     arr[:, [i, j]] = arr[:, [j, i]]
#     return arr


# def swap_rows_cols(arr, i, j):
#     """Swap the i_th and j_th rows and columns of a numpy array.
#
#     This function is not used yet."""
#     arr0 = swap_rows(arr, i, j)
#     return swap_cols(arr0, i, j)


if __name__ == '__main__':

    print("\n=======================================================================")

    print("\n--------------")
    print("START OF TESTS")
    print("--------------")

    project_path = path.join(getenv('PYPROJ'), 'abstract_algebra')

    algebras = [Group(path.join(project_path, 'Algebras/v4_klein_4_group.json')),
                Group(path.join(project_path, 'Algebras/z4_cyclic_group_of_order_4.json')),
                Group(path.join(project_path, 'Algebras/s3_symmetric_group_on_3_letters.json')),
                Group(path.join(project_path, 'Algebras/s3x_symmetric_group_OTHER.json')),
                Group(path.join(project_path, 'Algebras/Z2xZ2xZ2.json')),
                Group(path.join(project_path, "Algebras/Pinter_page_29.json")),
                Group(path.join(project_path, "Algebras/Pinter_page_29_VERS2.json")),
                Group(path.join(project_path, "Algebras/a4_alternating_group_on_4_letters.json")),
                Group(path.join(project_path, "Algebras/d3_dihedral_group_of_order_6.json")),
                Group(path.join(project_path, "Algebras/d4_dihedral_group_on_4_vertices.json"))
                ]

    # Create some direct products
    v4_x_z4 = algebras[0] * algebras[1]
    z4_x_s3 = algebras[1] * algebras[2]

    # Extend the list, above, with the direct products, just created:
    algebras.extend([v4_x_z4, z4_x_s3])

    # Show info for each algebra in the list
    for grp in algebras:
        grp.print_info()

    print("\n------------")
    print("END OF TESTS")
    print("------------")
