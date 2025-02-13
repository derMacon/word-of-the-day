import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import {JSX} from 'react/jsx-runtime';
import {ButtonGroup} from "react-bootstrap";
import {Language} from "../model/Language";


interface DropdownSelectProps {
    availableLanguages: Language[]
    selectedElem: Language
    onSelect: (input: Language) => void
}

export function LanguageSelect(props: Readonly<DropdownSelectProps>) {

    const items: JSX.Element[] = []
    props.availableLanguages.forEach((language: Language) => items.push(
        <Dropdown.Item key={language.language_uuid} onClick={() => props.onSelect(language)}>
            {language.full_name}
        </Dropdown.Item>
    ));

    console.log('props in lang select: ', props.selectedElem)

    const title: string = props.selectedElem.language_uuid

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

export default LanguageSelect;
