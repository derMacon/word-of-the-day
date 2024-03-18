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

interface UserInputProps {
    authProvider: AuthService
    setDictOptions: (options: DictOptionsItem[]) => void
    availLang: Language[]
    handleShowAnkiLogin: (e: any) => void
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
        <div className='sticky pt-3 pb-3 bg-white white-shadow'>
            <Row>
                <Col xs={12} md={8} className='mb-2'>
                    <TextField onSubmit={handleDictLookup}/>
                </Col>
                <Col xs={12} md={3}>
                    <ButtonGroup className='nopadding w-100'>
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
                <Col xs={12} md={1}>
                    <Button variant='light' onClick={props.handleShowAnkiLogin}>
                        {props.authProvider.userIsLoggedIn()
                            ? (<FaCloudArrowUp className='mb-1'/>)
                            : (<FaCloudBolt className='mb-1'/>)}

                    </Button>
                </Col>
            </Row>
        </div>
    );
}