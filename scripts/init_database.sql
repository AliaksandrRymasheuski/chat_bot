-- Create Events Table
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_date DATE NOT NULL,
    location TEXT NOT NULL,
    max_attendees INTEGER NOT NULL
);

-- Create Attendees Table
CREATE TABLE attendees (
    attendee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create Event RSVP Table
CREATE TABLE event_rsvp (
    rsvp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    attendee_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('yes', 'no', 'maybe')) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (attendee_id) REFERENCES attendees(attendee_id)
);


INSERT INTO events (event_name, event_date, location, max_attendees) VALUES
    ('Company Marathon', '2023-11-15', 'Central Park', 100),
    ('Annual Tech Conference', '2023-12-01', 'Downtown Convention Center', 500),
    ('Holiday Party', '2024-12-20', 'Office HQ', 200),
    ('Team Building Event', '2025-11-18', 'Mountain Resort', 50),
    ('All-Hands meeting', '2025-12-24', 'Teams (Online)', 1000),
    ('Product Launch', '2025-12-25', 'Online Webinar', 300);


INSERT INTO attendees (name, email) VALUES
    ('Alice Johnson', 'alice.johnson@example.com'),
    ('Bob Smith', 'bob.smith@example.com'),
    ('Charlie Brown', 'charlie.brown@example.com'),
    ('Diana Prince', 'diana.prince@example.com'),
    ('Ethan Hunt', 'ethan.hunt@example.com'),
    ('Fiona Davis', 'fiona.davis@example.com'),
    ('George Miller', 'george.miller@example.com'),
    ('Hannah Moore', 'hannah.moore@example.com');

INSERT INTO event_rsvp (event_id, attendee_id, status) VALUES
    -- RSVPs for Company Marathon
    (1, 1, 'yes'),
    (1, 2, 'yes'),
    (1, 3, 'maybe'),
    (1, 4, 'no'),

    -- RSVPs for Annual Tech Conference
    (2, 2, 'yes'),
    (2, 3, 'yes'),
    (2, 5, 'yes'),
    (2, 6, 'maybe'),
    (2, 7, 'no'),

    -- RSVPs for Holiday Party
    (3, 1, 'yes'),
    (3, 4, 'yes'),
    (3, 8, 'yes'),
    (3, 3, 'maybe'),

    -- RSVPs for Team Building Event
    (4, 2, 'yes'),
    (4, 6, 'yes'),
    (4, 7, 'maybe'),

    -- RSVPs for Product Launch
    (5, 1, 'yes'),
    (5, 3, 'yes'),
    (5, 5, 'yes'),
    (5, 8, 'no');