from abc import abstractmethod
from typing_extensions import override

from polymat.expressiontree.nodes import ExpressionNode
from polymat.sparserepr.sparserepr import SparseRepr
from polymat.state.state import State
from polymat.symbols.symbol import Symbol
from polymat.sparserepr.init import init_sparse_repr_from_data


# delete?
class FromVariables(ExpressionNode):
    """Underlying object for VariableExpression"""

    VARIABLE_VALUE_TYPE = tuple[Symbol, ...]
    VARIABLE_TYPE = VARIABLE_VALUE_TYPE

    def __str__(self):
        return str(self.variables)

    @property
    @abstractmethod
    def variables(self) -> VARIABLE_TYPE:
        """The symbol representing the variable."""

    @override
    def apply(self, state: State) -> tuple[State, SparseRepr]:
        def gen_polynomial_matrix():
            row = 0
            for variable in self.variables:
                # raises exception if variable doesn't exist
                start, stop = state.get_index_range(variable)

                for index in range(start, stop):
                    monomial = ((index, 1),)
                    yield (row, 0), {monomial: 1}
                    row += 1

        data = dict(gen_polynomial_matrix())
        shape = (len(data), 1)

        return state, init_sparse_repr_from_data(data=data, shape=shape)
