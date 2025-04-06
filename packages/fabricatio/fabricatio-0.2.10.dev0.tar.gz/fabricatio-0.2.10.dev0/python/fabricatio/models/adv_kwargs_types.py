"""A module containing kwargs types for content correction and checking operations."""

from importlib.util import find_spec
from typing import Required, Type, TypedDict

from fabricatio.models.extra.problem import Improvement
from fabricatio.models.extra.rag import MilvusDataBase
from fabricatio.models.extra.rule import RuleSet
from fabricatio.models.generic import SketchedAble
from fabricatio.models.kwargs_types import ReferencedKwargs


class CorrectKwargs[T: SketchedAble](ReferencedKwargs[T], total=False):
    """Arguments for content correction operations.

    Extends GenerateKwargs with parameters for correcting content based on
    specific criteria and templates.
    """

    improvement: Improvement


class CheckKwargs(ReferencedKwargs[Improvement], total=False):
    """Arguments for content checking operations.

    Extends GenerateKwargs with parameters for checking content against
    specific criteria and templates.
    """

    ruleset: RuleSet


if find_spec("pymilvus"):
    from pymilvus import CollectionSchema
    from pymilvus.milvus_client import IndexParams

    class CollectionConfigKwargs(TypedDict, total=False):
        """Configuration parameters for a vector collection.

        These arguments are typically used when configuring connections to vector databases.
        """

        dimension: int | None
        primary_field_name: str
        id_type: str
        vector_field_name: str
        metric_type: str
        timeout: float | None
        schema: CollectionSchema | None
        index_params: IndexParams | None

    class FetchKwargs[D: MilvusDataBase](TypedDict, total=False):
        """Arguments for fetching data from vector collections.

        Controls how data is retrieved from vector databases, including filtering
        and result limiting parameters.
        """

        document_model: Required[Type[D]]
        collection_name: str | None
        similarity_threshold: float
        result_per_query: int

    class RetrievalKwargs(FetchKwargs, total=False):
        """Arguments for retrieval operations."""

        final_limit: int
