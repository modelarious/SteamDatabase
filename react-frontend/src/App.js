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
} from '@chakra-ui/react'

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
    // XXX Improve this by generalizing the object sent through sockets so that the accesses
    // aren't all different (ex: title -> title, ob -> ob.gameName, ob -> ob.gameNameFromSteam)
    return (

    <div>
      <ChakraProvider resetCSS>
        <SimpleGrid columns={6} spacingX={1} spacingY={1}>
          <Container>
            <Text>Upcoming</Text>
            <br></br>
            <List>
              {this.state[UPCOMING_STATE].map(title => (
                <ListItem>{title}</ListItem>
              ))}
            </List>
          </Container>
          
          <Container>
            <Text>Finding Name Active</Text>
            <br></br>
            <List>
              {this.state[FINDING_NAME_ACTIVE_STATE].map(title => (
                <ListItem>{title}</ListItem>
              ))}
            </List>
          </Container>
          
          <Container>
            <Text>Awaiting User</Text>
            <br></br>
            <List>
              {this.state[AWAITING_USER_STATE].map(ob => (
                <ListItem>{ob.gameName}</ListItem>
              ))}
            </List>
          </Container>
          
          <Container>
            <Text>Queued for Info Retrieval</Text>
            <br></br>
            <List>
              {this.state[QUEUED_FOR_INFO_RETRIEVAL_STATE].map(ob => (
                <ListItem>{ob.gameNameFromSteam}</ListItem>
              ))}
            </List>
          </Container>
          
          <Container>
            <Text>Info Retrieval Active</Text>
            <br></br>
            <List>
              {this.state[INFO_RETRIEVAL_ACTIVE_STATE].map(ob => (
                <ListItem>{ob.gameNameFromSteam}</ListItem>
              ))}
            </List>
          </Container>
          
          <Container>
            <Text>Stored</Text>
            <br></br>
            <List>
              {this.state[STORED].map(ob => (
                <ListItem>{ob.name_on_steam}</ListItem>
              ))}
            </List>
          </Container>
          
        </SimpleGrid>
      </ChakraProvider>
    </div>
    );
  }
}

export default App;
