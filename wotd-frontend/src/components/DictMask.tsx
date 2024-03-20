import React, {useEffect, useState} from 'react';
import Container from "react-bootstrap/Container";
import {SelectableTable} from "./SelectableTable";
import {apiHealthStatus, dictGetAvailableLang} from "../logic/ApiFetcher";
import {Button} from "react-bootstrap";
import {Language} from "../model/Language";
import Offcanvas from "react-bootstrap/Offcanvas";
import Form from 'react-bootstrap/Form';
import AnkiSyncLogin from "./AnkiSyncLogin";
import {AuthService} from "../logic/AuthService";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {EmptyPage} from "./EmptyPage";
import {ApiHealthInformation} from "../model/ApiHealthInformation";
import {UserInput} from "./UserInput";
import Modal from 'react-bootstrap/Modal';
import LoginAlert from "./LoginAlert";
import {BasicUsage} from "./BasicUsage";


export function DictMask() {

    const [availLang, setAvailLang] = useState<Language[]>([])
    const [dictOptions, setDictOptions] = useState<DictOptionsItem[]>([])
    const [showAnkiLogin, setShowAnkiLogin] = useState(false);
    const [showAnkiStatusAlert, setShowAnkiStatusAlert] = useState(false);
    const [apiHealth, setApiHealth] = useState<ApiHealthInformation>(ApiHealthInformation.createInvalidStatus)

    const authProvider: AuthService = new AuthService();


    useEffect(() => {
        apiHealthStatus().then((healthStatus: ApiHealthInformation): void => {
                setApiHealth(healthStatus)

                if (!healthStatus.dbConnection) {
                    console.error('db connection down: ', healthStatus)
                } else {
                    dictGetAvailableLang().then(setAvailLang)

                    if (authProvider.showLoginPrompt()) {
                        handleShowAnkiStatusAlert()
                    }
                }

                if (!healthStatus.wotdApiConnection) {
                    console.error('wotd api not available: ', healthStatus)
                    alert('Backend API not available - not possible to lookup words. Please try again later.')
                } else if (!healthStatus.ankiApiConnection) {
                    console.error('anki api not available: ', healthStatus)
                    alert('Anki API not available - you can lookup words but cannot synchronize them with your anki web account.')
                }

            }
        )
    }, []);

    const handleCloseAnkiLogin = () => setShowAnkiLogin(false)
    const handleShowAnkiLogin = () => setShowAnkiLogin(true)

    const handleCloseAnkiStatusAlert = () => setShowAnkiStatusAlert(false)
    const handleShowAnkiStatusAlert = () => setShowAnkiStatusAlert(true)


    const handleAnkiLogin = (userEmail: string, ankiResponse: AnkiLoginResponseHeaders): void => {
        console.log('update auth provider with email: ', userEmail)
        authProvider.loadAnkiLoginResponse(userEmail, ankiResponse)
    }

    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width">

                    <LoginAlert
                        showAnkiStatusAlert={showAnkiStatusAlert}
                        handleCloseAnkiStatusAlert={handleCloseAnkiStatusAlert}
                        handleShowAnkiLogin={handleShowAnkiLogin}
                        authProvider={authProvider}
                    />

                    {apiHealth.wotdApiConnection
                        && <UserInput authProvider={authProvider}
                                      setDictOptions={setDictOptions}
                                      availLang={availLang}
                                      handleShowAnkiLogin={handleShowAnkiLogin}/>}

                    {/*<div className='mt-2'>*/}
                    <div className='mt-2'>
                        {/*<div className='debugborder'>test</div>*/}
                        {dictOptions !== undefined && dictOptions.length > 0
                            ? <SelectableTable
                                apiResponse={dictOptions}
                                userIsLoggedIn={authProvider.userIsLoggedIn()}/>
                            : <BasicUsage/>}
                            {/*// : <EmptyPage/>*/}
                    </div>

                </div>
            </Container>


            <Offcanvas show={showAnkiLogin} onHide={handleCloseAnkiLogin} className="w-100">
                <AnkiSyncLogin
                    handleAnkiLogin={handleAnkiLogin}
                    handleClose={handleCloseAnkiLogin}
                    authProvider={authProvider}
                />
                {/*<EmptyPage/>*/}
            </Offcanvas>

        </div>
    );
}
