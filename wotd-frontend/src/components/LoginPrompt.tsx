import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import {Button} from "react-bootstrap";


interface LoginPromptProps {
    showAnkiStatusAlert: boolean
    handleCloseAnkiStatusAlert: () => void
}

export function LoginPrompt(props: Readonly<LoginPromptProps>) {

    return (
        <Modal show={props.showAnkiStatusAlert} onHide={props.handleCloseAnkiStatusAlert}>
            <Modal.Header closeButton>
                <Modal.Title>Log into Anki account</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>In order for the cards to synchronize with your Anki account please login with
                    the following button or click on the cloud in the top right corner of the main
                    view.</p>

                <Form.Check
                    type='checkbox'
                    id='ignore-alert-checkbox'
                    label="don't show this message again"
                />

            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.handleCloseAnkiStatusAlert}>
                    Anki login
                </Button>
                <Button variant="primary" onClick={props.handleCloseAnkiStatusAlert}>
                    Ask me later
                </Button>
            </Modal.Footer>
        </Modal>

    );
}

export default LoginPrompt
