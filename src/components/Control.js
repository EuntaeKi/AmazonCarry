// React Library
import React, { Component } from 'react';

// Bootstrap Components
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';

import './Control.css';

class Control extends Component {
    // Instantiate all the states and bind all the functions
    constructor(props) {
        super(props);
        this.state = { 
            edit: false, 
            controlDistance: this.props.customDistance,
            remoteControlButton: 0,
            displayError: false,
            errors: {
                distance: ''
            }
        };
        this.timer = null;
        this.handleEditClick = this.handleEditClick.bind(this);
        this.handleControlClick = this.handleControlClick.bind(this);
        this.whileMouseDown = this.whileMouseDown.bind(this);
        this.onMouseRelease = this.onMouseRelease.bind(this);
    }

    /*  Distance Related Button Functions for Customizing Distance
     *  Case apply: Validate the form. If the input is not between 1 and 6
     *              then render error-related display. If it is between 1 and 6,
     *              update the state in App.js & change the conditional rendering state
     *  Case Cancel: Change the conditional rendering state
     *  Case Edit: Change the conditional rendering state & get rid of the error-related display
     */
    handleEditClick(e) {
        switch (e.currentTarget.value) {
            case "apply": 
                if ((this.state.controlDistance < 7 && this.state.controlDistance > 0)) {
                    this.props.updateCustomDistance(this.state.controlDistance);
                    this.setState({ edit: false });
                } else {
                    this.setState({displayError: true});
                    this.setState(prevState => {
                        let errors = Object.assign({}, prevState.errors);
                        errors.distance = "The value must be between 1 and 6.";
                        return { errors };
                    });
                }
                break;

            case "cancel": 
                this.setState({ edit: false });
                break;

            case "edit": 
                this.setState({ edit: true, displayError: false });
                break;

            default: 
                console.log("Edit Error: No value attached to the element");
                break;
        }
    }

    // Control Related Button Functions for Manually Controlling the Device
    handleControlClick(value) {
        switch (value) {
            case "top":
                this.setState({remoteControlButton: 'w'}, () => {this.props.updateControl(this.state.remoteControlButton)});
                this.props.sendControlData();
                break;
            case "bottom":
                this.setState({remoteControlButton: 's'}, () => {this.props.updateControl(this.state.remoteControlButton)});
                this.props.sendControlData();
                break;
            case "left":
                this.setState({remoteControlButton: 'a'}, () => {this.props.updateControl(this.state.remoteControlButton)});
                this.props.sendControlData();
                break;
            case "right":
                this.setState({remoteControlButton: 'd'}, () => {this.props.updateControl(this.state.remoteControlButton)});
                this.props.sendControlData();
                break;
            default:
                console.log("Error: Control Button does not have a value");
                break;
        }
    }

    /*  A function to repeat a handleControlClick() function with an old value from the event.
     *  Because the event that gets passed in is a synthetic event, the event object will disappear after it gets passed in.
     *  Hence, hold it as a temporary variable and pass it into the handleControlClick function. 
     */
    whileMouseDown(event) {
        event.persist();
        let temp = event.currentTarget.value;
        this.timer = setInterval(() => this.handleControlClick(temp), 250);
    }

    //  A function to clear the timer and update the global state to be 'b' (brake) on onMouseUp event.
    onMouseRelease() {
        clearInterval(this.timer);
        this.setState({remoteControlButton: 'b'}, () => { this.props.updateControl(this.state.remoteControlButton); });
    }

    render() {
        const isEditing = this.state.edit;
        let distanceRow;

        // Logic for Conditional Render
        if (isEditing) {
            distanceRow = 
            <Row id="control-setting-offset">
                <Form>
                    <Form.Group>
                        <Form.Label>Distance from the host</Form.Label>
                        <Form.Control className={ this.state.displayError ? "control-form-error control-setting-form" : "control-setting-form" } 
                        type="input" placeholder={"Maximum distance is 6 ft"} onChange={ (e) => {this.setState({ controlDistance: e.target.value })} } />
                        { <span style={{color: "#EE1515", fontSize: 0.8 + "rem"}}> { this.state.displayError ? this.state.errors.distance : "" } </span> }
                    </Form.Group>
                </Form>
                <Button className="control-setting-button" id="control-apply" value="apply" onClick={ e => this.handleEditClick(e) }>Apply</Button>
                <Button className="control-setting-button" id="control-cancel" value="cancel" onClick={ e => this.handleEditClick(e) }>Cancel</Button>
            </Row>;
        } else {
            distanceRow =
            <Row id="control-setting-text-offset">
                <div id="control-setting-background">
                    <span id="control-setting-text">Distance from the host: { this.props.customDistance } ft</span>
                    <Button id="control-edit-button" value="edit" onClick={ e => this.handleEditClick(e) }>
                        <div className="material-icons md-48" data-value="test">edit</div>
                    </Button>
                </div>
            </Row>
        }

        // Rendering Elements
        return (
            <React.Fragment>
                <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"></link>
                <div id="control-container">
                    <Row id="control-top-row-offset">
                        <Button className="control-button" id="top-button" value="top" onMouseDown={ e => this.whileMouseDown(e) } onMouseUp={ this.onMouseRelease }>
                            <i className="material-icons custom-size" id="control-icon-top">play_arrow</i>
                        </Button>
                        <ToggleButtonGroup type="checkbox">
                            <ToggleButton id={ this.props.manual ? "control-toggle-on" : "control-toggle-off" } onMouseDown={ () => this.props.updateManual() }>
			    { this.props.manual ? "Disable Manual Control" : "Enable Manual Control" } </ToggleButton>
                        </ToggleButtonGroup>
                    </Row>
                    <Row>
                        <Button className="control-button" id="left-button" value="left" onMouseDown={ e => this.whileMouseDown(e) } onMouseUp={ this.onMouseRelease }>
                            <i className="material-icons custom-size" id="control-icon-left">play_arrow</i>
                        </Button>
                        <Button className="control-button" id="right-button" value="right" onMouseDown={ e => this.whileMouseDown(e) } onMouseUp={ this.onMouseRelease }>
                            <i className="material-icons custom-size">play_arrow</i>
                        </Button>
                    </Row>
                    <Button className="control-button" id="bottom-button" value="bottom" onMouseDown={ e => this.whileMouseDown(e) } onMouseUp={ this.onMouseRelease }>
                        <i className="material-icons custom-size" id="control-icon-bottom">play_arrow</i>
                    </Button>
                    { distanceRow }
                </div>
                
            </React.Fragment>
        );
    }
}

export default Control;
