import React, {useEffect, useState} from 'react';
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {dictLookupWord, socket} from "../logic/ApiFetcher";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCircleInfo, FaCloudArrowUp, FaCloudBolt} from "react-icons/fa6";
import {Language} from "../model/Language";
import {AuthService} from "../logic/AuthService";
import {DictOptionsItem} from "../model/DictOptionsItem";
import Cookies from "universal-cookie";
import {socketAutocompleteWord} from "../logic/SocketFetcher";
import {InfoRequestDefaultLang} from "../model/InfoRequestDefaultLang";
import {plainToClass} from "class-transformer";

interface UserInputProps {
    authProvider: AuthService
    setDictOptions: (options: DictOptionsItem[]) => void
    availLang: Language[]
    handleShowAnkiLogin: (e: any) => void
    handleShowInfoPage: (e: any) => void
}


export function UserInput(props: Readonly<UserInputProps>) {

    const defaultFromLang: Language = new Language('EN', 'english')
    const defaultToLang: Language = new Language('DE', 'german')

    const [selectedFromLang, setSelectedFromLang] = useState<Language>(defaultFromLang)
    const [selectedToLang, setSelectedToLang] = useState<Language>(defaultToLang)

    const [isConnected, setIsConnected] = useState(socket.connected); // TODO what do we need this for?

    const cookies: Cookies = new Cookies(null, {path: '/'})
    const fromLangCookieKey: string = 'FROM-LANG'
    const toLangCookieKey: string = 'TO-LANG'

    const cookieSetFromLang = (lang: Language): void => {
        setSelectedFromLang(lang)

        // let requestWrapper: InfoRequestDefaultLang = plainToClass(InfoRequestDefaultLang, jsonObject)

        console.log('test json: ', JSON.stringify(lang))

        // cookies.set(fromLangCookieKey, JSON.stringify(lang))
        cookies.set(fromLangCookieKey, lang)
    }
    const cookieSetToLang = (lang: Language): void => {
        setSelectedToLang(lang)
        cookies.set(toLangCookieKey, lang.language_uuid.toString())
    }


    useEffect((): void => {
        const fromLang: Language | undefined = cookies.get(fromLangCookieKey)
        const toLang: Language | undefined = cookies.get(toLangCookieKey)

        console.log('userinput useeffect hook: ', fromLang)

        // if (props.availLang.length >= 2) {
        //     console.log('before setting lang', props.availLang)
        //     // setSelectedFromLang(props.availLang[0])
        //     cookieSetFromLang(props.availLang[0])
        //     setSelectedToLang(props.availLang[1])
        //     console.log('after setting lang')
        // }


        if (fromLang !== undefined) {
            cookieSetFromLang(fromLang)
        } else {
            cookieSetFromLang(defaultFromLang)
        }
        if (toLang !== undefined) {
            cookieSetToLang(toLang)
        } else {
            cookieSetToLang(defaultToLang)
        }


    }, [props.availLang])


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


    const handleLanguageSwitch = () => {
        let fromLangNewInstance: Language = selectedFromLang as Language
        let toLangNewInstance: Language = selectedToLang as Language
        cookieSetFromLang(toLangNewInstance)
        cookieSetToLang(fromLangNewInstance)
    }

    const handleAutocomplete = (word: string): void => {
        console.log('autocompleting word: ', word)
        socketAutocompleteWord(word, selectedFromLang, selectedToLang)
        // let apiResponse: string[] = await dictAutocompleteWord(word, selectedFromLang, selectedToLang)
        // console.log('autocomplete api resp options: ', apiResponse)
        // return apiResponse
    }

    const handleDictLookup = async (word: string) => {
        let headers = props.authProvider.getHeaders()
        let apiResponse: DictOptionsItem[] | null = await dictLookupWord(word, selectedFromLang, selectedToLang, headers)
        console.log('api resp options: ', apiResponse)
        if (apiResponse == null) {
            apiResponse = []
        }
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
