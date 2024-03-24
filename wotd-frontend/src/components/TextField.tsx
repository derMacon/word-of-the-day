import './TextField.css'
import React, {useEffect, useRef, useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";
import Overlay from 'react-bootstrap/Overlay';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';
import {ButtonGroup, Col, Row} from "react-bootstrap";
import {socket} from "../logic/ApiFetcher";
import {initSocket} from "../logic/SocketFetcher";


interface TextFieldProps {
    onSubmit: (input: string) => void
    onType: (input: string) => void
    type?: string
    placeholder?: string
}

export function TextField(props: TextFieldProps) {

    const inputRef = useRef<HTMLInputElement | null>(null);
    const [input, setInput] = useState('')
    const [showAutocompleteOptions, setShowAutocompleteOptions] = useState(false);
    const [options, setOptions] = useState<string[]>([])

    const setOptionsHandleShow = (input: string[]) => {
        setOptions(input)
        setShowAutocompleteOptions(true)
    }

    useEffect(() => initSocket(setOptionsHandleShow), []);

    const handleKeyDown = (e: any) => {
        if (e.code === 'Enter' || e.which === 13) {
            const output = e.target.value;
            props.onSubmit(output);
            setShowAutocompleteOptions(false)
            inputRef.current!.blur()
            // src: https://stackoverflow.com/questions/11845371/window-scrollto-is-not-working-in-mobile-phones
            setTimeout(() => window.scrollTo(0, 0), 100);
        }
    }

    const handleOnClear = (e: React.MouseEvent<HTMLElement, MouseEvent>) => {
        setInput('')
        inputRef.current!.focus();
        setShowAutocompleteOptions(false)
    }

    const handleInputChange = (e: any) => {
        setInput(e.target.value)
        props.onType(e.target.value)
        // setShowAutocompleteOptions(true)
    }


    const handleAutocompleteSelection = (word: string) => {
        setInput(word)
        props.onSubmit(word)
        setShowAutocompleteOptions(false)
    }

    const generateItems = () => {
        let items: JSX.Element[] = [];
        options.forEach((elem: string) => items.push(
            <ListGroup.Item
                onClick={(e) => handleAutocompleteSelection(elem)}
                className="custom-list-group-item">
                {elem}
            </ListGroup.Item>
        ))
        return items
    }

    const autocompleteOptions = <div className='w-100'>
        <div className="w-100 bg-white mx-0">
            <Container fluid="md">
                <div className="custom-max-width">
                    <Row>
                        <Col xs={12} md={7} className='px-1 pe-3 pe-md-2'>
                            <ListGroup variant="flush">
                                {generateItems()}
                            </ListGroup>
                            <div className="custom-margin-bottom"/>
                        </Col>
                    </Row>
                </div>
            </Container>
        </div>
    </div>

    return (
        <div>
            <InputGroup>
                <Form.Control
                    className="shadow-none"
                    autoFocus
                    ref={inputRef}
                    type={props.type || 'text'}
                    placeholder={props.placeholder || ''}
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />
                <InputGroup.Text onClick={handleOnClear}>
                    <FaTimes/>
                </InputGroup.Text>
            </InputGroup>

            <Overlay target={inputRef} show={showAutocompleteOptions} placement="bottom-start">
                {autocompleteOptions}
            </Overlay>
        </div>
    );
}

export default TextField;
