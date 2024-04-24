import { useState, useEffect} from 'react';


import {
    ACCESS_TOKEN_FIELD,
    REFRESH_TOKEN_FIELD,
    ME_URL,
    } from './Constants.jsx'
import {
    setToken,
    fetchToken
    } from './Auth.jsx'


export function getUser (frontToken) {
    const frontHeaders = {  'Content-Type': 'application/x-www-form-urlencoded',
                            'accept': 'application/json',
                            'token': frontToken }

    axios.get(
        ME_URL,
        { headers: frontHeaders}
    )
    .then(function (response) {
        if(response.data.hasOwnProperty("username")){
            setToken(
                {"token": response.data.username,
                "tokenType": USERNAME_FIELD,
                "isToken": false}
            )
            setToken(
                {"token": response.data.email,
                "tokenType": EMAIL_FIELD,
                "isToken": false}
            )
            setToken(
                {"token": response.data.role,
                "tokenType": ROLE_FIELD,
                "isToken": false}
            )
        }
        else{
            alert("INVALID TOKEN. LOGIN AND RETRY")
        }
    })
    .catch(function (error) {
        console.log(error);
    })
}

export function fetchUserData () {
    const username = localStorage.getItem(USERNAME_FIELD)
    const email = localStorage.getItem(EMAIL_FIELD)
    const role = localStorage.getItem(ROLE_FIELD)

    return {
        "username": username,
        "email": email,
        "role": role
    }
}

