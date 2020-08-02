/* Written By:	  Euntae Ki
 * Functionality: Synthesizes all the components and export it to index.js.
 * 		  Restrict links, global state manager, and WebSocket contact point
 */

// Import Relevant Libraries for React
import React, { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom'

// Import Children Components
import Main from './components/Main';
import Navbar from './components/Navbar';
import Debug from './components/Debug';
import Control from './components/Control';

// WebSocket URL
// Change the URL to match the IP Address of React server
const URL = 'ws://192.168.4.87:3301'

class App extends Component {
  constructor() {
    super();
    this.state = {
      distance: 2,
      control: 'b',
      customDistance: 2,
      detected: false,
      manual: false,
      detectCue: false
    };
  }

  ws = new WebSocket(URL);

  // Attach WS Connector/Reciever
  componentDidMount () {
    this.ws.onopen = () => {
      console.log('connected');
    }

    this.ws.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      this.setState({ distance: message["distance"], detected: message["camera"], detectCue: message["detectCue"] });
	console.log(this.state.detected);
    }
    this.ws.onclose = () => {
      console.log('disconnected');
      this.setState({
        ws: new WebSocket(URL)
      });
    }
  }

  // Update the distance state and send it to the WS server
  updateCustomDistance(newDistance) {
    this.setState({ customDistance: newDistance }, () => { 
      this.ws.send(JSON.stringify(
        {
          type: "customDistance",
          data: this.state.customDistance
        }
      )) 
    });
  }

  // Update manual state & send it to the WS Server
  updateManual() {
    this.setState({ manual: !(this.state.manual) }, () => {
	this.ws.send(JSON.stringify({
          type: "manual",
          data: this.state.manual
          })) 
	});
  }

  // Updates the control state
  updateControl(remoteControl) {
    this.setState({ control: remoteControl });
  }

	// Updates the detectCue state
	updateDetectCue() {
		this.setState({ detectCue: true }, () => {
			this.ws.send(JSON.stringify({
		  		type: "detectCue",
		  		data: this.state.detectCue
		  	}));
		});
	}
  
  // Send control to WS server
  // Note: We could have combined sendControlData() function with updateControl() function
  //       But because onMouseRelease() function uses updateControl() function,
  //       implementing this with updateControl() function is not suitable
  sendControlData() {
    if (this.state.manual) {
      this.ws.send(JSON.stringify(
        {
          type: "control",
          data: this.state.control
        }
      ));
    }
  }

  // Render pages
  render() {
    return (
      <React.Fragment>
        <Switch>
          <Route exact path="/">
            <Main updateDetectCue={ () => { this.updateDetectCue() } } detected={ this.state.detected } />
          </Route>
          <Route exact path="/debug" render={props => (
            this.state.detected ? 
            <React.Fragment>
              <Navbar /> 
              <Debug detected={ this.state.detected } manual={ this.state.manual } distance={ this.state.distance } />
            </React.Fragment> : <Redirect to='/'/>
          )}>            
          </Route>
          <Route exact path="/control" render={props => (
            this.state.detected ? 
            <React.Fragment>
              <Navbar /> 
              <Control 
                control={ this.state.control } customDistance={ this.state.customDistance } manual={ this.state.manual } 
                sendControlData={ () => { this.sendControlData() } }
                updateControl={ (remoteControl) => { this.updateControl(remoteControl) } }
                updateCustomDistance={ (newDistance) => { this.updateCustomDistance(newDistance) } }
                updateManual={ () => { this.updateManual() } } 
              />
            </React.Fragment> : <Redirect to='/'/>
          )}>
          </Route>
        </Switch>
      </React.Fragment>
    );
  }
}

export default App;
