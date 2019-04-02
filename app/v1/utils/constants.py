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

# User status
USER_STATUS_ACTIVE = 'active'
USER_STATUS_BANNED = 'banned'
USER_STATUS_INACTIVE = 'inactive'

# Post status
POST_STATUS_ACTIVE = 'active'
POST_STATUS_BANNED = 'banned'
POST_STATUS_EXPIRE = 'expire'
POST_STATUS_AUDITED = 'audited'
