import React, {Component} from 'react';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";
import PropTypes from "prop-types";
import Table from 'react-bootstrap/Table';


class SelectableTable extends Component {

    constructor(props) {
        super(props);
        this.handleKeyDown = this.handleKeyDown.bind(this)
        this.handleInputChange = this.handleInputChange.bind(this)
        this.handleOnClear = this.handleOnClear.bind(this)
        this.inputRef = React.createRef();
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

    render() {

        return (
            <Table striped bordered hover>
                <thead>
                <tr>
                    <th>Last Name</th>
                    <th>Username</th>
                </tr>
                </thead>
                <tbody>
                <tr onClick={e => console.log('user clicked row')}>
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

// TextField.propTypes = {
//     onSubmit: PropTypes.func.isRequired
// }

export default SelectableTable;
