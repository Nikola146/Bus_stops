# from django.urls import path
#
# from api import views
#

# Copy code
from django.urls import path
from rest_framework import routers

from api import views


urlpatterns = [
    path('routes/<int:stop_id>/', views.RouteListAPIView.as_view(), name='route-list'),
    path('next-stoptimes/<int:stop_id>/<str:route_id>/', views.NextStopTimeListView.as_view(),
         name='next-stoptimes-list'),
    path('stops/list/', views.StopListAreasView.as_view()),
    path('stops/list/<str:stop_area>/', views.StopListAreasView.as_view()),
    path('stops/area/<str:stop_area>/', views.StopListView.as_view()),
    path('coordinates/', views.coordinates_view),
]