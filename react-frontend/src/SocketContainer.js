import { w3cwebsocket as W3CWebSocket } from "websocket";
const { STATES } = require("./States.js");

const { SocketLinkBuilder } = require('./SocketLinkBuilder.js');
const autoBind = require('auto-bind');


export default class SocketContainer {
  constructor(endpoints) {
    const create_link = new SocketLinkBuilder().create_link;
  
    this.sockets = Object.fromEntries( 
      endpoints.map( name => [name, W3CWebSocket(create_link(name))]) 
    );

    autoBind(this);
  }
}