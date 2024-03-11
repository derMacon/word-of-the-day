import Offcanvas from "react-bootstrap/Offcanvas";
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import React, {useState} from "react";

import 'bootstrap/dist/css/bootstrap.min.css'


interface AnkiSyncLoginProps {
    handleAnkiLogin: (email: string, password: string) => void
}

export function AnkiSyncLogin(props: Readonly<AnkiSyncLoginProps>) {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e: any): void => {
        setEmail(e.target.value)
    }

    const handlePasswordChange = (e: any): void => {
        setPassword(e.target.value)
    }

    const handleAnkiLogin = () => {
        console.log('anki sync login email: ', email)
        props.handleAnkiLogin(email, password)
    }

    return (
        <Container fluid="md">
            <div className="custom-max-width">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Anki Sync</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>

                    <p>You are currently not logged into your anki account.
                        In order to sync the dictionary searches with anki web please log in.</p>

                    <p>If you do net have an account, please register <a href="https://ankiweb.net/account/signup">here</a> and
                        come back afterwards.</p>
                    <br/>

                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control
                                type="email"
                                placeholder="name@example.com"
                                onChange={handleEmailChange}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="password"
                                aria-describedby="passwordHelpBlock"
                                onChange={handlePasswordChange}
                            />
                            <Form.Text id="passwordHelpBlock" muted>
                                Your credentials will not be stored by this application.
                                After the initial login the api works with the token retrieved from anki web.
                            </Form.Text>
                        </Form.Group>
                    </Form>

                    <Button onClick={handleAnkiLogin} variant="light">Login</Button>


                    {/*<p>Word Vaults</p>*/}
                    {/*<ListGroup>*/}
                    {/*    <ListGroup.Item>English Dictionary</ListGroup.Item>*/}
                    {/*    <ListGroup.Item disabled>German Duden Definitions</ListGroup.Item>*/}
                    {/*</ListGroup>*/}

                </Offcanvas.Body>
            </div>
        </Container>
    );
}

export default AnkiSyncLogin;
