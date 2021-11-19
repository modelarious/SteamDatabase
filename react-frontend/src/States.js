// socket is used for communicating which games are awaiting initial processing
const UPCOMING_STATE = '/upcoming';

// socket is used for communicating which games are having their nearest names found
const FINDING_NAME_ACTIVE_STATE = '/findingNameActive';

// socket is waiting for user to input which selection is correct
const AWAITING_USER_STATE = '/awaitingUser';

// awaiting an available process to start retrieving info
const QUEUED_FOR_INFO_RETRIEVAL_STATE = '/queuedForInfoRetrieval';

// info about game is currently being collected - scraping steam page, hitting steam API
const INFO_RETRIEVAL_ACTIVE_STATE = '/infoRetrievalActive';

// game has been persisted to database and will now show up on main screen
const STORED = '/stored';

const ERROR_STATE = '/error';

const stateToTitleMap = {
    [UPCOMING_STATE]: "Upcoming",
    [FINDING_NAME_ACTIVE_STATE]: "Finding Name",
    [AWAITING_USER_STATE]: "Awaiting User",
    [QUEUED_FOR_INFO_RETRIEVAL_STATE]: "Queued For Info Retrieval",
    [INFO_RETRIEVAL_ACTIVE_STATE]: "Info Retrieval Active",
    [STORED]: "Stored",
    [ERROR_STATE]: "Error"
}

const translate_state_to_title = function(stateName) {
    return stateToTitleMap[stateName];
}

// states:
//  - upcoming
//  - finding name (active)
//  - awaiting user input
//  - queued for info retrieval
//  - info retrieval (active)
//  - stored
const STATES = [
    UPCOMING_STATE,
    FINDING_NAME_ACTIVE_STATE,
    AWAITING_USER_STATE,
    QUEUED_FOR_INFO_RETRIEVAL_STATE,
    INFO_RETRIEVAL_ACTIVE_STATE,
    STORED,
    ERROR_STATE
];

module.exports = {
    STATES,
    UPCOMING_STATE,
    FINDING_NAME_ACTIVE_STATE,
    AWAITING_USER_STATE,
    QUEUED_FOR_INFO_RETRIEVAL_STATE,
    INFO_RETRIEVAL_ACTIVE_STATE,
    STORED,
    ERROR_STATE,
    translate_state_to_title
}