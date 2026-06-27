ROLE_SCOPES = {
    "student": [
        "resume:read",
        "resume:write",
        "interview:create"
    ],
    "teacher": [
        "resume:read",
        "interview:read"
    ],
    "admin": [
        "resume:read",
        "resume:write",
        "interview:create",
        "interview:delete",
        "admin"
    ]
}