import React from 'react';
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

    const handleOnClick = (e: React.MouseEvent<HTMLTableRowElement>, selectedOption: Option) => {
        console.log(e)
        // console.log(apiIsHealthy())
        apiIsHealthy().then(e => console.log(selectedOption))
    }

    console.log('in table options: ', props.apiResponse.options)

    const items: JSX.Element[] = []
    props.apiResponse.options.forEach((option: Option) => items.push(
        <tr onClick={(e: React.MouseEvent<HTMLTableRowElement>) => handleOnClick(e, option)}>
            <td>{option.input}</td>
            <td>{option.output}</td>
        </tr>
    ))


    return (
        <Table striped bordered hover>
            <thead>
            <tr>
                <th>{props.apiResponse.dictRequest.fromLanguage.toString()}</th>
                <th>{props.apiResponse.dictRequest.toLanguage.toString()}</th>
            </tr>
            </thead>
            <tbody>
                {items}
            </tbody>
        </Table>
    );
}
