from django.conf.urls import url
from .views.post_report import PostReportView, PostReportDetail


urlpatterns = [

    # Post replies
    url(r'^post_reports$', PostReportView.as_view()),
    url(r'^post_reports/(?P<post_report_id>[\d]+)$', PostReportDetail.as_view()),

]
