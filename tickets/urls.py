from django.urls import path
from .views import TicketListCreateView, TicketDetailView, TicketCommentView, BreachedTicketsView, TicketsListView, TicketCreateView, TicketDetailPageView

urlpatterns = [
    # API endpoints
    path('api/tickets', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('api/tickets/<int:pk>', TicketDetailView.as_view(), name='ticket-detail'),
    path('api/tickets/<int:pk>/comments', TicketCommentView.as_view(), name='ticket-comment'),
    path('api/tickets/breached', BreachedTicketsView.as_view(), name='breached-tickets'),

    # Template pages
    path('tickets', TicketsListView.as_view(), name='tickets-list'),
    path('tickets/new', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>', TicketDetailPageView.as_view(), name='ticket-detail-page'),
]
