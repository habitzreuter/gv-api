"""
GV API
Task schema
"""

SCHEMA = {
    "title": "Create Task",
    "type": "object",
    "description": "Schema used to validade incoming task requests",
    "properties": {
        "number": {
            "type": ["integer", "null"],
            "minimum": 0,
        },
        "title": {
            "type": ["string", "null"]
        },
        "status": {
            "type": ["string", "null"]
        },
        "group": {
            "type": ["string", "null"]
        },
        "score": {
            "type": ["integer", "null"],
            "minimum": 0,
        },
        "max_score": {
            "type": ["integer", "null"],
            "minimum": 0,
        },
        "extra_info": {
            "type": ["string", "null"]
        },
        "assigned_to": {
            "type": ["string", "null"]
        },
        "url": {
            "type": ["string", "null"],
            "format": "uri",
        },
        "due_date": {
            "type": ["string", "null"],
            "format": "date-time",
        },
        "location": {
            "type": ["string", "null"]
        },
    },
}