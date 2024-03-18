import React, {useEffect, useState} from 'react';
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {SelectableTable} from "./SelectableTable";
import {ankiApiLogin, dictGetAvailableLang, dictLookupWord, apiHealthStatus} from "../logic/ApiFetcher";
import {LanguageUUID} from "../model/LanguageUUID";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCloudBolt, FaCloudArrowUp} from "react-icons/fa6";
import {Language} from "../model/Language";
import Offcanvas from "react-bootstrap/Offcanvas";
import ListGroup from "react-bootstrap/ListGroup";
import Form from 'react-bootstrap/Form';
import AnkiSyncLogin from "./AnkiSyncLogin";
import {AuthService} from "../logic/AuthService";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {EmptyPage} from "./EmptyPage";
import {ApiHealthInformation} from "../model/ApiHealthInformation";
import {UserInput} from "./UserInput";


export function DictMask() {

    const [availLang, setAvailLang] = useState<Language[]>([])
    const [dictOptions, setDictOptions] = useState<DictOptionsItem[]>([])
    const [showAnkiLogin, setShowAnkiLogin] = useState(false);
    const [apiHealth, setApiHealth] = useState<ApiHealthInformation>(ApiHealthInformation.createInvalidStatus)

    const authProvider: AuthService = new AuthService();


    useEffect(() => {
        apiHealthStatus().then((healthStatus: ApiHealthInformation): void => {
                setApiHealth(healthStatus)

                if (!healthStatus.dbConnection) {
                    console.error('db connection down: ', healthStatus)
                } else {
                    dictGetAvailableLang().then(setAvailLang)
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

    const handleAnkiLogin = (userEmail: string, ankiResponse: AnkiLoginResponseHeaders): void => {
        console.log('update auth provider with email: ', userEmail)
        authProvider.loadAnkiLoginResponse(userEmail, ankiResponse)
    }

return (
    <div>
        <Container fluid="md">
            <div className="custom-max-width">

                {apiHealth.wotdApiConnection
                    && <UserInput authProvider={authProvider}
                                  setDictOptions={setDictOptions}
                                  availLang={availLang}
                                  handleShowAnkiLogin={handleShowAnkiLogin}/>}

                <div className='mt-2'>
                    {dictOptions !== undefined && dictOptions.length > 0
                        ? <SelectableTable
                            apiResponse={dictOptions}
                            userIsLoggedIn={authProvider.userIsLoggedIn()}/>
                        : <EmptyPage/>
                    }
                </div>

            </div>
        </Container>


        <Offcanvas show={showAnkiLogin} onHide={handleCloseAnkiLogin} className="w-100">
            <AnkiSyncLogin
                handleAnkiLogin={handleAnkiLogin}
                handleClose={handleCloseAnkiLogin}
                authProvider={authProvider}
            />
        </Offcanvas>

    </div>
);
}
