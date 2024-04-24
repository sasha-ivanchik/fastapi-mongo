import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';

function PopupCreateForm(props) {

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [additionalInfo, setAdditionalInfo] = useState('');
    const [isPublic, setIsPublic] = useState(true);
    const [isDone, setIsDone] = useState(false);

    function handleCreateSubmit () {
        if(
            description.length === 0
            && additionalInfo.length === 0
        ){
            alert("`TITLE` AND `DESCRIPTION` ARE REQUIRED")
        }
        else{
            props.onCreate({
                "title": title,
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
                    Create TODO
                </Modal.Title>

            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="formTitle">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            size="sm"
                            type="text"
                            placeholder="Enter todo's title"
                            value={title}
                            onChange={ (e) => setTitle(e.target.value) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formDescription">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            size="sm"
                            type="text"
                            placeholder="Enter todo's description"
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
                            placeholder="Enter todo's additional information"
                            onChange={ (e) => setAdditionalInfo(e.target.value) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formPublic">
                        <Form.Check
                            type="checkbox"
                            label="Public"
                            defaultChecked={true}
                            onChange={ (e) => setIsPublic(e.target.checked) }
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formDone">
                        <Form.Check
                            type="checkbox"
                            label="Done"
                            defaultChecked={false}
                            onChange={ (e) => setIsDone(e.target.checked) }
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="submit"
                        className="me-3"
                        onClick={ (e) => { e.preventDefault(); handleCreateSubmit(); props.onHide() ;} }
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

export default PopupCreateForm;