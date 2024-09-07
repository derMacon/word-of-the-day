import Offcanvas from "react-bootstrap/Offcanvas";
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import React, {useEffect, useState} from "react";
import Alert from 'react-bootstrap/Alert';
import Spinner from 'react-bootstrap/Spinner';

import 'bootstrap/dist/css/bootstrap.min.css'
import {ankiApiIsHealthy, ankiApiLogin} from "../logic/ApiFetcher";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {AuthService} from "../logic/AuthService";


interface AnkiSyncLoginProps {
    handleAnkiLogin: (ankiResponse: AnkiLoginResponseHeaders) => void
    handleClose: () => void
    authProvider: AuthService
}

export function AnkiSyncLogin(props: Readonly<AnkiSyncLoginProps>) {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [healthyApi, setHealthyApi] = useState(true);
    const [showSpinner, setShowSpinner] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result: boolean = await ankiApiIsHealthy();
                setHealthyApi(result);
            } catch (error) {
                console.error('Error fetching data:', error);
                setHealthyApi(false);
            }
        };

        fetchData();
    }, []);


    const handleEmailChange = (e: any): void => {
        setEmail(e.target.value)
    }

    const handlePasswordChange = (e: any): void => {
        setPassword(e.target.value)
    }

    const handleKeyDown = (e: any): void => {
        if (e.code === 'Enter' || e.which === 13) {
            handleLogin()
        }
    }


    const handleLogin = () => {
        console.log('anki sync login email: ', email)
        setShowSpinner(true)
        ankiApiLogin(email, password).then((response: AnkiLoginResponseHeaders | undefined) => {
            console.log('anki response: ', response)
            setShowSpinner(false)

            if (response == undefined) {
                setEmail('')
                setPassword('')
                alert('Credentials incorrect, please try again.')
            } else {
                props.handleAnkiLogin(response)
                props.handleClose()
            }

        })
    }

    const ankiApiDownReport: React.JSX.Element =
        <Alert variant="danger">
            <Alert.Heading>Anki API not reachable</Alert.Heading>
            <p>
                Check the API container status on the worker node. Refresh the page once it has restarted.
            </p>
        </Alert>

    const spinner: React.JSX.Element =
        <Spinner
            as="span"
            animation="grow"
            size="sm"
            role="status"
            aria-hidden="true"
        />

    const loggedInStatus: React.JSX.Element =
        <Alert variant="success">
            <Alert.Heading>Anki Web Login</Alert.Heading>
            <p>
                You are currently logged into your anki web account under <b>{email}</b>.
            </p>
            <hr/>
            <div className="d-flex">
                <Button onClick={() => props.authProvider.cleanCookies()} variant="outline-success">
                    Logout
                </Button>
            </div>
        </Alert>

    const loginForm: React.JSX.Element =
        <>
            <p>You are currently not logged into your anki account.
                In order to sync the dictionary searches with anki web please log in.</p>

            <p>If you do net have an account, please register <a
                href="https://ankiweb.net/account/signup">here</a> and
                come back afterwards.</p>
            <br/>

            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={handleEmailChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="password"
                        aria-describedby="passwordHelpBlock"
                        value={password}
                        onChange={handlePasswordChange}
                        onKeyDown={handleKeyDown}
                    />
                    <Form.Text id="passwordHelpBlock" muted>
                        Your credentials will not be stored by this application.
                        After the initial login the api works with the token retrieved from anki web.
                    </Form.Text>
                </Form.Group>
            </Form>

            <Button onClick={handleLogin} variant="light">
                {showSpinner ? spinner : 'Login'}
            </Button>


            {/*<p>Word Vaults</p>*/}
            {/*<ListGroup>*/}
            {/*    <ListGroup.Item>English Dictionary</ListGroup.Item>*/}
            {/*    <ListGroup.Item disabled>German Duden Definitions</ListGroup.Item>*/}
            {/*</ListGroup>*/}
        </>

    return (
        <Container fluid="md">
            <div className="custom-max-width">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Anki Sync</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    {healthyApi
                        ? (props.authProvider.userIsLoggedIn() ? loggedInStatus : loginForm)
                        : ankiApiDownReport
                    }
                </Offcanvas.Body>
            </div>
        </Container>
    );
}

export default AnkiSyncLogin;
