import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function RefreshModal(props) {
    return (
    <Modal
        show={props.show}
        onHide={props.onHide}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
    >
        <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
                Updating your access data
            </Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <p>
                We will endeavor to update your access details.
                If the update fails, you will need to log in again.
            </p>
        </Modal.Body>
        <Modal.Footer>
            <Button onClick={props.onHide}>Close</Button>
        </Modal.Footer>
    </Modal>
    );
}

export default RefreshModal;