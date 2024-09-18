import React, {useState} from 'react';
// import 'bootstrap/dist/css/bootstrap.min.css'
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ListGroup from 'react-bootstrap/ListGroup';

import Offcanvas from 'react-bootstrap/Offcanvas';


export function Trainer() {

    const GRAY_LIGHT: any = {
        backgroundColor: "#f3f3f3",
        // borderColor: "white"
    }

    const GRAY_MIDDLE: any = {
        backgroundColor: "#9d9d9d",
        // borderColor: "white"
    }

    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        // TODO delete this
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


        <div className='custom-min-height'>

            {/*<Navbar expand="lg" className="bg-body-tertiary">*/}
            {/*    <Container>*/}
            {/*        <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>*/}
            {/*        <Navbar.Toggle aria-controls="basic-navbar-nav"/>*/}
            {/*        <Navbar.Collapse id="basic-navbar-nav">*/}
            {/*            <Nav className="me-auto">*/}
            {/*                <Nav.Link href="#home">Home</Nav.Link>*/}
            {/*                <Nav.Link href="#link">Link</Nav.Link>*/}
            {/*                <NavDropdown title="Dropdown" id="basic-nav-dropdown">*/}
            {/*                    <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>*/}
            {/*                    <NavDropdown.Item href="#action/3.2">*/}
            {/*                        Another action*/}
            {/*                    </NavDropdown.Item>*/}
            {/*                    <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>*/}
            {/*                    <NavDropdown.Divider/>*/}
            {/*                    <NavDropdown.Item href="#action/3.4">*/}
            {/*                        Separated link*/}
            {/*                    </NavDropdown.Item>*/}
            {/*                </NavDropdown>*/}
            {/*            </Nav>*/}
            {/*        </Navbar.Collapse>*/}
            {/*    </Container>*/}
            {/*</Navbar>*/}

            <div className="custom-max-width">


                <div className="card d-flex flex-column custom-min-height">


                    <div
                        onClick={handleShow}
                        style={GRAY_MIDDLE}
                        className="text-sm-start px-3 py-2">
                        Launch test deck
                    </div>

                    {/*<hr className="my-0"/>*/}

                    <div className="px-1 progress">25</div>

                    <ButtonGroup size="sm" className="px-1" style={GRAY_LIGHT}>
                        <div className="px-1 text-decoration-underline text-xs">25</div>
                        <div className="px-1 text-decoration-underline">54</div>
                        {/*<div className="px-1 text-decoration-underlinexs">54</div>*/}
                        {/*<div className="px-1 text-decoration-underlinexs">184</div>*/}
                    </ButtonGroup>

                    {/*<ButtonGroup size="sm">*/}
                    {/*    <Button>Left</Button>*/}
                    {/*    <Button>Middle</Button>*/}
                    {/*    <Button>Right</Button>*/}
                    {/*</ButtonGroup>*/}

                    {/*<hr className="my-0"/>*/}

                    {/*<div className="d-flex justify-content-center align-items-center flex-grow-1">*/}
                    {/*    Front*/}
                    {/*</div>*/}

                    <div>Front</div>

                    <hr className="my-1 mx-2"/>

                    <div className="d-flex justify-content-center flex-grow-1">
                        Back
                    </div>

                    {/*<div>Front</div>*/}

                    <hr className='my-0'/>

                    <div>
                        <ButtonGroup className="w-100" aria-label="Basic example">
                            <Button>Very Hard</Button>
                            <Button variant="light text-muted">Hard</Button>
                            <Button variant="light text-muted">Easy</Button>
                            <Button variant="light text-muted">Very Easy</Button>
                        </ButtonGroup>
                    </div>

                </div>
            </div>


            <Offcanvas show={show} onHide={handleClose} className="w-100">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Offcanvas</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>

                    <p>Explanation: asdf asdf a sdf asdf asd fsad f sadf asdf asd fasd f asdf sdf</p>

                    <br/>
                    <p>Input</p>
                    <ListGroup>
                        <ListGroup.Item>Dictionary</ListGroup.Item>
                        <ListGroup.Item disabled>Duden</ListGroup.Item>
                    </ListGroup>

                    <br/>

                    <p>Word Vaults</p>
                    <ListGroup>
                        <ListGroup.Item>English Dictionary</ListGroup.Item>
                        <ListGroup.Item disabled>German Duden Definitions</ListGroup.Item>
                    </ListGroup>

                </Offcanvas.Body>
            </Offcanvas>

        </div>


    );
}
