from __future__ import annotations

from dataclasses import replace
import functools
from typing import override

from dataclassabc import dataclassabc

from polymat.typing import (
    ScalarPolynomialExpression,
)

from sosopt.coneconstraints.semidefiniteconstraint import init_semi_definite_constraint
from sosopt.polymat.symbols.auxiliaryvariablesymbol import AuxiliaryVariableSymbol
from sosopt.polymat.from_ import (
    sos_monomial_basis,
    gram_matrix,
)
from sosopt.polynomialconstraints.constraintprimitives.polynomialconstraintprimitive import (
    PolynomialConstraintPrimitive,
)
from sosopt.polymat.symbols.decisionvariablesymbol import DecisionVariableSymbol
from sosopt.polynomialconstraints.polynomialvariablesmixin import (
    PolynomialVariablesMixin,
)


@dataclassabc(frozen=True, slots=True)
class SumOfSquaresPrimitive(PolynomialVariablesMixin, PolynomialConstraintPrimitive):
    name: str
    expression: ScalarPolynomialExpression
    polynomial_variable_indices: tuple[int, ...]
    decision_variable_symbols: tuple[DecisionVariableSymbol, ...]
    sparse_smr: bool

    @functools.cached_property
    def auxilliary_variable_symbol(self):
        return AuxiliaryVariableSymbol(self.name)

    @functools.cached_property
    def sos_monomial_basis(self):
        return sos_monomial_basis(
            expression=self.expression,
            variables=self.polynomial_variable,
            sparse_smr=self.sparse_smr,
        ).cache()

    @functools.cached_property
    def gram_matrix(self):
        return gram_matrix(
            expression=self.expression,
            variables=self.polynomial_variable,
            monomials=self.sos_monomial_basis,
            auxilliary_variable_symbol=self.auxilliary_variable_symbol,
            sparse_smr=self.sparse_smr,
        ).cache()

    def copy(self, /, **others):
        return replace(self, **others)

    @override
    def to_cone_constraint(self):
        return init_semi_definite_constraint( 
            name=self.name,
            expression=self.gram_matrix,
            decision_variable_symbols=None,     # enforce reevaluation of decision variables
        )


def init_sum_of_squares_primitive(
    name: str,
    expression: ScalarPolynomialExpression,
    polynomial_variable_indices: tuple[int, ...],
    decision_variable_symbols: tuple[DecisionVariableSymbol, ...],
    sparse_smr: bool,
):

    return SumOfSquaresPrimitive(
        name=name,
        expression=expression,
        polynomial_variable_indices=polynomial_variable_indices,
        decision_variable_symbols=decision_variable_symbols,
        sparse_smr=sparse_smr,
    )
