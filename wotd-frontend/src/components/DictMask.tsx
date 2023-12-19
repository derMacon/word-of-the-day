import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import {SelectableTable} from "./SelectableTable";
import {dictGetAvailableLang, dictLookupWord, pushSelectedOption} from "../logic/ApiFetcher";
import {LanguageUUID} from "../model/LanguageUUID";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate} from "react-icons/fa6";
import {Language} from "../model/Language";


export function DictMask() {

    const [selectedFromLang, setSelectedFromLang] = useState<LanguageUUID>(LanguageUUID.EN) // TODO use cookie values here
    const [selectedToLang, setSelectedToLang] = useState<LanguageUUID>(LanguageUUID.DE) // TODO use cookie values here
    const [availLang, setAvailLang] = useState<Map<LanguageUUID, string>>(new Map())
    const [dictOptions, setDictOptions] = useState<DictOptionsResponse>()

    useEffect(() => {
        dictGetAvailableLang().then((languages: Language[]) => {
                const langMap: Map<LanguageUUID, string> = new Map<LanguageUUID, string>()
                for (let i = 0; i < languages.length; i++) {
                    langMap.set(languages[i].language_uuid, languages[i].name)
                }
                setAvailLang(langMap)
            }
        )
    }, []);

    const handleLanguageSwitch = () => {
        let fromLangNewInstance: LanguageUUID = selectedFromLang.toString() as LanguageUUID
        let toLangNewInstance: LanguageUUID = selectedToLang.toString() as LanguageUUID
        setSelectedFromLang(toLangNewInstance)
        setSelectedToLang(fromLangNewInstance)
    }

    const handleDictLookup = async (word: string) => {
        let apiResponse = await dictLookupWord(word, selectedFromLang, selectedToLang)
        setDictOptions(apiResponse)
    }

    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width">

                <div className='sticky pt-3 pb-3 bg-white white-shadow'>
                    <Row>
                        <Col xs={12} md={9} className='mb-2'>
                            <TextField onSubmit={handleDictLookup}/>
                        </Col>
                        <Col xs={12} md={3}>
                            <ButtonGroup className='nopadding w-100'>
                                <DropdownSelect
                                    selectedElem={selectedFromLang}
                                    onSelect={setSelectedFromLang}>
                                    {availLang}
                                </DropdownSelect>
                                <Button variant='light' onClick={handleLanguageSwitch}><FaArrowsRotate
                                    className='mb-1'/></Button>
                                <DropdownSelect
                                    selectedElem={selectedToLang}
                                    onSelect={setSelectedToLang}>
                                    {availLang}
                                </DropdownSelect>
                            </ButtonGroup>
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
        </div>
    );
}
