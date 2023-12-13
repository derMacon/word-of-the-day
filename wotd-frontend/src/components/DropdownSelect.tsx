import React, {Key} from 'react';
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

    const items: JSX.Element[] = []
    props.children.forEach((value: string, key: T) => items.push(
        <Dropdown.Item key={key} onClick={() => props.onSelect(key)}>
            {value}
        </Dropdown.Item>
    ));

    const title: string = props.children.get(props.selectedElem) || ''

    return (
        <DropdownButton
            as={ButtonGroup}
            variant='light'
            className='w-50'
            title={title}>
            {items}
        </DropdownButton>
    );
}

export default DropdownSelect;
