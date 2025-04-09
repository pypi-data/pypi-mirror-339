from dataclassabc import dataclassabc
from numpy.typing import NDArray

from polymat.symbols.symbol import Symbol
from polymat.utils.getstacklines import FrameSummary
from polymat.sparserepr.sparserepr import SparseRepr
from polymat.expressiontree.nodes import ExpressionNode
from polymat.expressiontree.operations.assertshape import AssertShape
from polymat.expressiontree.operations.blockdiagonal import (
    BlockDiagonal,
)
from polymat.expressiontree.operations.cache import Cache
from polymat.expressiontree.operations.diagonal import Diagonal
from polymat.expressiontree.operations.evaluate import Evaluate
from polymat.expressiontree.operations.filternonzero import FilterNonZero
from polymat.expressiontree.operations.filterpredicator import (
    FilterPredicate,
)
from polymat.expressiontree.sources.fromany import FromAny
from polymat.expressiontree.sources.fromsparserepr import FromSparseRepr
from polymat.expressiontree.sources.fromvariableindices import (
    FromVariableIndices,
)
from polymat.expressiontree.sources.fromvariables import FromVariables
from polymat.expressiontree.operations.kronecker import Kronecker
from polymat.expressiontree.operations.coefficientvector import CoefficientVector
from polymat.expressiontree.operations.monomialvector import (
    MonomialVector,
)
from polymat.expressiontree.operations.product import Product
from polymat.expressiontree.operations.quadraticcoefficients import (
    QuadraticCoefficients,
)
from polymat.expressiontree.operations.quadraticmonomials import (
    QuadraticMonomials,
)
from polymat.expressiontree.operations.repeatmatrix import RepeatMatrix
from polymat.expressiontree.operations.reshape import Reshape
from polymat.expressiontree.operations.getitem import GetItem
from polymat.expressiontree.operations.rowsummation import RowSummation
from polymat.expressiontree.operations.tosymmetricmatrix import ToSymmetricMatrix
from polymat.expressiontree.sources.fromvectortosymmetricmatrix import (
    FromVectorToSymmetricMatrix,
)
from polymat.expressiontree.operations.tovariablevector import (
    ToVariableVector,
)
from polymat.expressiontree.operations.addition import Addition
from polymat.expressiontree.operations.combinations import (
    Combinations,
)
from polymat.expressiontree.operations.differentiate import (
    Differentiate,
)
from polymat.expressiontree.operations.elementwisemult import (
    ElementwiseMult,
)
from polymat.expressiontree.sources.fromnumpy import FromNumpy
from polymat.expressiontree.operations.definevariable import (
    DefineVariable,
)
from polymat.expressiontree.operations.matrixmultiplication import MatrixMultiplication
from polymat.expressiontree.operations.transpose import Transpose
from polymat.expressiontree.operations.truncatemonomials import TruncateMonomials
from polymat.expressiontree.operations.verticalstack import VerticalStack


@dataclassabc(frozen=True, repr=False)
class AdditionImpl(Addition):
    left: ExpressionNode
    right: ExpressionNode
    stack: tuple[FrameSummary, ...]


def init_addition(
    left: ExpressionNode,
    right: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return AdditionImpl(left=left, right=right, stack=stack)


@dataclassabc(frozen=True, repr=False)
class AssertShapeImpl(AssertShape):
    child: ExpressionNode
    func: AssertShape.AssertionType
    message: AssertShape.MessageType
    stack: tuple[FrameSummary, ...]

    def __repr__(self):
        return repr(self.child)


def init_assert_shape(
    child: ExpressionNode,
    func: AssertShape.AssertionType,
    message: AssertShape.MessageType,
    stack: tuple[FrameSummary, ...],
):
    return AssertShapeImpl(child=child, func=func, message=message, stack=stack)


def init_assert_vector(child: ExpressionNode, stack: tuple[FrameSummary, ...]):
    return init_assert_shape(
        child=child,
        stack=stack,
        func=lambda row, col: col == 1,
        message=lambda row, col: f"number of column {col} must be 1",
    )


def init_assert_polynomial(child: ExpressionNode, stack: tuple[FrameSummary, ...]):
    return init_assert_shape(
        child=child,
        stack=stack,
        func=lambda row, col: row == 1 and col == 1,
        message=lambda row, col: f"number of row {row} and column {col} must be both 1",
    )


@dataclassabc(frozen=True, slots=True)
class BlockDiagonalImpl(BlockDiagonal):
    children: tuple[ExpressionNode, ...]


def init_block_diagonal(children: tuple[ExpressionNode, ...]):
    return BlockDiagonalImpl(children=children)


@dataclassabc(frozen=True, repr=False)
class CacheImpl(Cache):
    child: ExpressionNode
    stack: tuple[FrameSummary, ...]


def init_cache(
    child: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return CacheImpl(child=child, stack=stack)


@dataclassabc(frozen=True, repr=False)
class CombinationsImpl(Combinations):
    child: ExpressionNode
    degrees: Combinations.DegreeType
    stack: tuple[FrameSummary, ...]


def init_combinations(
    child: ExpressionNode,
    degrees: Combinations.DegreeType,
    stack: tuple[FrameSummary, ...],
):
    assert len(degrees)

    return CombinationsImpl(
        child=child,
        degrees=degrees,
        stack=stack,
    )


@dataclassabc(frozen=True, repr=False)
class DefineVariableImpl(DefineVariable):
    symbol: Symbol
    size: DefineVariable.SizeType
    stack: tuple[FrameSummary, ...]


def init_define_variable(
    symbol: Symbol,
    stack: tuple[FrameSummary, ...],
    size: DefineVariable.SizeType | None = None,
):
    if size is None:
        size = 1

    return DefineVariableImpl(symbol=symbol, size=size, stack=stack)


@dataclassabc(frozen=True, repr=False)
class DifferentiateImpl(Differentiate):
    child: ExpressionNode
    variables: ExpressionNode.VariableType
    stack: tuple[FrameSummary, ...]


def init_differentiate(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
    stack: tuple[FrameSummary, ...],
):
    return DifferentiateImpl(child=child, variables=variables, stack=stack)


@dataclassabc(frozen=True, repr=False)
class DiagonalImpl(Diagonal):
    child: ExpressionNode
    stack: tuple[FrameSummary, ...]


def init_diagonal(
    child: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return DiagonalImpl(child=child, stack=stack)


@dataclassabc(frozen=True, repr=False)
class ElementwiseMultImpl(ElementwiseMult):
    left: ExpressionNode
    right: ExpressionNode
    stack: tuple[FrameSummary, ...]


def init_elementwise_mult(
    left: ExpressionNode,
    right: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return ElementwiseMultImpl(left=left, right=right, stack=stack)


@dataclassabc(frozen=True, repr=False)
class EvaluateImpl(Evaluate):
    child: ExpressionNode
    substitutions: Evaluate.SubstitutionType
    stack: tuple[FrameSummary, ...]


def init_evaluate(
    child: ExpressionNode,
    substitutions: Evaluate.SubstitutionType,
    stack: tuple[FrameSummary, ...],
):
    return EvaluateImpl(
        child=child,
        substitutions=substitutions, #tuple(substitutions.items()),
        stack=stack,
    )


@dataclassabc(frozen=True, repr=False)
class FilterPredicateImpl(FilterPredicate):
    child: ExpressionNode
    predicate: FilterPredicate.PredicatorType
    stack: tuple[FrameSummary, ...]


# default constructor
def init_filter_predicate(
    child: ExpressionNode,
    predicate: FilterPredicate.PredicatorType,
    stack: tuple[FrameSummary, ...],
):
    return FilterPredicateImpl(
        child=child,
        predicate=predicate,
        stack=stack,
    )


@dataclassabc(frozen=True, repr=False)
class FilterNonZeroImpl(FilterNonZero):
    child: ExpressionNode
    stack: tuple[FrameSummary, ...]


# default constructor
def init_filter_non_zero(
    child: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return FilterNonZeroImpl(
        child=child,
        stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class FromNumpyImpl(FromNumpy):
    data: NDArray


def init_from_numpy(data: NDArray):
    return FromNumpyImpl(data=data)


@dataclassabc(frozen=True, repr=False)
class FromAnyImpl(FromAny):
    data: tuple[tuple[FromAny.ValueType]]
    stack: tuple[FrameSummary, ...]


def init_from_any(
    data: tuple[tuple[FromAny.ValueType]],
    stack: tuple[FrameSummary, ...],
):
    return FromAnyImpl(
        data=data,
        stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class FromSparseReprImpl(FromSparseRepr):
    sparse_repr: SparseRepr


def init_from_sparse_repr(sparse_repr: SparseRepr):
    return FromSparseReprImpl(sparse_repr=sparse_repr)


@dataclassabc(frozen=True, slots=True)
class FromVariablesImpl(FromVariables):
    variables: FromVariables.VARIABLE_TYPE


def init_from_variables(variables: FromVariables.VARIABLE_TYPE):
    return FromVariablesImpl(variables=variables)


@dataclassabc(frozen=True, slots=True)
class FromVariableIndicesImpl(FromVariableIndices):
    indices: tuple[int, ...]
    # stack: tuple[FrameSummary, ...]


def init_from_variable_indices(
    indices: tuple[int, ...],
    # stack: tuple[FrameSummary, ...],
):
    assert isinstance(indices, tuple), f'Indices {indices} is not of type Tuple'

    return FromVariableIndicesImpl(
        indices=indices,
        # stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class KroneckerImpl(Kronecker):
    left: ExpressionNode
    right: ExpressionNode


def init_kronecker(
    left: ExpressionNode,
    right: ExpressionNode,
):
    return KroneckerImpl(left=left, right=right)


@dataclassabc(frozen=True, repr=False)
class CoefficientVectorImpl(CoefficientVector):
    child: ExpressionNode
    monomials: ExpressionNode
    variables: ExpressionNode.VariableType
    ignore_unmatched: bool
    stack: tuple[FrameSummary, ...]


def init_coefficient_vector(
    child: ExpressionNode,
    stack: tuple[FrameSummary, ...],
    variables: ExpressionNode.VariableType | None = None,
    monomials: ExpressionNode | None = None,
    ignore_unmatched: bool = False,
):
    match variables, monomials:
        case None, None:
            raise Exception('Either variables or monomials need to be provided.')
        case _, None:
            monomials = init_monomial_vector(
                child=child,
                variables=variables,
            )
        case None, _:
            variables = init_variable_vector(
                monomials
            )

    return CoefficientVectorImpl(
        child=child,
        variables=variables,
        monomials=monomials,
        ignore_unmatched=ignore_unmatched,
        stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class MonomialVectorImpl(MonomialVector):
    child: ExpressionNode
    variables: ExpressionNode.VariableType


def init_monomial_vector(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
):
    return MonomialVectorImpl(child=child, variables=variables)


@dataclassabc(frozen=True, repr=False)
class MatrixMultiplicationImpl(MatrixMultiplication):
    left: ExpressionNode
    right: ExpressionNode
    stack: tuple[FrameSummary, ...]


def init_matrix_mult(
    left: ExpressionNode,
    right: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return MatrixMultiplicationImpl(left=left, right=right, stack=stack)


@dataclassabc(frozen=True, repr=False)
class ProductImpl(Product):
    children: tuple[ExpressionNode, ...]
    degrees: Product.DegreeType
    stack: tuple[FrameSummary, ...]


def init_product(
    children: tuple[ExpressionNode, ...],
    stack: tuple[FrameSummary, ...],
    degrees: Product.DegreeType,
):
    return ProductImpl(
        children=children,
        stack=stack,
        degrees=degrees,
    )


@dataclassabc(frozen=True, repr=False)
class QuadraticCoefficientsImpl(QuadraticCoefficients):
    child: ExpressionNode
    monomials: ExpressionNode
    variables: ExpressionNode.VariableType
    ignore_unmatched: bool
    stack: tuple[FrameSummary, ...]


def init_quadratic_coefficients(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
    stack: tuple[FrameSummary, ...],
    monomials: ExpressionNode | None = None,
    ignore_unmatched: bool = False,
):
    if monomials is None:
        monomials = init_quadratic_monomials(child=child, variables=variables)

    return QuadraticCoefficientsImpl(
        child=child,
        variables=variables,
        monomials=monomials,
        ignore_unmatched=ignore_unmatched,
        stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class QuadraticMonomialsImpl(QuadraticMonomials):
    child: ExpressionNode
    variables: ExpressionNode.VariableType


def init_quadratic_monomials(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
):
    return QuadraticMonomialsImpl(child=child, variables=variables)


@dataclassabc(frozen=True, slots=True)
class FromVectorToSymmetricMatrixImpl(FromVectorToSymmetricMatrix):
    child: ExpressionNode
    stack: tuple[FrameSummary, ...]


def from_vector_to_symmetric_matrix(
    child: ExpressionNode,
    stack: tuple[FrameSummary, ...],
):
    return FromVectorToSymmetricMatrixImpl(
        child=child,
        stack=stack,
    )


@dataclassabc(frozen=True, slots=True)
class GetItemImpl(GetItem):
    child: ExpressionNode
    key: GetItem.KeyType


def init_get_item(
    child: ExpressionNode,
    key: GetItem.KeyType,
):
    return GetItemImpl(child=child, key=key)


@dataclassabc(frozen=True, slots=True)
class RowSummationImpl(RowSummation):
    child: ExpressionNode


def init_row_summation(child: ExpressionNode):
    return RowSummationImpl(child=child)


@dataclassabc(frozen=True, slots=True)
class ToSymmetricMatrixImpl(ToSymmetricMatrix):
    child: ExpressionNode


def init_to_symmetric_matrix(child: ExpressionNode):
    return ToSymmetricMatrixImpl(child=child)


@dataclassabc(frozen=True, slots=True)
class RepeatMatrixImpl(RepeatMatrix):
    child: ExpressionNode
    repetition: tuple[int, int]


def init_rep_mat(
    child: ExpressionNode,
    repetition: tuple[int, int],
):
    return RepeatMatrixImpl(child=child, repetition=repetition)


@dataclassabc(frozen=True, slots=True)
class ReshapeImpl(Reshape):
    child: ExpressionNode
    new_shape: tuple[int, int]


def init_reshape(
    child: ExpressionNode,
    new_shape: tuple[int, int],
):
    return ReshapeImpl(child=child, new_shape=new_shape)


@dataclassabc(frozen=True, slots=True)
class ToVariableVectorImpl(ToVariableVector):
    child: ExpressionNode


def init_variable_vector(child: ExpressionNode):
    return ToVariableVectorImpl(child=child)


@dataclassabc(frozen=True, slots=True)
class TransposeImpl(Transpose):
    child: ExpressionNode


def init_transpose(child: ExpressionNode):
    return TransposeImpl(child=child)


@dataclassabc(frozen=True, slots=True)
class TruncateMonomialsImpl(TruncateMonomials):
    child: ExpressionNode
    variables: ExpressionNode.VariableType
    degrees: TruncateMonomials.DegreeType


def init_truncate_monomials(
    child: ExpressionNode,
    variables: ExpressionNode.VariableType,
    degrees: TruncateMonomials.DegreeType,
):
    return TruncateMonomialsImpl(child=child, variables=variables, degrees=degrees)


@dataclassabc(frozen=True, repr=False)
class VerticalStackImpl(VerticalStack):
    children: tuple[ExpressionNode, ...]
    stack: tuple[FrameSummary, ...]


def init_v_stack(
    children: tuple[ExpressionNode, ...],
    stack: tuple[FrameSummary, ...],
):
    return VerticalStackImpl(children=children, stack=stack)
