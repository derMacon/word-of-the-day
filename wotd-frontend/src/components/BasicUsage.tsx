import React from 'react';
import {FaArrowsRotate, FaCloudBolt, FaCloudArrowUp} from "react-icons/fa6";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import {Button, ButtonGroup, Col, Row} from "react-bootstrap";
import LanguageSelect from "./LanguageSelect";
import {Language} from "../model/Language";
import DropdownButton from 'react-bootstrap/DropdownButton';
import { FaCircleInfo } from "react-icons/fa6";

export function BasicUsage() {

    return (
        <Container fluid="md" className="text-lg-start p-0">

            <p>Click on the icons in the top right corner to execute the following actions</p>

            <Table striped bordered hover className='table-fixed'>
                <tbody>
                <tr>
                    <td className='w-50'>
                        <FaCloudArrowUp className="mx-1"/>
                        <FaCloudBolt className="mx-1"/>
                    </td>
                    <td className='w-50'>click to see anki account login status</td>
                </tr>
                <tr>
                    <td className='w-50'>
                        <FaArrowsRotate className="mx-1"/>
                    </td>
                    <td className='w-50'>switch languages</td>
                </tr>
                <tr>
                    <td className='w-50'>
                        <FaCircleInfo className="mx-1"/>
                    </td>
                    <td className='w-50'>further info / description</td>
                </tr>
                </tbody>
            </Table>

        </Container>
    );
}
