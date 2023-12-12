import React, {Component, Key, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import {JSX} from 'react/jsx-runtime';
import {ButtonGroup} from "react-bootstrap";


interface DropdownSelectProps<T> {
    children: Map<T, string>
    selectedElem: T
    onSelect: (input: T) => void
}

export function DropdownSelect<T extends Key>(props: DropdownSelectProps<T>) {

    const [selectedElem, setSelectedElem] = useState<T>(props.selectedElem);

    const handleOnClick = (key: T) => {
        setSelectedElem(key);
        props.onSelect(key);
    }


    const items: JSX.Element[] = []
    props.children.forEach((value: string, key: T) => items.push(
        <Dropdown.Item key={key} onClick={() => handleOnClick(key)}>
            {value}
        </Dropdown.Item>
    ));

    return (
        <DropdownButton as={ButtonGroup} title={props.children.get(selectedElem)}>
            {items}
        </DropdownButton>
    );
}

export default DropdownSelect;
