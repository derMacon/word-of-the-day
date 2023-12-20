import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiIsHealthy, pushSelectedOption} from "../../logic/ApiFetcher";
import {DictOptionsResponse} from "../../model/DictOptionsResponse";
import {Option} from "../../model/Option";
import './SelectableTable.css';
import {DictOptionsItem} from "../../model/DictOptionsItem";


interface SelectableTableProps {
    apiResponse: DictOptionsResponse
}

export function SelectableTable(props: Readonly<SelectableTableProps>) {

    const [highlight, setHighlight] = useState<Map<number, boolean>>(() => {
        const initialHighlight = new Map();
        props.apiResponse.options.forEach((option: DictOptionsItem) => {
            initialHighlight.set(option.dictOptionsItemId, false);
        });

        return initialHighlight;
    });

    useEffect(() => {
        // preselect first entry
        if (props.apiResponse.options.length > 0) {
            handleSelection(props.apiResponse.options[0])
        }
    }, []);

    const handleSelection = (selectedOption: DictOptionsItem) => {
        apiIsHealthy().then(e => {
            let state: boolean = !highlight.get(selectedOption.dictOptionsItemId)
            setHighlight((prevHighlight) => new Map(prevHighlight).set(selectedOption.dictOptionsItemId, state))

            if (highlight.get(selectedOption.dictOptionsItemId)) {
                // TODO unselect
            } else {
                pushSelectedOption(selectedOption.dictOptionsItemId)
            }
        })
    }

    const items: JSX.Element[] = []
    props.apiResponse.options.forEach((option: DictOptionsItem) => items.push(
        <tr key={option.dictOptionsItemId} onClick={(e: React.MouseEvent<HTMLTableRowElement>) => handleSelection(option)}>
            <td className={`w-50 ${highlight.get(option.dictOptionsItemId) ? 'text-bg-dark bg-secondary' : ''}`}>{option.input}</td>
            <td className={`w-50 ${highlight.get(option.dictOptionsItemId) ? 'text-bg-dark bg-secondary' : ''}`}>{option.output}</td>
        </tr>
    ))

    return (
        <Table striped bordered hover className='table-fixed'>
            <thead>
            {/*<tr>*/}
            {/*    <th>{props.apiResponse.dictRequest.fromLanguage.toString()}</th>*/}
            {/*    <th>{props.apiResponse.dictRequest.toLanguage.toString()}</th>*/}
            {/*</tr>*/}
            </thead>
            <tbody>
            {items}
            </tbody>
        </Table>
    );
}
