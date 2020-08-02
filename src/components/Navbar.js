/* Written By:	  Euntae Ki
 * Functionality: Allows the user to move between pages through a tab in the navigation bar.
 */

// Imports for React + React-Boostrap
import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

// Imports for design components
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { NavLink } from 'react-router-dom';
import logo from '../logo.svg';
import './Navbar.css'

class NavBar extends Component {
    render() {
        return (
            <Navbar bg="light" expand="lg">
                <Navbar.Brand as={ NavLink } to="/"><img src={logo} alt="Amazon Carry" width="150px" /></Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link as={ NavLink } to="/debug" className="nav-link" activeClassName="is-active">Debugging Console</Nav.Link>
                        <Nav.Link as={ NavLink } to="/control" className="nav-link" activeClassName="is-active">Manual Control</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default NavBar;
