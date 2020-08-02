/* Written By:	  Euntae Ki
 * Functionality: Renders debugging console page. Will change the distance of the device in the page in real time.
		  Dsiplays date, connectivity, object detection status, and current distance in real time.
 */

// Imports for React + React-Boostrap
import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

// Imports for design components + Date
import { Row, Col } from 'react-bootstrap';
import './Debug.css';

var dateFormat = require('dateformat');

class Debug extends Component {
    constructor(props) {
        super(props);
        this.state = {
            date: Date.now()
        };
    }

    // Update the date state every 1000ms (1s)
    componentDidMount() {
        this.interval = setInterval(() => this.setState({ date: this.state.date + 1000 }), 1000);
    }

    // Reset the interval
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    // Rendering Component
    render() {
        return (
            <div id="debug-container">
                <Row>
                    <Col className="debug-col" xs={3} lg={3}>
                        <p className={ this.props.detected ? "host-host" : "host-disconnected" }>Host</p>
                        <p id="host-status">{ this.props.detected ? "Connected": "Disconnected" }</p>
                    </Col>
                    <Col className="manual-col" xs={{span: 3, offset: 5}} lg={{span: 3, offset: 5}}>
                        <p id="manual-text">Manual</p>
                        <p id="manual-status">{ this.props.manual ? "ON" : "OFF" }</p>
                    </Col>
                </Row>
                
                <Row id="time-distance-group">
                    <Col className="debug-col" xs={2} lg={2}>
                        <p id="time-heading">Time</p>
                        <p id="time-time">{ dateFormat(this.state.date, "hh:MM:ss") }</p>
                        <p id="time-string">{ dateFormat(this.state.date, "TT") }</p>
                    </Col>
                    <Col id="distance-group" xs={true} lg={true}>
                        <Row>
                            <div id="distance-host" />
                            <div className="distance-measure" id="distance-measure-left" />
                            <p id="distance-text">{ this.props.distance } ft</p>
                            <div className="distance-measure" id="distance-measure-right" style={{ width: this.props.distance * 5 + "vw" }} />
                            <div id="distance-device" />
                        </Row>
                        <Row>
                            <div id="distance-floor" />
                        </Row>
                    </Col>
                </Row>
            </div>
        );
    }
}

export default Debug;
