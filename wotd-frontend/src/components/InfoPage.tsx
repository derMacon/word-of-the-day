import React from 'react';
import Container from "react-bootstrap/Container";
import Offcanvas from "react-bootstrap/Offcanvas";
import './InfoPage.css'


export function InfoPage() {

    return (
        <Container fluid="md">
            <div className="custom-max-width">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title></Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body style={{ maxHeight: '95vh', overflowY: 'auto' }}>

                    <h1 className="text-lg-center">Word of the day</h1>
                    <h2 className={'text-left'}>Description</h2>
                    <p className="text-justify">This online dictionary leverages the api of <a
                        href="https://www.dict.cc/">dict.cc</a> to
                        translate a
                        given input word. The webapp then saves this request to a flash card for the user to learn later
                        on.
                        The flash card app in use is currently anki (see their <a
                            href="https://apps.ankiweb.net/">website</a>). Anki provides a mobile client as well as a
                        webinterface which the user can interact with and learn previous requested translations.</p>
                    <p>The webapp also provides the possiblity to select other options other than the default
                        translation
                        for the generated flashcards.</p>

                    <h2>Usage</h2>
                    <ol>
                        <li>enter anki web credentials in order to sync generated flash cards with your anki account
                        </li>
                        <li>select the source and target language for the translation (if both are equal we&#39;ll
                            simply
                            return a definition of the input word)
                        </li>
                        <li>type in the word which should be translated</li>
                        <li>Optional: select a word which should be generated to serve as a flashcard in anki</li>
                        <li>learn stack in anki <a href="https://ankiweb.net/about">web</a> or <a
                            href="https://apps.ankiweb.net/">client</a></li>
                    </ol>

                    <h2>Code</h2>
                    <p>The source code for this project is available on <a
                        href='https://gitlab.com/s.hoffmann/projects/programming/msc/word-of-the-day'>gitlab</a>.
                    </p>

                    <div className='custom-margin-bottom-small'/>

                </Offcanvas.Body>
            </div>
        </Container>
    );
}
