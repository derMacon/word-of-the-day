import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import {SelectableTable} from "./SelectableTable";
import {apiIsHealthy, dictGetAvailableLang, dictLookupWord} from "../logic/ApiFetcher";
import {Language} from "../data/Language";


export function DictMask() {

    // const []

    const testInput = ['a', 'b', 'c']

    const [availLang, setAvailLang] = useState<Map<Language, string>>(new Map())


    useEffect(() => {
        dictGetAvailableLang().then((languages: Language[]) => {
                console.log('languages: ', languages.length)
                const langMap: Map<Language, string> = new Map<Language, string>()
                for (let i = 0; i < languages.length; i++) {
                    console.log('lang: ', languages[i])
                    langMap.set(languages[i], languages[i].toString())
                }

                setAvailLang(langMap)
            }
        )
    }, []);


    return (
        <div>

            <Container fluid="md">
                <div className='my-3 shadow bg-white rounded border-1'>
                    <TextField onSubmit={output => {
                        console.log("top level before output: ", output)
                        dictLookupWord(output, Language.DE, Language.EN)
                        console.log("top level after output: ", output)
                    }}/>
                </div>
                <DropdownSelect
                    selectedElem={Language.EN}
                    onSelect={e => console.log('user selected: ', e)}>
                    {availLang}
                </DropdownSelect>
                <SelectableTable
                    rows={[['test1', 'test2']]}
                />
                <p>works</p>
            </Container>
        </div>
    );

}
