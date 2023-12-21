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
        // <div>
        //     <div className="custom-max-width custom-min-height">
        //
        //         <div className="card d-flex flex-column custom-min-height">
        //             <div>
        //                 <p>This is the second child div.</p>
        //             </div>
        //
        //             <ListGroup variant="flush" className='flex-grow-1'>
        //                 <ListGroup.Item className='flex-grow-1 vertical-center' style={{
        //                     // margin: 'auto'
        //                 }}>
        //                     {/*<div className='align-midle debugborderpurple' style={{height: '100px'}}>*/}
        //                         Front
        //                     {/*</div>*/}
        //                 </ListGroup.Item>
        //                 <ListGroup.Item className='flex-grow-1'>Back</ListGroup.Item>
        //             </ListGroup>
        //
        //             <div className="">
        //                 <ButtonGroup className='w-100' aria-label="Basic example">
        //                     <Button variant="light text-muted">Very Hard</Button>
        //                     <Button variant="light text-muted">Hard</Button>
        //                     <Button variant="light text-muted">Easy</Button>
        //                     <Button variant="light text-muted">Very Easy</Button>
        //                 </ButtonGroup>
        //             </div>
        //         </div>
        //
        //     </div>
        // </div>


        <div>
            <div className="custom-max-width custom-min-height">
                <div className="card d-flex flex-column custom-min-height">
                    <div>
                        <p>This is the second child div.</p>
                    </div>
                    <hr className="my-1"/>

                    <div className="d-flex justify-content-center align-items-center flex-grow-1">
                        Front
                    </div>

                    <hr className="my-1 mx-2"/>

                    <div className="d-flex justify-content-center align-items-center flex-grow-1">
                        Back
                    </div>

                    <hr className='my-0'/>

                    <div>
                        <ButtonGroup className="w-100" aria-label="Basic example">
                            <Button variant="light text-muted">Very Hard</Button>
                            <Button variant="light text-muted">Hard</Button>
                            <Button variant="light text-muted">Easy</Button>
                            <Button variant="light text-muted">Very Easy</Button>
                        </ButtonGroup>
                    </div>

                </div>
            </div>
        </div>


    );
}
