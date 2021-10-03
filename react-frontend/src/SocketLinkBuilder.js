const autoBind = require('auto-bind');

export class SocketLinkBuilder {
	constructor() {
		const backendServerIP = "127.0.0.1"
		const backendServerPort = 3091;
		this.socketLinkStart = `ws://${backendServerIP}:${backendServerPort}`;
  
		autoBind(this);
	}
	create_link(endpoint) {
		return `${this.socketLinkStart}${endpoint}`
	}
  }