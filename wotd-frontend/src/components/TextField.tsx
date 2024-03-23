import React, {useRef, useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";
import Overlay from 'react-bootstrap/Overlay';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';
import {ButtonGroup, Col, Row} from "react-bootstrap";


interface TextFieldProps {
    onSubmit: (input: string) => void
    onType: (input: string) => void
    type?: string
    placeholder?: string
}

export function TextField(props: TextFieldProps) {

    const inputRef = useRef<HTMLInputElement | null>(null);
    const [input, setInput] = useState('')
    const [show, setShow] = useState(false);


    const handleKeyDown = (e: any) => {
        if (e.code === 'Enter' || e.which === 13) {
            const output = e.target.value;
            props.onSubmit(output);
            inputRef.current!.blur()
            // src: https://stackoverflow.com/questions/11845371/window-scrollto-is-not-working-in-mobile-phones
            setTimeout(() => window.scrollTo(0, 0), 100);
        }
    }

    const handleOnClear = (e: React.MouseEvent<HTMLElement, MouseEvent>) => {
        setInput('')
        inputRef.current!.focus();
    }

    const handleInputChange = (e: any) => {
        setInput(e.target.value)
        setShow(true)
    }

    const options = [
        {id: 1, name: 'Apple'},
        {id: 2, name: 'Banana'},
        {id: 3, name: 'Orange'},
        // Add more options as needed
    ];

    const testList = <div className='w-100'>
        <div className="w-100 bg-primary mx-0">
            <Container fluid="md">

                <div className="custom-max-width">
                    {/*<div className="custom-max-width bg-white debugborder" >*/}
                    <Row>
                        <Col xs={12} md={7} className='px-1 pe-3 pe-md-2'>
                            {/*<div className='debugborder'>*/}
                            {/*    test*/}
                            {/*</div>*/}
                            <ListGroup variant="flush">
                                <ListGroup.Item>Cras justo odio</ListGroup.Item>
                                <ListGroup.Item>Dapibus ac facilisis in</ListGroup.Item>
                                <ListGroup.Item>Morbi leo risus</ListGroup.Item>
                                <ListGroup.Item>Porta ac consectetur ac</ListGroup.Item>
                                <ListGroup.Item>Vestibulum at eros</ListGroup.Item>
                            </ListGroup>
                        </Col>
                    </Row>
                </div>
            </Container>
        </div>
    </div>
    // <Row>
    //     <Col>
    {/*<Col xs={12} md={7} className='pe-md-1 pb-2'>*/
    }

    {/*
    }
    <div className='debugborderpurple w-100'>test</div>
    {/*    <Button>test</Button>*/
    }
    // </Col>
    // </Row>

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

            <Overlay target={inputRef} show={show} placement="bottom-start">
                {testList}
            </Overlay>
        </div>
    );
}

export default TextField;
