import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from "react-bootstrap/Container";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Card from 'react-bootstrap/Card';


export function Trainer() {


    return (
        <div>
            <Container fluid="md">
                <div className="custom-max-width min-height">

                    <Card border='light' className=''>
                        <Card.Text className='min-height'>
                            front
                        </Card.Text>

                        <Card.Text className='min-height'>
                            back
                        </Card.Text>


                        <div className=''>
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
