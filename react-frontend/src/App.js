import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import {
  STATES, 
  UPCOMING_STATE,
  FINDING_NAME_ACTIVE_STATE,
  AWAITING_USER_STATE,
  QUEUED_FOR_INFO_RETRIEVAL_STATE,
  INFO_RETRIEVAL_ACTIVE_STATE,
  STORED
} from './States.js';
import {
  ChakraProvider,
  Container,
  List,
  ListItem,
  Text,
  SimpleGrid
} from '@chakra-ui/react';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';

const autoBind = require('auto-bind');

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES) {
      this.state[state] = [];
    }
    autoBind(this);
  }
  
  componentDidMount() {
    const endpoints = STATES.concat([
      "/command",
    ]);

    const socketContainer = new SocketContainer(endpoints);
    const sockets = Object.entries(socketContainer.get_sockets())
    for (const [state, sock] of sockets) {
      sock.onmessage = (message) => {
        const receivedMessage = JSON.parse(message.data);
        this.setState({
          [state]: receivedMessage
        });
      };

      sock.onopen = () => {
        console.log(`${state} open`);
      };
      sock.onclose = () => {
        console.log(`${state} close`);
      }
    }
  }
  
  render() {
    var debugBoardNeededStateData = {}
    for (const stateName of STATES) {
      debugBoardNeededStateData[stateName] = this.state[stateName];
    }

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1">Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3" default>Debug</TabLink>
      
        <TabContent for="tab1"> "games view"</TabContent>
        <TabContent for="tab2">"user input view"</TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData}/>
        </TabContent>
      </Tabs>
    );
  }
}




// XXX improve this by generalizing how data is stored in the objects in each of the queues
// XXX to make sure that something like gameNameOnDisk is present in every object
function DebugBoard(props) {
  return <div>
  <ChakraProvider>
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

export default App;
