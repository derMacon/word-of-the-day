import React, {Component} from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import Card from 'react-bootstrap/Card';
import InputGroup from 'react-bootstrap/InputGroup';
import './ItemInput.css';
import {FaTimes} from "react-icons/fa";


// import Checklist from './Checklist';


class ItemInput extends Component {

    constructor(props) {
        super(props);
        this.handleKeyDown = this.handleKeyDown.bind(this)
        this.handleInputChange = this.handleInputChange.bind(this)
        this.handleOnClear = this.handleOnClear.bind(this)
        this.state = {
            input: '',
        };
    }

    // handleKeyDown(e) {
    //     if (e.code == "Enter") {
    //         console.log('user pressed enter, submitting: ', e.target.value)
    //         const output = e.target.value
    //         this.setState({input: ''})
    //         this.props.onSubmit(output)
    //     } else {
    //         console.log('target val: ', e.target.value)
    //     }
    //     this.setState({input: e.target.value})
    // }

    handleKeyDown(e) {
        if (e.code === 'Enter') {
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
        this.setState({input: ''})
    }

    handleInputChange(e) { // Add this function
        this.setState({input: e.target.value});
    }

    render() {

        return (
            <div>
                <InputGroup
                    className='my-3 shadow bg-white rounded border-1'>
                    <Form.Control
                        autoFocus
                        type="text"
                        value={this.state.input}
                        onChange={this.handleInputChange}
                        onKeyDown={this.handleKeyDown}
                    />
                    <InputGroup.Text onClick={this.handleOnClear}>
                        <FaTimes/>
                    </InputGroup.Text>
                </InputGroup>
            </div>
        );
    }
}

export default ItemInput;
