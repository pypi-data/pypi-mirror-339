from typing import override
from dataclasses import replace
from dataclassabc import dataclassabc

from polymat.utils.getstacklines import FrameSummary
from polymat.typing import (
    ExpressionNode,
    VariableExpression,
    MonomialVectorExpression,
)

from sosopt.polymat.symbols.auxiliaryvariablesymbol import AuxiliaryVariableSymbol
from sosopt.polymat.sources.decisionvariableexpression import (
    DecisionVariableVectorSymbolExpression,
)
from sosopt.polymat.symbols.decisionvariablesymbol import DecisionVariableSymbol
from sosopt.polymat.sources.polynomialvariable import (
    PolynomialMatrixVariable,
    ScalarPolynomialVariable,
)
from sosopt.polymat.operations.sosmonomialbasis import (
    SOSMonomialBasis,
)
from sosopt.polymat.operations.sosmonomialbasissparse import (
    SOSMonomialBasisSparse,
)
from sosopt.polymat.operations.grammatrix import (
    GramMatrix,
)
from sosopt.polymat.operations.grammatrixsparse import (
    GramMatrixSparse,
)


@dataclassabc(frozen=True, slots=True)
class DecisionVariableExpressionImpl(DecisionVariableVectorSymbolExpression):
    child: ExpressionNode
    symbol: DecisionVariableSymbol

    @override
    def copy(self, /, **changes):
        return replace(self, **changes)


def init_decision_variable_expression(
    child: ExpressionNode, symbol: DecisionVariableSymbol
):
    return DecisionVariableExpressionImpl(
        child=child,
        symbol=symbol,
    )


@dataclassabc(frozen=True, slots=True)
class PolynomialMatrixVariableImpl(PolynomialMatrixVariable):
    name: str
    child: ExpressionNode
    coefficients: tuple[tuple[VariableExpression]]
    shape: tuple[int, int]
    monomials: MonomialVectorExpression

    @override
    def copy(self, /, **changes):
        return replace(self, **changes)


@dataclassabc(frozen=True, slots=True)
class ScalarPolynomialVariableImpl(ScalarPolynomialVariable):
    name: str
    child: ExpressionNode
    coefficient: VariableExpression
    monomials: MonomialVectorExpression

    @override
    def copy(self, /, **changes):
        return replace(self, **changes)


def init_polynomial_variable(
    name: str,
    child: ExpressionNode,
    coefficients: tuple[tuple[VariableExpression]],
    monomials: MonomialVectorExpression,
    shape: tuple[int, int] = (1, 1),
):
    if shape == (1, 1):
        return ScalarPolynomialVariableImpl(
            name=name,
            monomials=monomials,
            coefficient=coefficients[0][0],
            child=child,
        )
    else:
        return PolynomialMatrixVariableImpl(
            name=name,
            monomials=monomials,
            coefficients=coefficients,
            child=child,
            shape=shape,
        )


@dataclassabc(frozen=True, slots=True, repr=False)
class GramMatrixImpl(GramMatrix):
    child: ExpressionNode
    monomials: ExpressionNode
    variables: GramMatrix.VariableType
    auxilliary_variable_symbol: AuxiliaryVariableSymbol | None
    stack: tuple[FrameSummary, ...]


def init_gram_matrix(
    child: ExpressionNode,
    variables: GramMatrix.VariableType,
    monomials: ExpressionNode | None = None,
    auxilliary_variable_symbol: AuxiliaryVariableSymbol | None = None,
):
    if monomials is None:
        monomials = init_sos_monomial_basis(child=child, variables=variables)

    return GramMatrixImpl(
        child=child,
        variables=variables,
        monomials=monomials,
        auxilliary_variable_symbol=auxilliary_variable_symbol,
        stack=GramMatrix.get_frame_summary(),
    )


@dataclassabc(frozen=True, slots=True, repr=False)
class GramMatrixSparseImpl(GramMatrixSparse):
    child: ExpressionNode
    monomials: ExpressionNode
    variables: ExpressionNode.VariableType
    stack: tuple[FrameSummary, ...]


def init_gram_matrix_sparse(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
    monomials: ExpressionNode | None = None,
):
    if monomials is None:
        monomials = init_sos_monomial_basis_sparse(child=child, variables=variables)

    return GramMatrixSparseImpl(
        child=child,
        variables=variables,
        monomials=monomials,
        stack=GramMatrixSparse.get_frame_summary(),
    )


@dataclassabc(frozen=True, slots=True)
class QuadraticMonomialVectorImpl(SOSMonomialBasis):
    child: ExpressionNode
    variables: SOSMonomialBasis.VariableType


def init_sos_monomial_basis(
    child: ExpressionNode,
    variables: SOSMonomialBasis.VariableType,
):
    return QuadraticMonomialVectorImpl(
        child=child,
        variables=variables,
    )


@dataclassabc(frozen=True, slots=True)
class QuadraticMonomialVectorSparseImpl(SOSMonomialBasisSparse):
    child: ExpressionNode
    variables: ExpressionNode.VariableType


def init_sos_monomial_basis_sparse(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
):
    return QuadraticMonomialVectorSparseImpl(child=child, variables=variables)
