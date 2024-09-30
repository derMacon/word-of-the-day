import React, {useEffect, useState} from 'react';
import Cookies from "universal-cookie";
import Container from "react-bootstrap/Container";
import {SelectableTable} from "./SelectableTable";
import {dictGetAvailableLang, wotdApiHealthStatus} from "../logic/ApiFetcher";
import {Language} from "../model/Language";
import Offcanvas from "react-bootstrap/Offcanvas";
import AnkiSyncLogin from "./AnkiSyncLogin";
import {AuthService} from "../logic/AuthService";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {InfoPage} from "./InfoPage";
import {ApiHealthInformation} from "../model/ApiHealthInformation";
import {UserInput} from "./UserInput";
import LoginAlert from "./LoginAlert";
import {BasicUsage} from "./BasicUsage";
import {ErrorPage} from "./ErrorPage";


const COOKIE_KEY_FIRST_TIME_USER: string = 'FIRST-TIME-USER'

export function DictMask() {

    const [availLang, setAvailLang] = useState<Language[]>([])
    const [dictOptions, setDictOptions] = useState<DictOptionsItem[]>([])
    const [showAnkiLogin, setShowAnkiLogin] = useState(false);
    const [showAnkiStatusAlert, setShowAnkiStatusAlert] = useState(false);
    const [showErrorPage, setShowErrorPage] = useState(false);
    const [showInfoPage, setShowInfoPage] = useState(false);
    const [apiHealth, setApiHealth] = useState<ApiHealthInformation>(ApiHealthInformation.createInvalidStatus)

    const authProvider: AuthService = new AuthService();
    const cookies: Cookies = new Cookies(null, {path: '/'})

    const debugWrapper = (e: any) => {
        console.log('debug wrapper: ', e)
        setAvailLang(e)
    }


    useEffect(() => {
        wotdApiHealthStatus().then((healthStatus: ApiHealthInformation): void => {
                setApiHealth(healthStatus)

                if (!healthStatus.dbConnection) {
                    console.error('db connection down: ', healthStatus)
                } else {
                    console.log('before setting avail lang')
                    dictGetAvailableLang().then(debugWrapper)
                    // dictGetAvailableLang().then(setAvailLang)
                    console.log('after setting avail lang: ', availLang)

                    if (authProvider.showLoginPrompt()) {
                        handleShowAnkiStatusAlert()
                    }
                }

                if (!healthStatus.wotdApiConnection) {
                    console.error('wotd api not available: ', healthStatus)
                    // alert('Backend API not available - not possible to lookup words. Please try again later.')
                    setShowErrorPage(true)
                } else if (!healthStatus.ankiApiConnection) {
                    console.error('anki api not available: ', healthStatus)
                }

                const isFirstTimeUser: Boolean = cookies.get(COOKIE_KEY_FIRST_TIME_USER)
                if (isFirstTimeUser === undefined || isFirstTimeUser) {
                    cookies.set(COOKIE_KEY_FIRST_TIME_USER, false)
                    setShowInfoPage(true)
                }

            }
        )
    }, []);

    const handleCloseAnkiLogin = () => setShowAnkiLogin(false)
    const handleShowAnkiLogin = () => setShowAnkiLogin(true)

    const handleCloseInfoPage = () => setShowInfoPage(false)
    const handleShowInfoPage = () => setShowInfoPage(true)


    const handleCloseAnkiStatusAlert = () => setShowAnkiStatusAlert(false)
    const handleShowAnkiStatusAlert = () => setShowAnkiStatusAlert(true)


    const handleAnkiLogin = (ankiResponse: AnkiLoginResponseHeaders): void => {
        console.log('update auth provider with signed email: ', ankiResponse.signedUsername)
        authProvider.loadAnkiLoginResponse(ankiResponse)
    }

    console.log('avail langs during dict mask render: ', availLang)

    const mainPage = <>
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
                          handleShowInfoPage={handleShowInfoPage}
                          handleShowAnkiLogin={handleShowAnkiLogin}/>}

        <div className='mt-2'>
            {dictOptions !== undefined && dictOptions.length > 0
                ? <SelectableTable
                    apiResponse={dictOptions}
                    userIsLoggedIn={authProvider.userIsLoggedIn()}/>
                : <BasicUsage/>}
        </div>
    </>

    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width">

                    {showErrorPage ? <ErrorPage/> : mainPage}

                </div>
            </Container>


            <Offcanvas show={showAnkiLogin} onHide={handleCloseAnkiLogin} className="w-100">
                <AnkiSyncLogin
                    handleAnkiLogin={handleAnkiLogin}
                    handleClose={handleCloseAnkiLogin}
                    authProvider={authProvider}
                />
            </Offcanvas>

            <Offcanvas show={showInfoPage} onHide={handleCloseInfoPage} className="w-100">
                <InfoPage/>
            </Offcanvas>

        </div>
    );
}
