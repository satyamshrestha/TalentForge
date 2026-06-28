ROLE_SCOPES = {
    "student": [
        "resume:read",
        "resume:write",
        "interview:create",
        "interview:read",
        "answer:create",
        "dashboard:read"
    ],
    "teacher": [
        "resume:read",
        "interview:read",
        "answer:create",
        "dashboard:read"
    ],
    "admin": [
        "resume:read",
        "resume:write",
        "interview:create",
        "interview:read",
        "interview:delete",
        "dashboard:read",
        "answer:create",
        "admin"
    ]
}