from ninja.pagination import PaginationBase
from ninja import Schema
from typing import Optional, List, Any
from common.utils.urls import replace_query_param, remove_query_param


class Pagination(PaginationBase):
    class Input(Schema):
        limit: int = 25
        offset: int = 0

    class Output(Schema):
        results: List[Any]
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None

    items_attribute: str = "results"

    def paginate_queryset(self, queryset, pagination: Input, request, **params):
        count = queryset.count()
        limit = pagination.limit
        offset = pagination.offset
        return {
            'results': queryset[offset:offset + limit],
            'count': count,
            'next': self.get_next_link(request, count, limit, offset),
            'previous': self.get_previous_link(request, count, limit, offset)
        }

    def get_next_link(self, request, count, limit, offset):
        if offset + limit >= count:
            return None
        url = request.build_absolute_uri()
        return replace_query_param(url, 'offset', offset + limit)

    def get_previous_link(self, request, count, limit, offset):
        if offset == 0:
            return None
        url = request.build_absolute_uri()
        if offset <= limit:
            return remove_query_param(url, 'offset')
        return replace_query_param(url, 'offset', offset - limit)
