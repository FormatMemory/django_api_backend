from django.conf.urls import url
from .views.category import CategoryView, CategoryDetail


urlpatterns = [

    url(r'^categories$', CategoryView.as_view()),
    url(r'^categories/(?P<category_id>[\d]+)$', CategoryDetail.as_view()),

]
