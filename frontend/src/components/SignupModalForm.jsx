import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';


function SignupForm(props) {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    function handleSignupSubmit () {
        if (username.length === 0){
            alert("`USERNAME` REQUIRED")
        }
        else if (username.length < 3) {
            alert("`USER NAME` MUST CONTAIN A MINIMUM OF 3 CHARACTERS.")
        }
        else if (password.length === 0) {
            alert("`PASSWORD` REQUIRED")
        }
        else if (email.length === 0) {
            alert("`EMAIL` REQUIRED")
        }
        else{
            props.onSignup({
                "signupUsername": username,
                "signupPassword": password,
                "signupEmail": email,
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
                    Crate a new account
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                        <Form.Group className="mb-3" controlId="formUsername">
                            <Form.Label>Username</Form.Label>
                            <Form.Control
                                size="sm"
                                type="text"
                                placeholder="Enter your username"
                                value={username}
                                onChange={ (e) => setUsername(e.target.value) }
                            />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                size="sm"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={ (e) => setPassword(e.target.value) }
                            />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formEmail">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                size="sm"
                                type="email"
                                placeholder="Enter your email"
                                value={email}
                                onChange={ (e) => setEmail(e.target.value) }
                            />
                        </Form.Group>

                        <Button
                            variant="primary"
                            type="submit"
                            className="me-3"
                            onClick={ (e) => { e.preventDefault(); handleSignupSubmit(); props.onHide() ;} }
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

export default SignupForm;