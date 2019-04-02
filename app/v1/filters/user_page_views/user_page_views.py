from v1.filters.common import filter_query_params
from datetime import date

def user_page_views_filter(request, query):
    """
    Filter results based on request query parameters
    """

    allowed = {
        'user': lambda x: int(x),
        'post': lambda x: int(x), 
        'start_time__startswith': lambda x: date(x),
        'start_time__year': lambda x: date(x).year,
        'start_timee__month': lambda x: date(x).month, 
        'start_time__day': lambda x: date(x).day,
    }

    return filter_query_params(allowed, query, request)

