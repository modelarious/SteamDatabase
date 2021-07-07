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

const socket_to_name = [
  {
    state: UPCOMING_STATE, 
    name: "Upcoming"
  },
  {
    state: FINDING_NAME_ACTIVE_STATE, 
    name: "Finding Name Active"
  },
  {
    state: AWAITING_USER_STATE, 
    name: "Awaiting User"
  },
  {
    state: QUEUED_FOR_INFO_RETRIEVAL_STATE, 
    name: "Queued for Info Retrieval"
  },
  {
    state: INFO_RETRIEVAL_ACTIVE_STATE, 
    name: "Info Retrieval Active"
  },
  {
    state: STORED, 
    name: "Stored"
  }
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
        socket_to_name.map(socket_to_name_data => (
          <Container>
          <Text>{socket_to_name_data.name}</Text>
          <br></br>
          <List>
            {props.stateData[socket_to_name_data.state].map(state_data => (
              <ListItem>{state_data.game_name_on_disk}</ListItem>
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