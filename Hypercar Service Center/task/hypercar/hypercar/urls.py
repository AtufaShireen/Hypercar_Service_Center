from django.urls import path
from tickets.views import WelcomeView, TicketView, check_time, ProcessView,next

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', TicketView.as_view()),
    path('get_ticket/<str:service>', check_time),
    path('processing/', ProcessView.as_view()),
    path('next/', next),

]
