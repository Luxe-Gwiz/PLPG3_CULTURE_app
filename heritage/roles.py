HEAD_OF_CULTURE = "Head of Culture"
CULTURE_CHIEF = "Culture Chief"
LOCAL_MEMBER = "Local Member"

ROLES = [HEAD_OF_CULTURE, CULTURE_CHIEF, LOCAL_MEMBER]

CREATE = "create"
READ = "read"
UPDATE = "update"
DELETE = "delete"

ROLE_PERMISSIONS = {
    HEAD_OF_CULTURE: [CREATE, READ, UPDATE, DELETE],
    CULTURE_CHIEF: [CREATE, READ, UPDATE],
    LOCAL_MEMBER: [CREATE, READ],
}


def has_permission(role, permission):
    return permission in ROLE_PERMISSIONS[role]
