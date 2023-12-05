import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';


interface DropdownSelectProps {
    children: string[]
    selectedIndex?: number
    onSelect: (input: string) => void
}

interface DropdownSelectState {
    selectedElem: string
}

class DropdownSelect extends Component<DropdownSelectProps, DropdownSelectState> {

    constructor(props: DropdownSelectProps) {
        super(props);
        this.handleOnClick = this.handleOnClick.bind(this)
        console.log(props)

        let selectedElem = '';
        if (this.props.selectedIndex !== undefined
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

    handleOnClick(inputText: string) {
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

export default DropdownSelect;
