import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiIsHealthy} from "../logic/ApiFetcher";
import {DictOptionsResponse} from "../model/DictOptionsResponse";


interface SelectableTableProps {
    options: DictOptionsResponse
}

export function SelectableTable(props: SelectableTableProps) {

    const handleOnClick = (e: React.MouseEvent<HTMLTableRowElement>) => {
        console.log(e)
        // console.log(apiIsHealthy())
        apiIsHealthy().then(e => console.log(e))
    }

    console.log('in table options: ', props.options.dictRequest)

    return (
        <Table striped bordered hover>
            <thead>
            <tr>
                <th>{props.options.dictRequest.fromLanguage.toString()}</th>
                <th>{props.options.dictRequest.toLanguage.toString()}</th>
            </tr>
            </thead>
            <tbody>
            <tr onClick={handleOnClick}>
                <td>Otto</td>
                <td>@mdo</td>
            </tr>
            <tr>
                <td>Thornton</td>
                <td>@fat</td>
            </tr>

            </tbody>
        </Table>
    );
}
