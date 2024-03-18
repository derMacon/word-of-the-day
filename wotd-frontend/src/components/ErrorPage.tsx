import React from 'react';
import Container from "react-bootstrap/Container";


export function ErrorPage() {

    // TODO when selecttable in own component, maybe its useful to put the search also in a seperate component
    return (
        <Container fluid="md" className="text-lg-start">
            <h1 className="text-lg-center">Oops something went wrong</h1>
            <h2 className={'text-left'}>We're working on it, please try again later</h2>
        </Container>
    );
}
