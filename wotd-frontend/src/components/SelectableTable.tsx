import React, {useCallback, useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {toggleSelectedOption, wotdApiHealthStatus} from "../logic/ApiFetcher";
import './SelectableTable.css';
import {DictOptionsItem} from "../model/DictOptionsItem";


interface SelectableTableProps {
    apiResponse: DictOptionsItem[]
    userIsLoggedIn: boolean
}

export function SelectableTable(props: Readonly<SelectableTableProps>) {


    // Memoize the highlight data function
    const hightlight_data = useCallback(() => {
        const initialHighlight = new Map<number, boolean>();
        props.apiResponse.forEach((option: DictOptionsItem) => {
            console.log('inside api response foreach: ', option);
            initialHighlight.set(option.dictOptionsItemId, option.selected);
        });
        return initialHighlight;
    }, [props.apiResponse]);


    const [highlight, setHighlight] = useState<Map<number, boolean>>(hightlight_data);


    useEffect(() => {
        setHighlight(hightlight_data)
    }, [hightlight_data]);


    const handleSelection = (selectedOption: DictOptionsItem) => {
        wotdApiHealthStatus().then(e => {
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
