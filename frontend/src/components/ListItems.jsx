import { useState, useEffect} from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

import {
    ACCESS_TOKEN_FIELD,
    TODOS_URL
    } from './Constants.jsx'
import {
    setToken,
    fetchToken
    } from './Auth.jsx'
import SimpleCard from './Item.jsx'
import ModalCreateForm from './CreateModalForm.jsx'


function ListItems () {
    const [todos, setTodos] = useState([])
    const [modalShow, setModalShow] = useState(false);

    const frontHeaders = {  'Content-Type': 'application/json',
                            'accept': 'application/json',
                            'token': fetchToken(ACCESS_TOKEN_FIELD) }

    function getListItems () {
        axios.get(
            TODOS_URL,
            { headers: frontHeaders}
        )
        .then(function (response) {
            if(response.data.status === "success"){
                setTodos(response.data.data)
                console.log(response.data)
            }
            else{
                console.log(response.data)
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        })
    }

    function handleDeleteItem (title) {
        axios.delete(
            `${TODOS_URL}/${title}`,
            { headers: frontHeaders}
        )
        .then(function (response) {
            getListItems()
        })
        .catch(function (error) {
            console.log(error);
        })
    }

    function handleUpdateItem ({title, description, additionalInfo, isPublic, isDone}) {
        const updatingData = {
                'description': description,
                'additional_info': additionalInfo,
                'public': isPublic,
                'is_done': isDone,
            }

        axios.patch(
            `${TODOS_URL}/${title}`,
            updatingData,
            { headers: frontHeaders}
        )
        .then(function (response) {
            getListItems();
        })
        .catch(function (error) {
            console.log(error);
        });
    }


    function handleCreateItem ({title, description, additionalInfo, isPublic, isDone}) {
        const creatingData = {
                'title': title,
                'description': description,
                'additional_info': additionalInfo,
                'public': isPublic,
                'is_done': isDone,
        }

        axios.post(
            `${TODOS_URL}`,
            creatingData,
            { headers: frontHeaders}
        )
        .then(function (response) {
            getListItems();
        })
        .catch(function (error) {
            console.log(error);
        });
    }


    function handleSwapDoneItem (title, isDone) {
        const payload = {
            "is_done":  !isDone,
            "additional_info": null,
        }

        axios.patch(
            `${TODOS_URL}/${title}`,
            payload,
            { headers: frontHeaders}
        )
        .then(function (response) {
            getListItems()
        })
        .catch(function (error) {
            console.log(error);
        })
    }


    useEffect( () => {
        getListItems();
    }, [])

    if (!todos) {
        return(
            <>
                <div className="d-flex flex-column">
                    <Button
                        variant="outline-primary"
                        onClick={() => setModalShow(true)}
                        className="mb-3"
                    >
                        + Create TODO
                    </Button>
                    <ModalCreateForm
                        show={modalShow}
                        onHide={() => setModalShow(false)}
                        onCreate={ handleCreateItem }
                    />
                    <Card>
                        <Card.Body>
                            <Card.Title>No data</Card.Title>
                        </Card.Body>
                    </Card>
                </div>
            </>
        )
    }
    else {
        const items = todos.map((todo) =>
            <SimpleCard
                key={todo.title}
                todo={todo}
                onDelete={handleDeleteItem}
                onDoneSwap={handleSwapDoneItem}
                onUpdate={handleUpdateItem}
            />
        )
        return(
            <>
                <div className="d-flex flex-column">
                    <Button
                        variant="outline-primary"
                        onClick={() => setModalShow(true)}
                        className="mb-3 align-items-center"
                    >
                        + Create TODO
                    </Button>
                    <ModalCreateForm
                        show={modalShow}
                        onHide={() => setModalShow(false)}
                        onCreate={ handleCreateItem }
                    />
                    {items}
                </div>
            </>
        )
    }

}

export default ListItems;