import React, {useRef, useState} from 'react';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";


interface TextFieldProps {
    onSubmit: (input: string) => void
}

interface TextFieldState {
    input: string
}

export function TextField(props: TextFieldProps) {

    const inputRef = useRef<HTMLInputElement | null>(null);

    const [input, setInput] = useState('')

    const handleKeyDown = (e: any) => {
        console.log(typeof (e))
        if (e.code === 'Enter' || e.which === 13) {
            console.log('user pressed enter, submitting: ', e.target.value);
            const output = e.target.value;
            setInput('')
            props.onSubmit(output);
        } else {
            console.log('target val: ', e.target.value);
        }
    }

    const handleOnClear = (e: React.MouseEvent<HTMLElement, MouseEvent>) => {
        console.log("user cleared input")
        setInput('')
        inputRef.current!.focus();
    }

    const handleInputChange = (e: any) => {
        setInput(e.target.value)
    }

    return (
        <div>
            <InputGroup>
                <Form.Control
                    className="shadow-none"
                    autoFocus
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />
                <InputGroup.Text onClick={handleOnClear}>
                    <FaTimes/>
                </InputGroup.Text>
            </InputGroup>
        </div>
    );
}

export default TextField;
