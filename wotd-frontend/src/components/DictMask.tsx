import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import {SelectableTable} from "./SelectableTable";
import {dictGetAvailableLang, dictLookupWord} from "../logic/ApiFetcher";
import {Language} from "../model/Language";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import {FaArrowsRotate} from "react-icons/fa6";


export function DictMask() {

    const [selectedFromLang, setSelectedFromLang] = useState<Language>(Language.EN) // TODO use cookie values here
    const [selectedToLang, setSelectedToLang] = useState<Language>(Language.DE) // TODO use cookie values here
    const [availLang, setAvailLang] = useState<Map<Language, string>>(new Map())
    const [dictOptions, setDictOptions] = useState<DictOptionsResponse>()

    useEffect(() => {
        dictGetAvailableLang().then((languages: Language[]) => {
                console.log('languages: ', languages.length)
                const langMap: Map<Language, string> = new Map<Language, string>()
                for (let i = 0; i < languages.length; i++) {
                    langMap.set(languages[i], languages[i].toString())
                }
                setAvailLang(langMap)
            }
        )
    }, []);

    const handleLanguageSwitch = () => {
        let fromLangNewInstance: Language = selectedFromLang.toString() as Language
        let toLangNewInstance: Language = selectedToLang.toString() as Language
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

                {/*<table className="table">*/}
                {/*    <colgroup>*/}
                {/*        <col className="bg-success"></col>*/}
                {/*        <col className="bg-info"></col>*/}
                {/*        <col className="bg-danger"></col>*/}
                {/*    </colgroup>*/}
                {/*    <thead>*/}
                {/*    <tr>*/}
                {/*        <th scope="col" className='bg-primary'>ID</th>*/}
                {/*        <th scope="col">Name</th>*/}
                {/*        <th scope="col">Age</th>*/}
                {/*    </tr>*/}
                {/*    </thead>*/}
                {/*    <tbody>*/}
                {/*    <tr>*/}
                {/*        <td className="bg-primary">1</td>*/}
                {/*        <td>John</td>*/}
                {/*        <td>25</td>*/}
                {/*    </tr>*/}
                {/*    <tr className="highlight bg-primary">*/}
                {/*        <td>2</td>*/}
                {/*        <td>Jane</td>*/}
                {/*        <td>30</td>*/}
                {/*    </tr>*/}
                {/*    <tr style={{backgroundColor: '#930000'}}>*/}
                {/*        <td>3</td>*/}
                {/*        <td>Bob</td>*/}
                {/*        <td>22</td>*/}
                {/*    </tr>*/}
                {/*    </tbody>*/}
                {/*</table>*/}

                {dictOptions !== undefined && (
                    <div className='mt-2'>
                        <SelectableTable apiResponse={dictOptions}/>
                    </div>
                )}
            </Container>
        </div>
    );
}
