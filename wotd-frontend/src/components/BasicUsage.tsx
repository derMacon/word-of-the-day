import React from 'react';
import {FaArrowsRotate, FaCircleInfo, FaCloudArrowUp, FaCloudBolt} from "react-icons/fa6";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";

export function BasicUsage() {

    return (
        <Container fluid="md" className="text-start p-0">

            <p>Click on the icons in the top right corner to execute the following actions</p>

            <ul>
                <li>
                    <FaCloudArrowUp className="mx-1 me-3"/>
                    anki account login status
                </li>
                <li>
                    <FaArrowsRotate className="mx-1 me-3"/>
                    switch languages
                </li>
                <li>
                    <FaCircleInfo className="mx-1 me-3"/>
                    further info / description
                </li>
            </ul>

        </Container>
    );
}
