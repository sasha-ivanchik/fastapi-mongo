import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';

function ModalUpdateForm(props) {

    const [description, setDescription] = useState(props.currentTodo.description);
    const [additionalInfo, setAdditionalInfo] = useState(props.currentTodo.additional_info);
    const [isPublic, setIsPublic] = useState(props.currentTodo.public);
    const [isDone, setIsDone] = useState(props.currentTodo.is_done);

    function handleUpdateSubmit () {
        if(
            description == props.currentTodo.description
            && additionalInfo == props.currentTodo.additional_info
            && isPublic == props.currentTodo.public
            && isDone == props.currentTodo.is_done
        ){
            alert("THERE ARE NO CHANGES")
        }
        else{
            props.onUpdate({
                "title": props.currentTodo.title,
                "description": description,
                "additionalInfo": additionalInfo,
                "isPublic": isPublic,
                "isDone": isDone,
            })
        }
    }

    return (
        <Modal
          show={props.show}
          onHide={props.onHide}
          size="md"
          aria-labelledby="contained-modal-title-vcenter"
          centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Update TODO
                </Modal.Title>

            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="formDescription">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            size="sm"
                            type="text"
                            placeholder={props.currentTodo.description}
                            value={description}
                            onChange={ (e) => setDescription(e.target.value) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formAdditionalInfo">
                        <Form.Label>Additional information</Form.Label>
                        <Form.Control
                            size="sm"
                            as="textarea"
                            rows={3}
                            value={ additionalInfo }
                            placeholder={props.currentTodo.additional_info ? props.currentTodo.additional_info : "Add new description"}
                            onChange={ (e) => setAdditionalInfo(e.target.value) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formPublic">
                        <Form.Check
                            type="checkbox"
                            label="Public"
                            defaultChecked={props.currentTodo.public}
                            onChange={ (e) => setIsPublic(e.target.checked) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formDone">
                        <Form.Check
                            type="checkbox"
                            label="Done"
                            defaultChecked={props.currentTodo.is_done}
                            onChange={ (e) => setIsDone(e.target.checked) }
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="submit"
                        className="me-3"
                        onClick={ (e) => { e.preventDefault(); handleUpdateSubmit(); props.onHide() ;} }
                    >
                        Save
                    </Button>

                    <Button onClick={ props.onHide }>
                        Close
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}

export default ModalUpdateForm;