# socket is used for communicating which games are awaiting initial processing
UPCOMING_STATE = '/upcoming'

# socket is used for communicating which games are having their nearest names found
FINDING_NAME_ACTIVE_STATE = '/findingNameActive'

# socket is waiting for user to input which selection is correct
AWAITING_USER_STATE = '/awaitingUser'

# awaiting an available process to start retrieving info
QUEUED_FOR_INFO_RETRIEVAL_STATE = '/queuedForInfoRetrieval'

# info about game is currently being collected - scraping steam page, hitting steam API
INFO_RETRIEVAL_ACTIVE_STATE = '/infoRetrievalActive'

# game has been persisted to database and will now show up on main screen
STORED = '/stored'

ERROR_STATE = '/error'

# states:
#  - upcoming
#  - finding name (active)
#  - awaiting user input
#  - queued for info retrieval
#  - info retrieval (active)
#  - stored
STATES = set([
    UPCOMING_STATE,
    FINDING_NAME_ACTIVE_STATE,
    AWAITING_USER_STATE,
    QUEUED_FOR_INFO_RETRIEVAL_STATE,
    INFO_RETRIEVAL_ACTIVE_STATE,
    STORED,
    ERROR_STATE
])

# anything of StateStrType means that it is a member of STATES
StateStrType = str