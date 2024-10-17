import React, {useEffect, useState} from 'react';
import Cookies from "universal-cookie";
import Container from "react-bootstrap/Container";
import {SelectableTable} from "./SelectableTable";
import {ankiApiUserLoggedIn, dictGetAvailableLang, wotdApiHealthStatus} from "../logic/ApiFetcher";
import {Language} from "../model/Language";
import Offcanvas from "react-bootstrap/Offcanvas";
import AnkiSyncLogin from "./AnkiSyncLogin";
import {CookieService} from "../logic/CookieService";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {InfoPage} from "./InfoPage";
import {ApiHealthInformation} from "../model/ApiHealthInformation";
import {UserInput} from "./UserInput";
import LoginAlert from "./LoginAlert";
import {BasicUsage} from "./BasicUsage";
import {ErrorPage} from "./ErrorPage";
import {ApiAnkiUserLoggedIn} from "../model/ApiAnkiUserLoggedIn";


const COOKIE_KEY_FIRST_TIME_USER: string = 'FIRST-TIME-USER'

export function DictMask() {

    const [availLang, setAvailLang] = useState<Language[]>([])
    const [dictOptions, setDictOptions] = useState<DictOptionsItem[]>([])
    const [showAnkiLogin, setShowAnkiLogin] = useState(false);
    const [showAnkiStatusAlert, setShowAnkiStatusAlert] = useState(false);
    const [showErrorPage, setShowErrorPage] = useState(false);
    const [showInfoPage, setShowInfoPage] = useState(false);
    const [apiHealth, setApiHealth] = useState<ApiHealthInformation>(ApiHealthInformation.createInvalidStatus)

    const cookieProvider: CookieService = new CookieService();
    const cookies: Cookies = new Cookies(null, {path: '/'})

    const debugWrapper = (e: any) => {
        console.log('debug wrapper: ', e)
        setAvailLang(e)
    }


    useEffect(() => {
        wotdApiHealthStatus().then((healthStatus: ApiHealthInformation): void => {
                setApiHealth(healthStatus)
                handleDbConnection(healthStatus)
                handleUserLogin(healthStatus)
                handleFirstTimeUser()
            }
        )
    }, []);


    const handleDbConnection = (healthStatus: ApiHealthInformation): void => {
        if (!healthStatus.dbConnection) {
            console.error('db connection down: ', healthStatus)
        } else {
            console.log('before setting avail lang')
            // dictGetAvailableLang().then(debugWrapper)
            dictGetAvailableLang().then(setAvailLang)
            console.log('after setting avail lang: ', availLang)

        }
    }

    const handleUserLogin = (healthStatus: ApiHealthInformation): void => {
        if (!healthStatus.wotdApiConnection) {
            console.error('wotd api not available: ', healthStatus)
            // alert('Backend API not available - not possible to lookup words. Please try again later.')
            setShowErrorPage(true)
        } else if (!healthStatus.ankiApiConnection) {
            console.error('anki api not available: ', healthStatus)
        } else {
            ankiApiUserLoggedIn(cookieProvider.getHeaders()).then((credentialStatus: ApiAnkiUserLoggedIn): void => {
                if (!credentialStatus.ankiUserLoggedIn) {
                    console.log('anki user not logged in')
                    cookieProvider.cleanAllCookies(false)
                    if (!cookieProvider.ignoreLoginPrompt && !showAnkiStatusAlert) {
                        console.log('show anki status alert')
                        handleShowAnkiStatusAlert()
                    }
                }
            })
        }
    }

    const handleFirstTimeUser = (): void => {
        if (cookieProvider.firstTimeUser) {
            console.log('user is first time user')
            cookieProvider.firstTimeUser = false
            cookieProvider.setCookies()
            setShowInfoPage(true)
        }
    }


    const handleCloseAnkiLogin = () => setShowAnkiLogin(false)
    const handleShowAnkiLogin = () => setShowAnkiLogin(true)

    const handleCloseInfoPage = () => setShowInfoPage(false)
    const handleShowInfoPage = () => setShowInfoPage(true)


    const handleCloseAnkiStatusAlert = () => setShowAnkiStatusAlert(false)
    const handleShowAnkiStatusAlert = () => setShowAnkiStatusAlert(true)


    const handleAnkiLogin = (ankiResponse: AnkiLoginResponseHeaders): void => {
        console.log('update auth provider with signed email: ', ankiResponse.signedUsername)
        cookieProvider.loadAnkiLoginResponse(ankiResponse)
    }

    console.log('avail langs during dict mask render: ', availLang)

    const mainPage = <>
        <LoginAlert
            showAnkiStatusAlert={showAnkiStatusAlert}
            handleCloseAnkiStatusAlert={handleCloseAnkiStatusAlert}
            handleShowAnkiLogin={handleShowAnkiLogin}
            authProvider={cookieProvider}
        />

        {apiHealth.wotdApiConnection
            && <UserInput authProvider={cookieProvider}
                          setDictOptions={setDictOptions}
                          availLang={availLang}
                          handleShowInfoPage={handleShowInfoPage}
                          handleShowAnkiLogin={handleShowAnkiLogin}/>}

        <div className='mt-2'>
            {dictOptions !== undefined && dictOptions.length > 0
                ? <SelectableTable
                    apiResponse={dictOptions}
                    userIsLoggedIn={cookieProvider.userIsLoggedIn()}/>
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
                    cookieProvider={cookieProvider}
                />
            </Offcanvas>

            <Offcanvas show={showInfoPage} onHide={handleCloseInfoPage} className="w-100">
                <InfoPage/>
            </Offcanvas>

        </div>
    );
}
