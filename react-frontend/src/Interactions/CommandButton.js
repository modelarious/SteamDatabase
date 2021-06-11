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

export default CommandButton;