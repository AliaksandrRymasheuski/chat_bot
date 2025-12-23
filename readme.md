1. Create and initialize DB:

`sqlite3 my_database.db < init_database.sql`

2. Run the app:

`streamlit run main.py`

Sample queries in DB:
- Which events are happening next week?

`SELECT event_name, event_date, location
FROM events
WHERE event_date BETWEEN DATE('now') AND DATE('now', '+7 days');`

- How many people have RSVP’d for the marathon event?

`SELECT COUNT(1) AS total_rsvp
FROM event_rsvp er
INNER JOIN events e ON er.event_id = e.event_id
WHERE e.event_name = 'Company Marathon' AND er.status = 'yes';`

- What is the schedule for tomorrow?

`SELECT event_name, event_date, location
FROM events
WHERE event_date = DATE('now', '+1 day');`