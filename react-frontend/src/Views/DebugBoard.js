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
import React, { Component } from 'react';


const autoBind = require('auto-bind');
class CommandButton extends Component {
  constructor(props) {
    super();
    this.commandSocket = props.commandSocket;
    autoBind(this);
  }
  
  send_command() {
    const command = {
      'command_name' : 'start game match',
      'path_on_disk' : '/path/on/disk'
    }

    this.commandSocket.send(JSON.stringify(command))
  }
  
  render() {
    if (this.commandSocket) {
      return <button onClick={this.send_command}>Start game matching</button>
    }
    return <div/>
  }
}

// XXX improve this by generalizing how data is stored in the objects in each of the queues
// XXX to make sure that something like gameNameOnDisk is present in every object
function DebugBoard(props) {
  return <div>
    <ChakraProvider>
      <CommandButton commandSocket={props.commandSocket}/>
      <SimpleGrid columns={6} spacingX={1} spacingY={1}>
        <Container>
          <Text>Upcoming</Text>
          <br></br>
          <List>
            {props.stateData[UPCOMING_STATE].map(title => (
              <ListItem border="1px solid red" style={{display: 'flex',  borderRadius: '25px', justifyContent:'center', alignItems:'center'}}>{title}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Finding Name Active</Text>
          <br></br>
          <List>
            {props.stateData[FINDING_NAME_ACTIVE_STATE].map(title => (
              <ListItem>{title}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Awaiting User</Text>
          <br></br>
          <List>
            {props.stateData[AWAITING_USER_STATE].map(ob => (
              <ListItem>{ob.gameName}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Queued for Info Retrieval</Text>
          <br></br>
          <List>
            {props.stateData[QUEUED_FOR_INFO_RETRIEVAL_STATE].map(ob => (
              <ListItem>{ob.gameNameFromSteam}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Info Retrieval Active</Text>
          <br></br>
          <List>
            {props.stateData[INFO_RETRIEVAL_ACTIVE_STATE].map(ob => (
              <ListItem>{ob.gameNameFromSteam}</ListItem>
            ))}
          </List>
        </Container>
        
        <Container>
          <Text>Stored</Text>
          <br></br>
          <List>
            {props.stateData[STORED].map(ob => (
              <ListItem>{ob.name_on_steam}</ListItem>
            ))}
          </List>
        </Container>
      </SimpleGrid>
    </ChakraProvider>
  </div>
}

export default DebugBoard;