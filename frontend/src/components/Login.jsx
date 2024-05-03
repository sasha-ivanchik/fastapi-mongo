import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import {
    setToken,
    fetchToken
    } from './Auth.jsx'
import {
    ACCESS_TOKEN_FIELD,
    REFRESH_TOKEN_FIELD,
    LOGIN_URL,
    SIGNUP_URL,
    } from './Constants.jsx'
import LoginAlert from './LoginAlert.jsx'
import SignupForm from './SignupModalForm.jsx'


export default function Login () {

    const frontHeaders = {  'Content-Type': 'application/x-www-form-urlencoded',
                            'accept': 'application/json'}

    const navigate = useNavigate();
    const [signupModalShow, setSignupModalShow] = React.useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSignup = ({signupUsername, signupPassword, signupEmail}) => {
        const form = new FormData();
        form.append('username', signupUsername)
        form.append('password', signupPassword)
        form.append('email', signupEmail)

        if (fetchToken(ACCESS_TOKEN_FIELD)) {
            localStorage.clear();
        };
        axios.post(
            `${SIGNUP_URL}`,
            form,
            { headers: frontHeaders}
        )
        .then(function (response) {
            if(response.data.hasOwnProperty("access_token")){
                setToken(
                    {"token": response.data.access_token,
                    "tokenType": ACCESS_TOKEN_FIELD,
                    "isToken": true}
                );

                setToken(
                    {"token": response.data.refresh_token,
                    "tokenType": REFRESH_TOKEN_FIELD,
                    "isToken": true},
                );
                navigate("/profile");
            }
            else{
                alert("INVALID DATA. RETRY.")
            }
        })
        .catch(function (error) {
            console.log(error);
        });

    }

    const handleLogin = () => {
        if(username.length === 0){
            alert("NO USERNAME")
        }
        else if(password.length === 0){
            alert("NO PASSWORD")
        }
        else{
            if (fetchToken(ACCESS_TOKEN_FIELD)) {
                localStorage.clear();
            };
            const form = new FormData();
            form.append('username', username)
            form.append('password', password)

            axios.post(
                LOGIN_URL,
                form,
                { headers: frontHeaders }
            )
            .then(function (response) {
                if(response.data.hasOwnProperty("access_token")){
                    setToken(
                        {"token": response.data.access_token,
                        "tokenType": ACCESS_TOKEN_FIELD,
                        "isToken": true}
                    )
                    setToken(
                        {"token": response.data.refresh_token,
                        "tokenType": REFRESH_TOKEN_FIELD,
                        "isToken": true},
                    )
                    navigate("/items");
                }
                else{
                    alert("INVALID USERNAME OR PASSWORD")
                }
            })
            .catch(function (error) {
                console.log(error);
                alert("BAD REQUEST");
            });
        }
    }

    return (
    <Card>
        <Card.Body>
            <Form>
                {
                    fetchToken(ACCESS_TOKEN_FIELD)
                    ? (
                        <LoginAlert isOk={true} />
                    )
                    : (
                        <LoginAlert isOk={false} />
                    )
                }
                <Form.Group className="mb-3" controlId="formUsername">
                    <Form.Label>Your username</Form.Label>
                    <Form.Control
                        size="sm"
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={ (e) => setUsername(e.target.value) }
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formPassword">
                    <Form.Label>Your password</Form.Label>
                    <Form.Control
                        size="sm"
                        type="password"
                        value={password}
                        placeholder="Enter password"
                        onChange={ (e) => setPassword(e.target.value) }
                    />
                </Form.Group>

                <Button
                    variant="outline-primary"
                    type="submit"
                    className="me-3"
                    onClick={ (e) => { e.preventDefault(); handleLogin() } }
                >
                    Log in
                </Button>

                <Button
                    variant="outline-danger"
                    onClick={() => setSignupModalShow(true)}
                >
                    + Create an account
                </Button>
                <SignupForm
                    show={signupModalShow}
                    onHide={() => setSignupModalShow(false)}
                    onSignup={handleSignup}
                />
            </Form>
        </Card.Body>
    </Card>
    );
}