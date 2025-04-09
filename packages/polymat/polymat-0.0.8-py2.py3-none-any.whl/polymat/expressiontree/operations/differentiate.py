from abc import abstractmethod
from typing import override

from polymat.sparserepr.data.polynomial import differentiate_polynomial
from polymat.sparserepr.sparserepr import SparseRepr
from polymat.state.state import State
from polymat.expressiontree.nodes import (
    SingleChildExpressionNode,
)
from polymat.utils.getstacklines import FrameSummaryMixin, to_operator_traceback
from polymat.sparserepr.init import init_sparse_repr_from_data


class Differentiate(FrameSummaryMixin, SingleChildExpressionNode):
    @property
    @abstractmethod
    def variables(self) -> SingleChildExpressionNode.VariableType: ...

    def __str__(self):
        return f"diff({self.child}, {self.variables})"

    @override
    def apply(self, state: State) -> tuple[State, SparseRepr]:
        state, child = self.child.apply(state=state)
        state, indices = self.to_variable_indices(state, self.variables)

        if not (child.shape[1] == 1):
            raise AssertionError(
                to_operator_traceback(
                    message=f"{child.shape[1]=} is not 1",
                    stack=self.stack,
                )
            )

        def gen_polynomial_matrix():
            for row in range(child.shape[0]):
                polynomial = child.at(row, 0)

                if polynomial:
                    for col, index in enumerate(indices):
                        derivative = differentiate_polynomial(polynomial, index)

                        if derivative:
                            yield (row, col), derivative

        data = dict(gen_polynomial_matrix())

        return state, init_sparse_repr_from_data(
            data=data,
            shape=(child.shape[0], len(indices)),
        )
