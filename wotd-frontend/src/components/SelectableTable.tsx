import React, {Component} from 'react';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";
import PropTypes from "prop-types";
import Table from 'react-bootstrap/Table';


interface SelectableTableProps {
   rows : [string, string][]
}

interface SelectableTableState {

}

class SelectableTable extends Component<SelectableTableProps, SelectableTableState> {

    constructor(props: SelectableTableProps) {
        super(props);
        this.handleOnClick = this.handleOnClick.bind(this)
    }

    handleOnClick(e: React.MouseEvent<HTMLTableRowElement>) {
        console.log(e)
    }

    render() {

        const rows = this.props.rows.map(())

        return (
            <Table striped bordered hover>
                <thead>
                <tr>
                    <th>Last Name</th>
                    <th>Username</th>
                </tr>
                </thead>
                <tbody>
                <tr onClick={this.handleOnClick}>
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
}


export default SelectableTable;
