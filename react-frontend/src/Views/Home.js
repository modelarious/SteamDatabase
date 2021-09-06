import React, { Component } from 'react';
import { Links } from './Links';
const autoBind = require('auto-bind');

export class Home extends Component {
  constructor(props) {
    super();
    this.state = {
      games: props.games,
    };
    this.updateScrollDistanceMethod = props.updateScrollDistanceMethod;
    this.currentScrollTop = props.currentScrollTop;
    autoBind(this);
  }

  // need to be able to update this component's state based on a parent update. This is called before render.
  UNSAFE_componentWillReceiveProps(nextProps) {
    this.setState({ 
      games: nextProps.games 
    });
  }

  componentDidMount() {
    window.scrollTo(0, this.currentScrollTop);
    window.addEventListener('scroll', this.listenToScroll);
  }

  componentWillUnmount() {
    window.removeEventListener('scroll', this.listenToScroll);
  }

  listenToScroll = () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    this.updateScrollDistanceMethod(winScroll);
  };

  render() {
    return <Links games={this.state.games} />;
  }
}
