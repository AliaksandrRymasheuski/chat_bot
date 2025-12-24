DATABASE_SCHEMA = """
Database Schema Information:
###
Table: attendees
- attendee_id (INTEGER, PRIMARY KEY): Unique attendee identifier
- name (TEXT, NOT NULL): attendee's username
- email (TEXT, NOT NULL): attendee's email address

Contains information about attendees of events

Example of data:
[
	{
		"attendee_id": 100,
		"name": "Alice Johnson",
		"email": "alice.johnson@example.com"
	}
]

###
Table: events
- event_id (INTEGER, PRIMARY KEY): Unique event identifier
- event_name (TEXT, NOT NULL): Name of the event
- event_date (DATE, NOT NULL): Date of the event
- location (TEXT, NOT NULL): Location of the event
- max_attendees (INTEGER, NOT NULL): Maximum number of attendees for this event

Contains information about events.

Example of data:
[
	{
		"event_id": 1,
		"event_name": "Company Marathon",
		"event_date": "2023-11-15",
		"location": "Central Park",
		"max_attendees": 100
	}
]

###
Table: event_rsvp
- rsvp_id (INTEGER, PRIMARY KEY): Unique identifier of the rsvp
- event_id (INTEGER, NOT NULL, FOREIGN KEY -> events.event_id): Event identifier
- attendee_id (INTEGER, NOT NULL, FOREIGN KEY -> attendees.attendee_id): Attendee identifier
- status (TEXT, NOT NULL, CHECK(status IN ('yes', 'no', 'maybe')): Response status of the attendee for the event

Contains requests confirmation from attendees for event invitations.

Sample of data:
[
	{
		"rsvp_id": 2000,
		"event_id": 1,
		"attendee_id": 100,
		"status": "yes"
	}
]

------------
Relationships:
- event_rsvp.event_id references events.event_id (one event can have many answers from users (RSVP))
- event_rsvp.attendee_id references attendees.attendee_id (one attendee can have many answers for different events)

Important Notes:
- Database is SQLite
- Always use proper JOIN clauses when querying related tables
- Be careful with aggregations and use appropriate GROUP BY clauses
- Use LIMIT clause to prevent returning too many rows (max 100 rows recommended)
- All timestamps are in UTC
"""

def get_schema_context():
    """Returns the database schema information for LLM context."""
    return DATABASE_SCHEMA