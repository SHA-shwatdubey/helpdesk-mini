# HelpDesk Mini

A Django-based ticketing system with SLA timers, assignments, threaded comments, searchable timeline, and role-based access.

## Features
- Ticket creation, assignment, and status tracking
- SLA timers and breach detection
- Threaded comments and timeline logging
- Role-based access: user, agent, admin
- Optimistic locking for updates
- Search and pagination

## Endpoints
- `/tickets` — List and search tickets
- `/tickets/new` — Create a new ticket
- `/tickets/:id` — View and update ticket details

## API
- `POST /api/tickets`
- `GET /api/tickets?...&limit=&offset=`
- `GET /api/tickets/:id`
- `PATCH /api/tickets/:id`
- `POST /api/tickets/:id/comments`

## Setup
1. Install dependencies: `pip install django`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`

## Folder Structure
- `helpdesk_mini/` — Project settings
- `tickets/` — Main app for ticketing

## Next Steps
- Implement models for Ticket, Comment, Timeline, and Role
- Build API views and serializers
- Add templates and frontend pages
- Ensure all constraints and judge checks are met
