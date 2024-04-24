import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Link, BrowserRouter, Routes, Route, NavLink } from "react-router-dom";

import Login from './Login.jsx'
import Profile from './Profile.jsx'
import {RequireToken} from './Auth.jsx'


function SimpleNav() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary card">
      <Container className>
        <Navbar.Brand href="#home">Purple python machine</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link className="btn btn-primary" as={Link} to="/">Login</Nav.Link>
            <Nav.Link className="btn btn-primary" as={Link} to="profile">Profile</Nav.Link>
            <Nav.Link className="btn btn-primary" as={Link} to="items">Cards</Nav.Link>
            <NavDropdown title="Dropdown" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">
                Separated link
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default SimpleNav;