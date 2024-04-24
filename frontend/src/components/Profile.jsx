import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import {
    USERNAME_FIELD,
    EMAIL_FIELD,
    ROLE_FIELD,
    ACCESS_TOKEN_FIELD,
    } from './Constants.jsx'

import {
    fetchToken
    } from './Auth.jsx'


export default function Profile () {
    const navigate = useNavigate();
    const signOut = () => {
        localStorage.removeItem(ACCESS_TOKEN_FIELD);
        navigate("/")
    }

    return (
    <>
        <Card>
            <Card.Body>
                <Card.Title>Profile : {fetchToken(USERNAME_FIELD)} </Card.Title>
                <hr />
                <Card.Text>
                    email: {fetchToken(EMAIL_FIELD)}
                </Card.Text>
                <Card.Text>
                    role: {fetchToken(ROLE_FIELD)}
                </Card.Text>
                <Button variant="outline-primary" onClick={signOut}>Log out</Button>
            </Card.Body>
        </Card>
    </>
    );
}