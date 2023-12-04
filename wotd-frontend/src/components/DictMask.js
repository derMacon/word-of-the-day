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


class DictMask extends Component {

    constructor(props) {
        super(props);
        this.handleOnClick = this.handleOnClick.bind(this)
        console.log(props)
        this.state = {
            input: '',
        };
    }

    handleKeyDown(e) {
        if (e.code === 'Enter' || e.which === 13) {
            console.log('user pressed enter, submitting: ', e.target.value);
            const output = e.target.value;
            this.setState({input: ''});
            this.props.onSubmit(output);
        } else {
            console.log('target val: ', e.target.value);
        }
    }

    handleOnClear(e) {
        console.log("user cleared input")
        this.setState({input: ''}, () => {
            this.inputRef.current.focus(); // Set focus after state is updated
        });
    }

    handleInputChange(e) { // Add this function
        this.setState({input: e.target.value});
    }

    handleOnClick(e) {
        console.log('clicked', e)
    }

    render() {

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
                    <SelectableTable/>
                    <p>works</p>
                </Container>
            </div>
        );

    }
}

// TextField.propTypes = {
//     onSubmit: PropTypes.func.isRequired
// }

export default DictMask;
