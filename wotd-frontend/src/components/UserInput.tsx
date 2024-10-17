import React, {useEffect, useState} from 'react';
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {dictLookupWord} from "../logic/ApiFetcher";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCircleInfo, FaCloudArrowUp, FaCloudBolt} from "react-icons/fa6";
import {Language} from "../model/Language";
import {CookieService} from "../logic/CookieService";
import {DictOptionsItem} from "../model/DictOptionsItem";
import Cookies from "universal-cookie";
import {socket, socketAutocompleteWord} from "../logic/SocketFetcher";
import {classToPlain, plainToClass} from "class-transformer";

interface UserInputProps {
    authProvider: CookieService
    setDictOptions: (options: DictOptionsItem[]) => void
    availLang: Language[]
    handleShowAnkiLogin: (e: any) => void
    handleShowInfoPage: (e: any) => void
}

interface LangCookieFormat {
    cookieKey: string;
    defaultValue: Language;
}

const LangCookieDefaults: { fromLang: LangCookieFormat; toLang: LangCookieFormat } = {
    fromLang: {
        cookieKey: 'FROM-LANG',
        defaultValue: new Language('', 'DE', 'German'),
    },
    toLang: {
        cookieKey: 'TO-LANG',
        defaultValue: new Language('', 'EN', 'English'),
    }
};


export function UserInput(props: Readonly<UserInputProps>) {

    const [selectedFromLang, setSelectedFromLang] = useState<Language>(LangCookieDefaults.fromLang.defaultValue)
    const [selectedToLang, setSelectedToLang] = useState<Language>(LangCookieDefaults.toLang.defaultValue)

    const [isConnected, setIsConnected] = useState(socket.connected); // TODO what do we need this for?

    const cookies: Cookies = new Cookies(null, {path: '/'})


    const cookieSetLanguage = (langCookieFormat: LangCookieFormat, lang: Language): void => {
        const plainLanguageObject = classToPlain(lang);
        const jsonString: string = JSON.stringify(plainLanguageObject);
        cookies.set(langCookieFormat.cookieKey, jsonString)
    }

    const cookieGetLanguage = (langCookieFormat: LangCookieFormat): Language => {
        const cookieJson: string | undefined = cookies.get(langCookieFormat.cookieKey)
        if (cookieJson === undefined) {
            return langCookieFormat.defaultValue
        }
        return plainToClass(Language, cookieJson)

    }

    const cookieSetFromLang = (lang: Language): void => {
        setSelectedFromLang(lang)
        cookieSetLanguage(LangCookieDefaults.fromLang, lang)
    }

    const cookieSetToLang = (lang: Language): void => {
        setSelectedToLang(lang)
        cookieSetLanguage(LangCookieDefaults.toLang, lang)
    }


    useEffect((): void => {
        setSelectedFromLang(cookieGetLanguage(LangCookieDefaults.fromLang))
        setSelectedToLang(cookieGetLanguage(LangCookieDefaults.toLang))
    }, [])


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
