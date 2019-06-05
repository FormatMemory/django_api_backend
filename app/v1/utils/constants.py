ERROR = 'Error'
SUCCESS = 'Success'

# Permissions
PERMISSION_ADMINISTRATOR_REQUIRED = 'Administrator permissions needed'
PERMISSION_MODERATOR_REQUIRED = 'Moderator permissions needed'

# User roles
USER_ROLE_ADMINISTRATOR = 'administrator'
USER_ROLE_MODERATOR = 'moderator'

# Votes
VOTE_UP = 1
VOTE_DOWN = -1
VOTE_VALUE_CHOICES = (
    (VOTE_UP, 'Up'),
    (VOTE_DOWN, 'Down')
)

# status
STATUS_ACTIVE = 'active'
STATUS_BANNED = 'banned'
STATUS_INACTIVE = 'inactive'
STATUS_AUDITED = 'audited'
STATUS_EXPIRE = 'expire'

USER_STATUS_CHOICES = (
    (STATUS_ACTIVE, 'active'),
    (STATUS_BANNED, 'banned'),
    (STATUS_INACTIVE, 'inactive'),
)

POST_STATUS_CHOICES = (
   (STATUS_ACTIVE, 'active'),
    (STATUS_BANNED, 'banned'),
    (STATUS_INACTIVE, 'inactive'),
    (STATUS_AUDITED, 'audited'),
    (STATUS_EXPIRE, 'expire'),
)


# View
USER_VIEW_CHOICES = (
    (1, 1),
)

# nickname Exist
USER_OR_NICKNAME_EXIST = "User or username exists"

# library status
LIBRARY_STATUS_PUBLIC = 'public'
LIBRARY_STATUS_PRIVATE = 'private'

# Report status
REPORT_STATUS_ACTIVE = 'active'
REPORT_STATUS_OK = 'ok'
REPORT_STATUS_INVALID = 'invalid'