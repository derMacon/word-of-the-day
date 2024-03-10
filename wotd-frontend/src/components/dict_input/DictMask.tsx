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
        let apiResponse = await dictLookupWord(word, selectedFromLang, selectedToLang)
        console.log('api resp options: ', apiResponse)
        setDictOptions(apiResponse)
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

                <Container fluid="md">
                    <div className="custom-max-width">
                        <Offcanvas.Header closeButton>
                            <Offcanvas.Title>Anki Sync</Offcanvas.Title>
                        </Offcanvas.Header>
                        <Offcanvas.Body>

                            <p>You are currently not logged into your anki account.
                                In order to sync the dictionary searches with anki web please log in.</p>

                            <br/>

                            <Form>
                                <Form.Group className="mb-3">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control type="email" placeholder="name@example.com"/>
                                </Form.Group>
                                <Form.Group className="mb-3">
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control type="password" placeholder="Password"/>
                                </Form.Group>
                            </Form>

                            <Button variant="light">Login</Button>


                            {/*<p>Word Vaults</p>*/}
                            {/*<ListGroup>*/}
                            {/*    <ListGroup.Item>English Dictionary</ListGroup.Item>*/}
                            {/*    <ListGroup.Item disabled>German Duden Definitions</ListGroup.Item>*/}
                            {/*</ListGroup>*/}

                        </Offcanvas.Body>
                    </div>
                </Container>
            </Offcanvas>
        </div>
    );
}
