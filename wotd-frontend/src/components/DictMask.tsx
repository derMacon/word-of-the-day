import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import {SelectableTable} from "./SelectableTable";
import {dictGetAvailableLang, dictLookupWord} from "../logic/ApiFetcher";
import {Language} from "../model/Language";
import {DictOptionsResponse} from "../model/DictOptionsResponse";


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

    // const


    return (
        <div>

            <Container fluid="md">
                <div className='my-3 shadow bg-white rounded border-1'>
                    <TextField onSubmit={async output => {
                        console.log("top level before output: ", output)
                        let apiResponse = await dictLookupWord(output, selectedFromLang, selectedToLang)
                        console.log('plain api response: ', apiResponse)
                        setDictOptions(apiResponse)
                        // console.log('api response: ', dictOptions!.dictRequest)
                        console.log("top level after output: ", output)
                    }}/>
                </div>
                <DropdownSelect
                    selectedElem={selectedFromLang}
                    onSelect={setSelectedFromLang}>
                    {availLang}
                </DropdownSelect>
                {dictOptions !== undefined && (
                    <SelectableTable options={dictOptions}/>
                )}
            </Container>
        </div>
    );

}
