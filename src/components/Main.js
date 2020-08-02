/* Written By:	  Euntae Ki
 * Functionality: Main page of Amazon Carry. Has a button that will cue the Raspberry Pi Camera to detect an object (Human).
		  Once the person is detected, it will prompt the user to the next page (/debug).
 */

// React + React-Boostrap
import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

// Import for Main Page
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';
import './Main.css';

class Main extends Component {
	constructor(props) {
		super(props);
	};
    render() {
        return (
            <div className="Main-Container">
                <div>
                    <h1 className="Welcome-Header">Amazon Carry</h1>
                </div>
                <div>
                    <Link to="/debug">
                        <Button id="Detect-Button" onMouseDown={ () => this.props.updateDetectCue() }>Detect</Button>
                    </Link>
                </div>
		<div>
			<h1>{this.props.detected}</h1>
		</div>
            </div>
        );
    }
}

export default Main;
