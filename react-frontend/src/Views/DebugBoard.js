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

// XXX now that all objects have game_name_on_disk, you can now improve this code by .map()'ing the Container objects
function DebugBoard(props) {
  return <div>
    <ChakraProvider>
      <CommandButton commandSocket={props.commandSocket}/>
      <SimpleGrid columns={6} spacingX={1} spacingY={1}>
        <Container>
          <Text>Upcoming</Text>
          <br></br>
          <List>
            {props.stateData[UPCOMING_STATE].map(ob => (
              <ListItem border="1px solid red" style={{display: 'flex',  borderRadius: '25px', justifyContent:'center', alignItems:'center'}}>{ob.game_name_on_disk}</ListItem>
            ))} 
          </List>
        </Container>
        
        <Container>
          <Text>Finding Name Active</Text>
          <br></br>
          <List>
            {props.stateData[FINDING_NAME_ACTIVE_STATE].map(ob => (
              <ListItem>{ob.game_name_on_disk}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Awaiting User</Text>
          <br></br>
          <List>
            {props.stateData[AWAITING_USER_STATE].map(ob => (
              <ListItem>{ob.game_name_on_disk}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Queued for Info Retrieval</Text>
          <br></br>
          <List>
            {props.stateData[QUEUED_FOR_INFO_RETRIEVAL_STATE].map(ob => (
              <ListItem>{ob.game_name_from_steam}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Info Retrieval Active</Text>
          <br></br>
          <List>
            {props.stateData[INFO_RETRIEVAL_ACTIVE_STATE].map(ob => (
              <ListItem>{ob.game_name_from_steam}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Stored</Text>
          <br></br>
          <List>
            {props.stateData[STORED].map(ob => (
              <ListItem>{ob.game_name_from_steam}</ListItem>
            ))}
          </List>
        </Container>
      </SimpleGrid>
    </ChakraProvider>
  </div>
}

export default DebugBoard;