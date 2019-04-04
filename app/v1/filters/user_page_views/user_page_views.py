from v1.filters.common import filter_query_params
from datetime import date

def user_page_views_filter(request, query):
    """
    Filter results based on request query parameters
    """

    allowed = {
        'user': lambda x: int(x),
        'post': lambda x: int(x), 
        'created__startswith': lambda x: date(x),
        'created__year': lambda x: date(x).year,
        'created__month': lambda x: date(x).month,
        'created__day': lambda x: date(x).day,
    }

    return filter_query_params(allowed, query, request)
