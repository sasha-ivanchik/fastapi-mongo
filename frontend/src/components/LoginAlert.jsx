import { useState } from 'react';
import Alert from 'react-bootstrap/Alert';

function LoginAlert({isOk}) {
    const [show, setShow] = useState(true);

    if (show) {
        if (isOk) {
            return (
                <Alert variant="success" onClose={() => setShow(false)} dismissible>
                    <p className="mb-0">
                        Hey, you are already logged in!
                    </p>
                </Alert>
            )

        } else {
            return (
                <Alert variant="danger" onClose={() => setShow(false)} dismissible>
                    <p className="mb-0">
                        Hey, you need to log in!
                    </p>
                </Alert>
            )
        }
    }
}

export default LoginAlert;