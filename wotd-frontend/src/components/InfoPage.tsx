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
                <Offcanvas.Body style={{maxHeight: '95vh', overflowY: 'auto'}}>

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
                        <li>
                            Enter anki web credentials in order to sync generated flash cards with your anki account
                        </li>
                        <li>
                            Select the source and target language for the translation.
                        </li>
                        <li>
                            Type in the word which should be translated
                        </li>
                        <li>
                            Optional: select a word which should be generated to serve as a flashcard in anki
                        </li>
                        <li>
                            Learn stack in anki <a href="https://ankiweb.net/about">web</a>, <a
                            href="https://apps.ankiweb.net/">desktop</a> or <a
                            href="https://play.google.com/store/apps/details?id=com.ichi2.anki&hl=de">mobile</a> client
                        </li>
                    </ol>

                    <p>
                        To get started click <a href=''>here</a>.
                    </p>

                    <h3 className='mt-4'>Enter Anki Credentials</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-4'>Select Languages</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-3'>Type Input</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-3'>Optional: Select Word</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-3'>Synchronize with Anki Web</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-3'>Visit Anki Web to see new vocabularies</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h3 className='mt-3'>Visit Anki client to see new vocabularies</h3>
                    <img
                        src="https://cdn.glitch.com/0e4d1ff3-5897-47c5-9711-d026c01539b8%2Fbddfd6e4434f42662b009295c9bab86e.gif?v=1573157191712"
                        alt="this slowpoke moves" className='w-75'/>

                    <h2 className='mt-4'>Code</h2>
                    <p>The source code for this project is available on <a
                        href='https://gitlab.com/s.hoffmann/projects/programming/msc/word-of-the-day'>gitlab</a>.
                    </p>

                    <div className='custom-margin-bottom-small'/>

                </Offcanvas.Body>
            </div>
        </Container>
    );
}
