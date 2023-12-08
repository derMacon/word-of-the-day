import React, {Component} from 'react';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";
import PropTypes from "prop-types";
import Table from 'react-bootstrap/Table';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Container from "react-bootstrap/Container";
import TextField from "./TextField";
import DropdownSelect from "./DropdownSelect";
import SelectableTable from "./SelectableTable";


export function DictMask() {

    const testInput = ['a', 'b', 'c']

    return (
        <div>

            <Container fluid="md">
                <div className='my-3 shadow bg-white rounded border-1'>
                    <TextField onSubmit={output => console.log("top level output: ", output)}/>
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
