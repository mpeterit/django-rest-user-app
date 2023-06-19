from django.urls import include, path

urlpatterns = [
    path('user/', include('user.urls')),
    path('api-auth/', include('rest_framework.urls'))
    ]