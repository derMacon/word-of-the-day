import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiIsHealthy} from "../logic/ApiFetcher";


interface SelectableTableProps {
    rows: [string, string][]
}

export function SelectableTable(props: SelectableTableProps) {

    const handleOnClick = (e: React.MouseEvent<HTMLTableRowElement>) => {
        console.log(e)
        // console.log(apiIsHealthy())
        apiIsHealthy().then(e => console.log(e))
    }

    return (
        <Table striped bordered hover>
            <thead>
            <tr>
                <th>Last Name</th>
                <th>Username</th>
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
