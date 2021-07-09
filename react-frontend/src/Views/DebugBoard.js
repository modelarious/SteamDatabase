import {
  UPCOMING_STATE,
  FINDING_NAME_ACTIVE_STATE,
  AWAITING_USER_STATE,
  QUEUED_FOR_INFO_RETRIEVAL_STATE,
  INFO_RETRIEVAL_ACTIVE_STATE,
  STORED
} from './../States.js';
import {
  ChakraProvider,
  Container,
  List,
  ListItem,
  Text,
  SimpleGrid
} from '@chakra-ui/react';
import CommandButton from '../Interactions/CommandButton';

class SocketInfo {
  constructor(state_constant, state_name, access_steam_name_instead) {
    this.state_constant = state_constant
    this.state_name = state_name
    this.access_steam_name_instead = access_steam_name_instead
  }

  get_name(state_data) {
    if (this.access_steam_name_instead) {
      return state_data.game_name_from_steam
    }
    return state_data.game_name_on_disk
    
  }
}

const socket_to_name = [
  new SocketInfo(UPCOMING_STATE, "Upcoming", false),
  new SocketInfo(FINDING_NAME_ACTIVE_STATE, "Finding Name Active", false),
  new SocketInfo(AWAITING_USER_STATE, "Awaiting User", false),
  new SocketInfo(QUEUED_FOR_INFO_RETRIEVAL_STATE, "Queued for Info Retrieval", true),
  new SocketInfo(INFO_RETRIEVAL_ACTIVE_STATE, "Info Retrieval Active", true),
  new SocketInfo(STORED, "Stored", true)
]


// expecting to receive:
/*
{
  commandSocket: A Socket that can be written to,
  stateData: {
    [STATE_CONSTANT] : [array of objects currently in this state],
    [STATE_CONSTANT_2] : [array of objects currently in this state],
    [STATE_CONSTANT_3] : [array of objects currently in this state],
    ...
  }
}
*/
function DebugBoard(props) {
  return <div>
    <ChakraProvider>
      <CommandButton commandSocket={props.commandSocket}/>
      <SimpleGrid columns={socket_to_name.length} spacingX={1} spacingY={1}> {
        socket_to_name.map(socket_info => (
          <Container>
          <Text>{socket_info.state_name}</Text>
          <br></br>
          <List>
            {props.stateData[socket_info.state_constant].map(state_data => (
              <ListItem>{socket_info.get_name(state_data)}</ListItem>
            ))}
          </List>
          </Container>
        ))
      }
      </SimpleGrid>
    </ChakraProvider>
  </div>
}

export default DebugBoard;