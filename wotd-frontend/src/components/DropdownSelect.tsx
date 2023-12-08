import React, {Component, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';


interface DropdownSelectProps {
    children: string[]
    selectedIndex?: number
    onSelect: (input: string) => void
}

export function DropdownSelect(props: DropdownSelectProps) {

    const [selectedElem, setSelectedElem] = useState<string>(() => {
        let defaultSelectedElem: string = '';
        if (
            props.selectedIndex !== undefined &&
            props.selectedIndex >= 0 &&
            props.selectedIndex < props.children.length
        ) {
            defaultSelectedElem = props.children[props.selectedIndex];
        } else {
            console.log('not able to preselect element in dropdown');
        }
        return defaultSelectedElem;
    });

    const handleOnClick = (inputText: string) => {
        setSelectedElem(inputText);
        props.onSelect(inputText);
    }


    const items = props.children.map((item, index) => (
        <Dropdown.Item key={index} onClick={() => handleOnClick(item)}>
            {item}
        </Dropdown.Item>
    ));

    return (
        <DropdownButton title={selectedElem}>
            {items}
        </DropdownButton>
    );
}

export default DropdownSelect;
