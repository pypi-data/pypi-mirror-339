# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["DeasySelectQueryParams", "TagSchema"]


class DeasySelectQueryParams(TypedDict, total=False):
    query: Required[str]

    vdb_profile_name: Required[str]

    columns: Optional[List[Literal["id", "filename", "text", "tags", "page_num", "dense", "point_id"]]]

    data_description: Optional[str]

    filter_type: Optional[Literal["deasy", "sql"]]

    max_search_reduction: Optional[float]

    min_search_reduction: Optional[float]

    return_type: Optional[Literal["results", "condition", "both"]]

    tag_level: Optional[Literal["file", "chunk", "both"]]

    tag_names: Optional[List[str]]

    tag_schemas: Optional[Iterable[TagSchema]]


class TagSchema(TypedDict, total=False):
    description: Required[str]

    name: Required[str]

    output_type: Required[str]

    available_values: Optional[List[str]]

    created_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    date_format: Optional[str]

    examples: Optional[List[Union[str, Dict[str, object]]]]

    max_values: Annotated[Union[int, str, Iterable[object], None], PropertyInfo(alias="maxValues")]

    neg_examples: Optional[List[str]]

    retry_feedback: Optional[Dict[str, object]]

    tag_id: Optional[str]

    tuned: Optional[int]

    updated_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    username: Optional[str]
