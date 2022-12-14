from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:post_pk>/comments', views.comments_create, name='comments_create'),
    path('<int:post_pk>/like', views.like, name='like'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)