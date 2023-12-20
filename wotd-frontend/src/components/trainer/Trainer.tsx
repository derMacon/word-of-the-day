import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Card from 'react-bootstrap/Card';
import {Col, Row} from "react-bootstrap";
import ListGroup from 'react-bootstrap/ListGroup';
import Stack from 'react-bootstrap/Stack';


export function Trainer() {


    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width custom-min-height">

                    <div className="card d-flex flex-column" style={{height: '500px'}}>
                        <div>
                            <p>This is the second child div.</p>
                        </div>
                        <ListGroup variant="flush" className='flex-grow-1'>
                            <ListGroup.Item className='flex-grow-1'>Front</ListGroup.Item>
                            <ListGroup.Item className='flex-grow-1'>Back</ListGroup.Item>
                        </ListGroup>
                        <div className="">
                            <ButtonGroup className='w-100' aria-label="Basic example">
                                <Button variant="light text-muted">Very Hard</Button>
                                <Button variant="light text-muted">Hard</Button>
                                <Button variant="light text-muted">Easy</Button>
                                <Button variant="light text-muted">Very Easy</Button>
                            </ButtonGroup>
                        </div>
                    </div>

                </div>

            </Container>
        </div>
    );
}
