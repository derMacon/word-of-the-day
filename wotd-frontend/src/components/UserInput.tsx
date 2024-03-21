import React, {useState} from 'react';
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {dictLookupWord} from "../logic/ApiFetcher";
import {LanguageUUID} from "../model/LanguageUUID";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCircleInfo, FaCloudArrowUp, FaCloudBolt} from "react-icons/fa6";
import {Language} from "../model/Language";
import {AuthService} from "../logic/AuthService";
import {DictOptionsItem} from "../model/DictOptionsItem";

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


    const handleLanguageSwitch = () => {
        let fromLangNewInstance: Language = selectedFromLang as Language
        let toLangNewInstance: Language = selectedToLang as Language
        setSelectedFromLang(toLangNewInstance)
        setSelectedToLang(fromLangNewInstance)
    }

    const handleDictLookup = async (word: string) => {
        let headers = props.authProvider.getHeaders()
        let apiResponse: DictOptionsItem[] = await dictLookupWord(word, selectedFromLang, selectedToLang, headers)
        console.log('api resp options: ', apiResponse)
        props.setDictOptions(apiResponse)
    }


    return (
        <div className='sticky pt-3 pb-2 bg-white white-shadow'>
                <Row>
                    <Col md={7} className='mb-2 pl-0 pr-1'>
                        <TextField onSubmit={handleDictLookup}/>
                    </Col>
                    <Col md={3} className='mb-2 px-1'>
                        <ButtonGroup className='w-100'>
                            {/*<LanguageSelect*/}
                            {/*    selectedElem={selectedFromLang}*/}
                            {/*    onSelect={setSelectedFromLang}*/}
                            {/*    availableLanguages={props.availLang}/>*/}
                            <LanguageSelect
                                selectedElem={selectedFromLang}
                                onSelect={setSelectedFromLang}
                                availableLanguages={props.availLang}/>
                            <Button variant='light' onClick={handleLanguageSwitch}><FaArrowsRotate
                                className='mb-1'/></Button>
                            <LanguageSelect
                                selectedElem={selectedToLang}
                                onSelect={setSelectedToLang}
                                availableLanguages={props.availLang}/>
                        </ButtonGroup>
                    </Col>
                    <Col md={1} className='mb-2 px-1'>
                        <Button variant='light' onClick={props.handleShowAnkiLogin}>
                            {props.authProvider.userIsLoggedIn()
                                ? (<FaCloudArrowUp className='mb-1'/>)
                                : (<FaCloudBolt className='mb-1'/>)}
                        </Button>
                    </Col>
                    <Col md={1} className='mb-2 px-0'>
                        <Button variant='light' onClick={props.handleShowInfoPage}>
                            <FaCircleInfo className='mb-1'/>
                        </Button>
                    </Col>
                </Row>

        </div>
    );
}
