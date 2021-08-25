import functools as fnc
import itertools as it


def power(x, n):
    result = 1
    for _ in range(n):
        result = result * x
    return result


class Term:
    """Represents a term of a polynomial.  Here's an example polynomial with four
    terms, separated by spaces: -2 -4x +7x^2 -3x^4
    """
    
    def __init__(self, coefficient, order):
        self.__coefficient = coefficient
        self.__order = order
        self.__varname = "x"
        
    def __repr__(self):
        return f"Term({self.__coefficient},{self.__order})"
    
    def __str__(self):
        if self.__coefficient > 0:
            sign = "+"
        else:
            sign = ""
        if self.__order == 0:
            return f"{sign}{self.__coefficient}"
        elif self.__order == 1:
            return f"{sign}{self.__coefficient}{self.__varname}"
        else:
            return f"{sign}{self.__coefficient}{self.__varname}^{self.__order}"
        
    def __call__(self, x):
        return self.__coefficient * power(x, self.__order)
    
    def __add__(self, other):
        if self.__order == other.__order:
            return Term(self.__coefficient + other.__coefficient, self.__order)
        else:
            raise ValueError(f"Terms must be of the same order, {self.__order} != {other.__order}")
    
    def __mul__(self, other):
        return Term(self.__coefficient * other.__coefficient,
                    self.__order + other.__order)
    
    def __eq__(self, other):
        return (self.__varname == other.__varname and
                self.__order == other.__order and
                self.__coefficient == other.__coefficient)
    
    @property
    def coefficient(self):
        return self.__coefficient
    
    @property
    def order(self):
        return self.__order
    
    def varname(self, newname=None):
        if newname is not None:
            if isinstance(newname, str):
                self.__varname = newname
            else:
                raise ValueError("Variable name must be a string.")
        return self.__varname
    
    def is_constant(self):
        if self.__order == 0:
            return self.__coefficient
        else:
            return False
        
    def is_linear(self):
        if self.__order == 1:
            return self.__coefficient
        else:
            return False


class Polynomial:
    """A callable class for polynomials.  The constructor takes the polynomial as a 
    single string, as long as the terms of the polynomial are separated by spaces.
    
    Example: Polynomial('-4x -2 -3x^4 +7x^2', 'x') ==> '-2 -4x 7x^2 -3x^4'
    """
    
    def __init__(self, poly_string, varname):
        self.__terms = [term for term in combine_like_terms(parse_polynomial(poly_string, varname))
                        if term.coefficient != 0]
        if len(self.__terms) == 0:
            self.__terms.append(Term(0, 0))

    def __repr__(self):
        poly_str = ""
        for term in self.__terms:
            poly_str += " " + str(term)
        return poly_str
    
    def __call__(self, x):
        return fnc.reduce(lambda a, b: a + b, map(lambda term: term(x), self.__terms))
    
    def terms(self):
        return self.__terms


def parse_term(term_str, varname):
    """A hacky term string parser.  Returns a Term from the input string."""

    if varname in term_str:
        varpower = varname + "^"
        if varpower in term_str:
            args = list(map(lambda x: int(x), term_str.split(varpower)))
        else:
            foo = term_str.split(varname)[0]
            if foo == '+' or foo == '-':
                coeff_str = foo + '1'
                args = [int(coeff_str), 1]
            else:
                args = [int(foo), 1]
    else:
        args = [int(term_str), 0]

    return Term(args[0], args[1])


def parse_polynomial(poly_str, varname):
    """An extreme hack.  Terms in polynomials have to be separated by a space.
    Example polynomial string where varname is 'x': '-2 -4x +7x^2 -3x^4'
    """
    return [parse_term(term, varname) for term in poly_str.split()]


def combine_like_terms(terms):
    """Given a list of Terms, this function returns a possibly smaller list of Terms,
    where terms with the same order ("like terms") have been combined."""
    result = list()
    # NOTE: 'groupby' **requires** the input list be sorted on the key used for grouping
    terms_sorted = sorted(terms, key=lambda x: x.order)
    for _, like_terms in it.groupby(terms_sorted, lambda x: x.order):
        combined_term = fnc.reduce(lambda t, s: t + s, like_terms)
        result.append(combined_term)
    return result
