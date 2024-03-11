import React, {useEffect, useState} from 'react';
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import LanguageSelect from "./LanguageSelect";
import {SelectableTable} from "./SelectableTable";
import {dictGetAvailableLang, dictLookupWord} from "../../logic/ApiFetcher";
import {LanguageUUID} from "../../model/LanguageUUID";
import {DictOptionsResponse} from "../../model/DictOptionsResponse";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate, FaCloudBolt} from "react-icons/fa6";
import {Language} from "../../model/Language";
import Offcanvas from "react-bootstrap/Offcanvas";
import ListGroup from "react-bootstrap/ListGroup";
import Form from 'react-bootstrap/Form';
import AnkiSyncLogin from "./AnkiSyncLogin";


export function DictMask() {

    const defaultFromLang = new Language(LanguageUUID.EN, 'english')
    const defaultToLang = new Language(LanguageUUID.DE, 'german')

    const [selectedFromLang, setSelectedFromLang] = useState<Language>(defaultFromLang)
    const [selectedToLang, setSelectedToLang] = useState<Language>(defaultToLang)
    const [availLang, setAvailLang] = useState<Language[]>([])
    const [dictOptions, setDictOptions] = useState<DictOptionsResponse>()
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    useEffect(() => {
        dictGetAvailableLang().then(setAvailLang)
    }, []);

    const handleLanguageSwitch = () => {
        let fromLangNewInstance: Language = selectedFromLang as Language
        let toLangNewInstance: Language = selectedToLang as Language
        setSelectedFromLang(toLangNewInstance)
        setSelectedToLang(fromLangNewInstance)
    }

    const handleDictLookup = async (word: string) => {
        let apiResponse: DictOptionsResponse = await dictLookupWord(word, selectedFromLang, selectedToLang)
        console.log('api resp options: ', apiResponse)
        setDictOptions(apiResponse)
    }

    const handleAnkiSyncLogin = (email: string, password: string) => {
        console.log('user logged into anki with email: ', email)
        console.log('user logged into anki with pass: ', password)
    }

    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width">

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
                                        availableLanguages={availLang}/>
                                    <Button variant='light' onClick={handleLanguageSwitch}><FaArrowsRotate
                                        className='mb-1'/></Button>
                                    <LanguageSelect
                                        selectedElem={selectedToLang}
                                        onSelect={setSelectedToLang}
                                        availableLanguages={availLang}/>
                                </ButtonGroup>
                            </Col>
                            <Col xs={12} md={1}>
                                {/*FaCloudArrowUp*/}
                                <Button variant='light' onClick={handleShow}><FaCloudBolt
                                    className='mb-1'/></Button>
                            </Col>
                        </Row>
                    </div>

                    {dictOptions !== undefined && (
                        <div className='mt-2'>
                            <SelectableTable apiResponse={dictOptions}/>
                        </div>
                    )}
                </div>

            </Container>


            <Offcanvas show={show} onHide={handleClose} className="w-100">
                <AnkiSyncLogin handleAnkiLogin={handleAnkiSyncLogin} />
            </Offcanvas>

        </div>
    );
}
