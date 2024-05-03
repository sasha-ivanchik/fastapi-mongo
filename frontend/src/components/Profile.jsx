import { useNavigate, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import axios from 'axios';

import {
    ACCESS_TOKEN_FIELD,
    REFRESH_TOKEN_FIELD,
    REFRESH_URL,
    ME_URL,
    } from './Constants.jsx';

import { setToken, fetchToken } from './Auth.jsx';
import RefreshModal from './RefreshModal.jsx';


export default function Profile () {

    const navigate = useNavigate();
    const signOut = () => {
        localStorage.clear();
        navigate("/")
    }

    const [modalShow, setModalShow] = useState(false);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = fetchToken(ACCESS_TOKEN_FIELD);

                if (token) {
                    const frontHeaders = {  'Content-Type': 'application/x-www-form-urlencoded',
                            'accept': 'application/json',
                            'token': token }

                    axios.get(
                        ME_URL,
                        { headers: frontHeaders}
                    )
                    .then(function (response) {
                        if(response.data.hasOwnProperty("username")){
                            const username = response.data.username;
                            const email = response.data.email;
                            const role = response.data.role;

                            const result_odj = {
                                "username": username,
                                "email": email,
                                "role": role,
                            };
                            setUserData(result_odj);
                        }
                        else{
                            alert("INVALID RESPONSE. LOGIN AND RETRY")
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                }
            } catch (error) {
                console.error('Error:', error);
            }
        };
        fetchUserData();
    }, []);

    const handRefresh = () => {
        const refreshToken = fetchToken(REFRESH_TOKEN_FIELD)

        const frontHeaders = {  'Content-Type': 'application/x-www-form-urlencoded',
                                'accept': 'application/json',
                                'refresh-token': refreshToken }

        axios.get(
            REFRESH_URL,
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
                console.log("successful tokens update")
            }
            else{
                console.log("INVALID REFRESH TOKEN")
            }
        })
        .catch(function (error) {
            console.log(error);
            alert("BAD REQUEST FOR REFRESHING");
        });

    }

    return (
    <>
        <Card>
            <Card.Body>
                <Card.Title>Profile : {userData.username} </Card.Title>
                <hr />
                <Card.Text>
                    email: {userData.email}
                </Card.Text>
                <Card.Text>
                    role: {userData.role}
                </Card.Text>
                <Button className="me-3" variant="outline-primary" onClick={signOut}>Log out</Button>

                <Button
                    variant="outline-primary"
                    onClick={(e) => { e.preventDefault(); handRefresh(); setModalShow(true)} }
                >
                    Update access data
                </Button>

                <RefreshModal
                    show={modalShow}
                    onHide={() => setModalShow(false)}
                />

            </Card.Body>
        </Card>
    </>
    );
}