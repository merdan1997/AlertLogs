from alertlog import views
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)

router.register('logs',views.AlertLogListApiView)
router.register('role',views.RulesListApiView)
#router.register('filter',views.FilterLogsViewSet)

urlpatterns = [
    path('',views.index , name='home'),
    path('api/', views.TodoListApiView.as_view()),
    path('count/',views.CountLogs.as_view()),
    path('check', views.ProcessDataView.as_view()),
    path('logupdate/',views.LogUpdateView.as_view(), name = "log -update"),
]+router.urls
