from abc import abstractmethod
from typing import Iterable
from typing_extensions import override

from polymat.expressiontree.nodes import ExpressionNode
from polymat.sparserepr.data.polynomialmatrix import MatrixIndexType
from polymat.sparserepr.data.polynomial import PolynomialType
from polymat.sparserepr.sparserepr import SparseRepr
from polymat.state.state import State
from polymat.utils.getstacklines import (
    FrameSummary,
    FrameSummaryMixin,
)
from polymat.symbols.symbol import Symbol
from polymat.sparserepr.init import init_sparse_repr_from_iterable


class DefineVariable(FrameSummaryMixin, ExpressionNode):
    """Underlying object for VariableExpression"""

    SizeType = int | ExpressionNode

    def __str__(self):
        return self.symbol

    @property
    @abstractmethod
    def size(self) -> SizeType:
        """Shape of the variable expression."""

    @property
    @abstractmethod
    def symbol(self) -> Symbol:
        """The symbol representing the variable."""

    @staticmethod
    def create_variable_vector(
        state: State, 
        variable: Symbol, 
        size: int, 
        stack: tuple[FrameSummary, ...]
    ):
        state, (start, stop) = state.register(
            symbol=variable,
            size=size,
            stack=stack,
        )

        def gen_polynomial_matrix() -> Iterable[tuple[MatrixIndexType, PolynomialType]]:
            for row, sym_index in enumerate(range(start, stop)):
                polynomial = {((sym_index, 1),): 1.0}
                yield (row, 0), polynomial

        return state, gen_polynomial_matrix

    @override
    def apply(self, state: State) -> tuple[State, SparseRepr]:
        if isinstance(self.size, int):
            size = self.size
        else:
            state, polymat = self.size.apply(state)
            size = polymat.shape[0] * polymat.shape[1]
            

        state, gen_polynomial_matrix = self.create_variable_vector(
            state,
            variable=self.symbol,
            size=size,
            stack=self.stack,
        )

        return state, init_sparse_repr_from_iterable(
            data=gen_polynomial_matrix(), 
            shape=(size, 1)
        )
