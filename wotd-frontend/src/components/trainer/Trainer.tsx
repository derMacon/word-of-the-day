import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Card from 'react-bootstrap/Card';
import {Col, Row} from "react-bootstrap";
import ListGroup from 'react-bootstrap/ListGroup';


export function Trainer() {


    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width">

                    <Card border='light' className=''>
                        <ListGroup variant="flush">
                            <ListGroup.Item>Front</ListGroup.Item>
                            <ListGroup.Item>Back</ListGroup.Item>
                        </ListGroup>


                        <div className='min-height'>
                            <ButtonGroup className='w-100' aria-label="Basic example">
                                <Button variant="light text-muted">Very Hard</Button>
                                <Button variant="light text-muted">Hard</Button>
                                <Button variant="light text-muted">Easy</Button>
                                <Button variant="light text-muted">Very Easy</Button>
                            </ButtonGroup>
                        </div>
                    </Card>


                </div>

            </Container>
        </div>
    );
}
