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
                <div className="custom-max-width custom-min-height debugborderpurple">

                    {/*<div className="flexitem">test1</div>*/}
                    {/*<div className="flexitem">test2</div>*/}

                    {/*/!*<Card border='dark' className='flexcontainer'>*!/*/}
                    {/*    <ListGroup variant="flush" className=''>*/}
                    {/*        <ListGroup.Item className='flexitem'>Front</ListGroup.Item>*/}
                    {/*        <ListGroup.Item>Back</ListGroup.Item>*/}
                    {/*    </ListGroup>*/}


                    {/*    <div className='min-height'>*/}
                    {/*        <ButtonGroup className='w-100' aria-label="Basic example">*/}
                    {/*            <Button variant="light text-muted">Very Hard</Button>*/}
                    {/*            <Button variant="light text-muted">Hard</Button>*/}
                    {/*            <Button variant="light text-muted">Easy</Button>*/}
                    {/*            <Button variant="light text-muted">Very Easy</Button>*/}
                    {/*        </ButtonGroup>*/}
                    {/*    </div>*/}
                    {/*/!*</Card>*!/*/}

                    {/*<Stack direction="vertical" className="debugbordergreen h-100" gap={3}>*/}
                    {/*    <div className="debugbordergreen">First item</div>*/}
                    {/*    <div className="debugborderpurple mh-100">Second item</div>*/}
                    {/*    <div className="vr"/>*/}
                    {/*    <div className="debugborderpurple">Third item</div>*/}
                    {/*</Stack>*/}

                    {/*<div className='debugborder '>*/}
                    {/*    /!*<div className='debugborder d-flex flex-column'>*!/*/}
                    {/*    <div className='debugborderpurple flexitem'>1</div>*/}
                    {/*    <div>2</div>*/}
                    {/*</div>*/}

                    <div className="d-flex flex-column" style={{height: '500px'}}>
                        <div className="" style={{height: '30px', backgroundColor: 'lightcoral'}}>
                            {/* Content for the second child div goes here */}
                            <p>This is the second child div.</p>
                        </div>
                        <div className="flex-grow-1" style={{backgroundColor: 'lightblue'}}>
                            {/* Content for the first child div goes here */}
                            <p>This is the first child div.</p>
                        </div>
                        {/* Second Child Div */}
                        <div className="" style={{backgroundColor: 'lightcoral'}}>
                            {/* Content for the second child div goes here */}
                            {/*<p>This is the second child div.</p>*/}

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
