from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lesson, LessonView, UserProductAccess, Product
from .serializers import LessonSerializer, LessonViewSerializer, UserSerializer, GroupSerializer, ProductStatsSerializer
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user.id

        # Get product_ids for products the user has access to
        product_ids = UserProductAccess.objects.filter(id=user, access_status=True).values_list('product_id', flat=True)
        lessons_ids = Lesson.objects.filter(products__in=product_ids).values_list('id', flat=True)

        lesson_views = LessonView.objects.filter(lesson_id__in = lessons_ids).distinct()

        return lesson_views

    @action(detail=False, methods=['GET'])
    def lessons_for_user(self, request):
        lessonviews = self.get_queryset() 
        serializer = LessonViewSerializer(lessonviews, many=True)
        return Response(serializer.data)
    
class LessonOfProductView(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs.get('product_id')  # Get the product_id from URL kwargs

        try:
            product = Product.objects.get(id=product_id, owner_id=user)
        except Product.DoesNotExist:
            return LessonView.objects.none()  # Return an empty queryset if the user havent access

        lesson_views = LessonView.objects.filter(user_id=user, lesson__products=product, viewed_status=True)

        return lesson_views

    @action(detail=False, methods=['GET'])
    def lessons_for_product(self, request, product_id):
        lesson_views = self.get_queryset()  
        serializer = LessonViewSerializer(lesson_views, many=True)
        return Response(serializer.data)
    

    
class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer

    @action(detail=False, methods=['GET'])
    def product_stats(self, request):
        total_users = User.objects.count()
        products = Product.objects.annotate(
            num_lessons_viewed=Count('lessons__lessonview', filter=F('lessons__lessonview__viewed_status')),
            total_viewing_time=Sum('lessons__lessonview__viewing_time_seconds'),
            num_users_accessing=Count('userproductaccess__user', distinct=True),
            access_percentage=ExpressionWrapper(
                Count('userproductaccess') * 100 / total_users,
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        )

        serializer = ProductStatsSerializer(products, many=True)
        return Response(serializer.data)




