import React, {useRef, useState} from 'react';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css'
import InputGroup from 'react-bootstrap/InputGroup';
import {FaTimes} from "react-icons/fa";


interface TextFieldProps {
    onSubmit: (input: string) => void
    type?: string
    placeholder?: string
}

export function TextField(props: TextFieldProps) {

    const inputRef = useRef<HTMLInputElement | null>(null);
    const [input, setInput] = useState('')


    const handleKeyDown = (e: any) => {
        if (e.code === 'Enter' || e.which === 13) {
            const output = e.target.value;
            props.onSubmit(output);
            inputRef.current!.blur()
            // src: https://stackoverflow.com/questions/11845371/window-scrollto-is-not-working-in-mobile-phones
            setTimeout(() => window.scrollTo(0, 0), 100);
        }
    }

    const handleOnClear = (e: React.MouseEvent<HTMLElement, MouseEvent>) => {
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
                    type={props.type || 'text'}
                    placeholder={props.placeholder || ''}
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
