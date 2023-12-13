import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiIsHealthy} from "../logic/ApiFetcher";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {Option} from "../model/Option";
import './SelectableTable.css';


interface SelectableTableProps {
    apiResponse: DictOptionsResponse
}

export function SelectableTable(props: SelectableTableProps) {

    const [highlight, setHighlight] = useState<Map<number, boolean>>(() => {
        const initialHighlight = new Map();
        props.apiResponse.options.forEach((option) => {
            initialHighlight.set(option.id, false);
        });
        return initialHighlight;
    });

    const handleOnClick = (e: React.MouseEvent<HTMLTableRowElement>, selectedOption: Option) => {
        console.log(e)
        apiIsHealthy().then(e => {
            console.log(selectedOption)
            let state: boolean = !highlight.get(selectedOption.id)
            setHighlight((prevHighlight) => new Map(prevHighlight).set(selectedOption.id, state));
        })
    }

    console.log('in table options: ', props.apiResponse.options)

    const items: JSX.Element[] = []
    props.apiResponse.options.forEach((option: Option) => items.push(
        <tr onClick={(e: React.MouseEvent<HTMLTableRowElement>) => handleOnClick(e, option)}>
            <td className={`w-50 ${highlight.get(option.id) ? 'text-bg-dark bg-secondary' : ''}`}>{option.input}</td>
            <td className={`w-50 ${highlight.get(option.id) ? 'text-bg-dark bg-secondary' : ''}`}>{option.output}</td>
            {/*<td className='w-25 bg-warning-subtle'>{option.output}</td>*/}
        </tr>
    ))

    console.log('--------------- hightlights: ', highlight)

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
