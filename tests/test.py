from database.database import execute_query

query1 = """
SELECT event_name, event_date, location
FROM events
WHERE event_date BETWEEN DATE('now') AND DATE('now', '+7 days');
"""

query2 = """
SELECT COUNT(1) AS total_rsvp
FROM event_rsvp er
INNER JOIN events e ON er.event_id = e.event_id
WHERE e.event_name = 'Company Marathon' AND er.status = 'yes';
"""

query3 = """
SELECT event_name, event_date, location
FROM events
WHERE event_date = DATE('now', '+1 day');
"""

query4 = """
SELECT *
FROM attendees
"""

print(execute_query(query1))
print(execute_query(query2))
print(execute_query(query3))
print(execute_query(query4))