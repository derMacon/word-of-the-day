import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import {SelectableTable} from "./SelectableTable";
import {dictLookupWord} from "../logic/ApiFetcher";
import {Language} from "../data/Language";


export function DictMask() {

    // const []

    const testInput = ['a', 'b', 'c']

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
                    selectedIndex={1}
                    onSelect={e => console.log('user selected: ', e)}>
                    {testInput}
                </DropdownSelect>
                <SelectableTable
                    rows={[['test1', 'test2']]}
                />
                <p>works</p>
            </Container>
        </div>
    );

}
