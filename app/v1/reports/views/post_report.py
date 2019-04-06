from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.reports.models.post_report import PostReport
from v1.reports.serializers.post_report import PostReportSerializer, PostReportSerializerCreate, PostReportSerializerUpdate
from v1.utils.permissions import is_administrator, is_moderator

# post_report 
class PostReportView(APIView):

    @staticmethod
    def post(request):
        """
        Create post report
        """

        serializer = PostReportSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(PostReportSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        """
        List post report
        admin and moderator can access all report
        normal users access report reported by himself/herself
        """
        if is_administrator(request.user) or is_moderator(request.user):
            post_reports = PostReport.objects.all()
        else:
            post_reports = PostReport.objects.all().filter(user=request.user)
        return Response(PostReportSerializer(post_reports, many=True).data)


# post_report/{post_report_id}
class PostReportDetail(APIView):

    @staticmethod
    def patch(request, post_report_id):
        """
        Update post report
        only admin and moderator can access this api 
        """
        if not is_administrator(request.user) and not is_moderator(request.user):
            return Response(status.HTTP_400_BAD_REQUEST)

        post_report = get_object_or_404(PostReport, pk=post_report_id)
        serializer = PostReportSerializerUpdate(post_report, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostReportSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def get(request, post_report_id):
        """
        See detail of one post report
        User authentication needed
        """

        post_report = get_object_or_404(PostReport, pk=post_report_id)
        if post_report.user != request.user and not is_administrator(request.user) and not is_moderator(request.user):
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response(PostReportSerializer(PostReportSerializer).data)