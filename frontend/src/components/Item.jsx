import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

import PopupUpdateForm from './UpdatePopupForm.jsx'


function SimpleCard({todo, onDelete, onDoneSwap, onUpdate}) {
    const [state, setState] = useState()
    const [modalShow, setModalShow] = useState(false);

    function isEmpty(obj) {
        for (const prop in obj) {
            if (Object.hasOwn(obj, prop)) {
              return false;
            }
        }
        return true;
    };

    function isString(x) {
        return Object.prototype.toString.call(x) === "[object String]"
    };

    function getAdditionalInfo(x) {
        if (!isEmpty(x) && !isString(x)) {
            return (
                <Card.Text as="span"  >
                    Additional info:
                    <ul>
                        {Object.keys(x).map((key)=>(
                            <li key={key} >{key} : {x[key]}</li>
                        ))}
                    </ul>
                </Card.Text>
            )
        } else if (!isEmpty(x) && isString(x)) {
            return (
                <Card.Text as="span"  >
                    Additional info: {x}
                </Card.Text>
            )
        } else return '';
    };

    return (
        <Card className="mb-3">
            <Card.Body>
                <Card.Title>{todo.title}</Card.Title>
                <hr />
                <Card.Text>{todo.description}</Card.Text>
                <Card.Text>Created at: {todo.created_at}</Card.Text>
                <Card.Text>Is done: {todo.is_done ? 'DONE' : 'NOT DONE'}</Card.Text>
                <Card.Text>Is public: {todo.public ? 'PUBLIC' : 'NOT PUBLIC'}</Card.Text>
                { getAdditionalInfo(todo.additional_info) }
                <div className="mt-3">
{/*                 ================================= BUTTON 1 =============================================== */}
                    <Button
                        className="me-3"
                        variant="outline-primary"
                        onClick={ (event) => onDoneSwap(todo.title, todo.is_done) }
                    >
                        {
                            todo.is_done
                            ? "Mark as NOT done"
                            : "Mark as done"
                        }
                    </Button>

{/*                 ================================= BUTTON 2 =============================================== */}
                    <Button
                        variant="outline-primary"
                        className="me-3"
                        onClick={() => setModalShow(true)}
                        disabled={ todo.is_done }
                    >
                        Update
                    </Button>

                    <PopupUpdateForm
                        show={modalShow}
                        onHide={() => setModalShow(false)}
                        currentTodo={todo}
                        onUpdate={onUpdate}
                    />

{/*                 ================================= BUTTON 3 =============================================== */}
                    <Button
                        variant="outline-danger"
                        onClick={ (event) => onDelete(todo.title) }
                    >
                        DELETE
                    </Button>
                </div>
            </Card.Body>
        </Card>
    );
}

export default SimpleCard;