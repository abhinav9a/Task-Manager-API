from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.serializers import TaskSerializer, RegisterSerializer
from api.permissions import IsStaffOrReadOnly
from api.models import Task


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None:
            status_filter = status_filter.lower() == 'true'
            queryset = Task.objects.filter(completed=status_filter)
        else:
            queryset = Task.objects.all()
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='status',
                description='Filter tasks by completion status (true: completed, false: not completed)',
                type=bool,
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

        return queryset


class TaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    http_method_names = ['get', 'put', 'delete']

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
