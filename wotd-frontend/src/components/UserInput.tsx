import React, {useEffect, useState} from 'react';
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {dictAutocompleteWord, dictLookupWord, socket} from "../logic/ApiFetcher";
import {convertToLanguageUUIDEnum, LanguageUUID} from "../model/LanguageUUID";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCircleInfo, FaCloudArrowUp, FaCloudBolt} from "react-icons/fa6";
import {Language} from "../model/Language";
import {AuthService} from "../logic/AuthService";
import {DictOptionsItem} from "../model/DictOptionsItem";
import Cookies from "universal-cookie";

interface UserInputProps {
    authProvider: AuthService
    setDictOptions: (options: DictOptionsItem[]) => void
    availLang: Language[]
    handleShowAnkiLogin: (e: any) => void
    handleShowInfoPage: (e: any) => void
}


export function UserInput(props: Readonly<UserInputProps>) {

    const defaultFromLang = new Language(LanguageUUID.EN, 'english')
    const defaultToLang = new Language(LanguageUUID.DE, 'german')

    const [selectedFromLang, setSelectedFromLang] = useState<Language>(defaultFromLang)
    const [selectedToLang, setSelectedToLang] = useState<Language>(defaultToLang)

    const [isConnected, setIsConnected] = useState(socket.connected);

    const cookies: Cookies = new Cookies(null, {path: '/'})
    const fromLangCookieKey: string = 'from-lang' // TODO all caps
    const toLangCookieKey: string = 'to-lang'

    const cookieSetFromLang = (lang: Language) => {
        setSelectedFromLang(lang)
        cookies.set(fromLangCookieKey, lang.language_uuid.toString())
    }
    const cookieSetToLang = (lang: Language) => {
        setSelectedToLang(lang)
        cookies.set(toLangCookieKey, lang.language_uuid.toString())
    }

    // TODO fix this
    // useEffect(() => {
    //     const fromLang: LanguageUUID | undefined = convertToLanguageUUIDEnum(cookies.get(fromLangCookieKey))
    //     const toLang: LanguageUUID | undefined = convertToLanguageUUIDEnum(cookies.get(toLangCookieKey))
    //
    //     if (fromLang !== undefined) {
    //         cookieSetFromLang(Language.createFromUUID(fromLang))
    //     } else {
    //         cookieSetFromLang(defaultFromLang)
    //     }
    //     if (toLang !== undefined) {
    //         cookieSetToLang(Language.createFromUUID(toLang))
    //     } else {
    //         cookieSetToLang(defaultToLang)
    //     }
    //
    // }, [cookieSetFromLang, cookieSetToLang, cookies, defaultFromLang, defaultToLang]);

    useEffect(() => {

        function onConnect() {
            console.log('connected to socket')
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
            alert('backend offline - check the docker compose setup on the host')
        }

        function onAutocorrectReceive(value: string[]) {
            console.log('executing test call: ', value)
        }

        console.log('before trying to connect')
        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('update_autocorrect', onAutocorrectReceive);
        console.log('after trying to connect')

        return () => {
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('update_autocorrect', onAutocorrectReceive);
        };
    }, []);


    const handleLanguageSwitch = () => {
        let fromLangNewInstance: Language = selectedFromLang as Language
        let toLangNewInstance: Language = selectedToLang as Language
        cookieSetFromLang(toLangNewInstance)
        cookieSetToLang(fromLangNewInstance)
    }

    const handleAutocomplete = async (word: string): Promise<string[]> => {
        console.log('autocompleting word: ', word)
        let apiResponse: string[] = await dictAutocompleteWord(word, selectedFromLang, selectedToLang)
        console.log('autocomplete api resp options: ', apiResponse)
        return apiResponse
    }

    const handleDictLookup = async (word: string) => {
        let headers = props.authProvider.getHeaders()
        let apiResponse: DictOptionsItem[] = await dictLookupWord(word, selectedFromLang, selectedToLang, headers)
        console.log('api resp options: ', apiResponse)
        props.setDictOptions(apiResponse)
    }


    return (
        <div className='sticky pt-2 pb-2 bg-white white-shadow'>
            <Row>
                <Col xs={12} md={7} className='pe-md-1 pb-2'>
                    <TextField onSubmit={handleDictLookup} onType={handleAutocomplete}/>
                </Col>

                <Col xs={8} md={3} className='ps-md-0 pe-1'>
                    <ButtonGroup className='w-100'>
                        <LanguageSelect
                            selectedElem={selectedFromLang}
                            onSelect={cookieSetFromLang}
                            availableLanguages={props.availLang}/>
                        <Button variant='light' onClick={handleLanguageSwitch}><FaArrowsRotate
                            className='mb-1'/></Button>
                        <LanguageSelect
                            selectedElem={selectedToLang}
                            onSelect={cookieSetToLang}
                            availableLanguages={props.availLang}/>
                    </ButtonGroup>
                </Col>

                <Col xs={4} md={2} className='ps-0'>
                    <ButtonGroup className='w-100'>
                        <Button variant='light' onClick={props.handleShowInfoPage}>
                            <FaCircleInfo className='mb-1'/>
                        </Button>
                        <Button variant='light' onClick={props.handleShowAnkiLogin}>
                            {props.authProvider.userIsLoggedIn()
                                ? (<FaCloudArrowUp className='mb-1'/>)
                                : (<FaCloudBolt className='mb-1'/>)}
                        </Button>
                    </ButtonGroup>
                </Col>
            </Row>

        </div>
    );
}
