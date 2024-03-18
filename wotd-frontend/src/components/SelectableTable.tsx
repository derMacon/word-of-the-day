import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiHealthStatus, toggleSelectedOption} from "../logic/ApiFetcher";
import './SelectableTable.css';
import {DictOptionsItem} from "../model/DictOptionsItem";


interface SelectableTableProps {
    apiResponse: DictOptionsItem[]
    userIsLoggedIn: boolean
}

export function SelectableTable(props: Readonly<SelectableTableProps>) {

    const [highlight, setHighlight] = useState<Map<number, boolean>>(() => {
        const initialHighlight = new Map();
        props.apiResponse.forEach((option: DictOptionsItem) => {
            initialHighlight.set(option.dictOptionsItemId, false);
        });

        return initialHighlight;
    });

    useEffect(() => {
        // preselect first entry
        if (props.apiResponse.length > 0) {
            let selectedOption = props.apiResponse[0]
            let state: boolean = !highlight.get(selectedOption.dictOptionsItemId)
            setHighlight((prevHighlight: Map<number, boolean>) => new Map(prevHighlight).set(selectedOption.dictOptionsItemId, state))
        }
    }, []);

    const handleSelection = (selectedOption: DictOptionsItem) => {
        apiHealthStatus().then(e => {
            let state: boolean = !highlight.get(selectedOption.dictOptionsItemId)
            setHighlight((prevHighlight: Map<number, boolean>) => new Map(prevHighlight).set(selectedOption.dictOptionsItemId, state))
            if (props.userIsLoggedIn) {
                console.log('user logged in, sending selection to backend')
                toggleSelectedOption(selectedOption.dictOptionsItemId)
            } else {
                console.log('user not logged in, not able to send selection to backend')
            }
        })
    }

    const items: JSX.Element[] = []
    props.apiResponse.forEach((option: DictOptionsItem) => items.push(
        <tr key={option.dictOptionsItemId}
            onClick={(e: React.MouseEvent<HTMLTableRowElement>) => handleSelection(option)}>
            <td className={`w-50 ${highlight.get(option.dictOptionsItemId) ? 'text-bg-dark bg-secondary' : ''}`}>{option.input}</td>
            <td className={`w-50 ${highlight.get(option.dictOptionsItemId) ? 'text-bg-dark bg-secondary' : ''}`}>{option.output}</td>
        </tr>
    ))

    return (
        <Table striped bordered hover className='table-fixed'>
            <thead>
            {/*<tr>*/}
            {/*TODO delete this*/}
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
