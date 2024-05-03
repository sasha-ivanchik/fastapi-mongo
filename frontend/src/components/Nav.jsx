import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Link, BrowserRouter, Routes, Route, NavLink } from "react-router-dom";


function SimpleNav() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary card" >
      <Container className>
        <Navbar.Brand href="#home">Purple python machine</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link className="btn btn-primary" as={Link} to="/">Login</Nav.Link>
            <Nav.Link
                    className="btn btn-primary"
                    as={Link}
                    to='/profile'
                >
                    Profile
            </Nav.Link>
            <Nav.Link className="btn btn-primary" as={Link} to="items">Cards</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default SimpleNav;