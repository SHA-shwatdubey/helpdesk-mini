
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Ticket, Comment, Timeline
from .serializers import TicketSerializer, CommentSerializer
from django.contrib.auth.models import User

class TicketListCreateView(generics.ListCreateAPIView):
	serializer_class = TicketSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'description', 'comments__content']

	def get_queryset(self):
		queryset = Ticket.objects.all().order_by('-created_at')
		search = self.request.query_params.get('search')
		if search:
			queryset = queryset.filter(
				Q(title__icontains=search) |
				Q(description__icontains=search) |
				Q(comments__content__icontains=search)
			).distinct()
		return queryset

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)

	# API Views
class TicketDetailView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk)
		return Response(TicketSerializer(ticket).data)

	def patch(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk)
		client_version = request.data.get('version')
		if client_version is None or int(client_version) != ticket.version:
			return Response({'detail': 'Stale update.'}, status=409)
		serializer = TicketSerializer(ticket, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save(version=ticket.version + 1)
			Timeline.objects.create(ticket=ticket, action='Updated', user=request.user)
			return Response(serializer.data)
		return Response(serializer.errors, status=400)

	# Template Views
@method_decorator(login_required, name='dispatch')
class TicketsListView(View):
	def get(self, request):
		tickets = Ticket.objects.all().order_by('-created_at')
		for ticket in tickets:
			ticket.is_breached = ticket.is_breached()
		return render(request, 'tickets/tickets_list.html', {'tickets': tickets})

@method_decorator(login_required, name='dispatch')
class TicketCreateView(View):
	def get(self, request):
		return render(request, 'tickets/ticket_form.html')
	def post(self, request):
		title = request.POST.get('title')
		description = request.POST.get('description')
		sla_deadline = request.POST.get('sla_deadline')
		if title and description and sla_deadline:
			ticket = Ticket.objects.create(
				title=title,
				description=description,
				created_by=request.user,
				sla_deadline=sla_deadline
			)
			Timeline.objects.create(ticket=ticket, action='Created', user=request.user)
			return redirect(f'/tickets/{ticket.id}')
		return render(request, 'tickets/ticket_form.html', {'error': 'All fields required.'})

@method_decorator(login_required, name='dispatch')
class TicketDetailPageView(View):
	def get(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk)
		return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})
	def post(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk)
		content = request.POST.get('content')
		if content:
			Comment.objects.create(ticket=ticket, user=request.user, content=content)
			Timeline.objects.create(ticket=ticket, action='Commented', user=request.user)
		return redirect(f'/tickets/{ticket.id}')
class TicketCommentView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk)
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(ticket=ticket, user=request.user)
			Timeline.objects.create(ticket=ticket, action='Commented', user=request.user)
			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)

class BreachedTicketsView(generics.ListAPIView):
	serializer_class = TicketSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Ticket.objects.filter(sla_deadline__lt=timezone.now(), status__in=['open', 'assigned'])
