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


class DropdownSelect extends Component {

    constructor(props) {
        super(props);
        this.handleOnClick = this.handleOnClick.bind(this)
        console.log(props)

        let selectedElem = '';
        if (this.props.children !== undefined
            && this.props.selectedIndex !== undefined
            && this.props.selectedIndex >= 0
            && this.props.selectedIndex < this.props.children.length
        ) {
            selectedElem = this.props.children[this.props.selectedIndex]
        } else {
            console.log('not able to preselect element in dropdown')
        }

        this.state = {
            selectedElem: selectedElem,
        };
    }

    handleOnClick(inputText) {
        this.setState({selectedElem: inputText});
        this.props.onSelect(inputText)
    }

    render() {

        const items = this.props.children.map((item, index) => (
            <Dropdown.Item key={index} onClick={() => this.handleOnClick(item)}>
                {item}
            </Dropdown.Item>
        ))

        return (
            <DropdownButton title={this.state.selectedElem}>
                {items}
            </DropdownButton>
        );

    }
}

DropdownSelect.propTypes = {
    selectedIndex: PropTypes.number,
    onSelect: PropTypes.func.isRequired,
    children: PropTypes.arrayOf(PropTypes.string)
}

export default DropdownSelect;
