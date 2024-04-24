import { Navigate, useLocation } from 'react-router-dom';

import {
    getUser
    } from './GetData.jsx'

import {
    ACCESS_TOKEN_FIELD,
    REFRESH_TOKEN_FIELD,
    } from './Constants.jsx'


export const setToken = ({token, tokenType, isToken}) => {
    // put token in localStorage
    localStorage.setItem(tokenType, token)
    if (!isToken) {
        getUser(token)
    }

}

export const fetchToken = (tokenType) => {
    // fetch the token from localStorage
    return localStorage.getItem(tokenType)
}

export function RequireToken ({children}) {
    let auth = fetchToken(ACCESS_TOKEN_FIELD)
    let location = useLocation()

     if(!auth) {
        return <Navigate to="/" state={{ from: location }} />;
     }

     return children;
}