import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import {Button} from "react-bootstrap";
import {AuthService} from "../logic/AuthService";


// interface InformationAlertProps {
//     showInfoAlert: boolean
//     handleCloseInfoAlert: () => void
// }
//
// export function InformationAlert(props: Readonly<InformationAlertProps>) {
//
//     const handleOnSelect = (e: any) => {
//         props.authProvider.ignoreLoginPrompt = e.target.checked
//         props.authProvider.writeIgnoreLoginPromptCookie()
//         props.handleCloseAnkiStatusAlert()
//     }
//
//     const openLoginDialog = () => {
//         props.handleCloseAnkiStatusAlert()
//         props.handleShowAnkiLogin()
//     }
//
//     return (
//         <Modal show={props.showAnkiStatusAlert} onHide={props.handleCloseAnkiStatusAlert}>
//             <Modal.Header closeButton>
//                 <Modal.Title>Log into Anki account</Modal.Title>
//             </Modal.Header>
//             <Modal.Body>
//                 <p>In order for the cards to synchronize with your Anki account please login with
//                     the following button or click on the cloud in the top right corner of the main
//                     view.</p>
//
//                 <Form.Check
//                     type='checkbox'
//                     id='ignore-alert-checkbox'
//                     label="don't show this message again"
//                     onSelect={handleOnSelect}
//                     onChange={handleOnSelect}
//                 />
//
//             </Modal.Body>
//             <Modal.Footer>
//                 <Button variant="secondary" onClick={openLoginDialog}>
//                     Anki login
//                 </Button>
//                 <Button variant="primary" onClick={props.handleCloseAnkiStatusAlert}>
//                     Ask me later
//                 </Button>
//             </Modal.Footer>
//         </Modal>
//
//     );
// }
//
// export default LoginAlert
