import React, {Component} from 'react';
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

class TextField extends Component<TextFieldProps, TextFieldState> {

    private readonly inputRef: React.RefObject<HTMLInputElement>;

    constructor(props: TextFieldProps) {
        super(props);
        this.handleKeyDown = this.handleKeyDown.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleOnClear = this.handleOnClear.bind(this);
        this.inputRef = React.createRef();
        this.state = {
            input: '',
        };
    }

    handleKeyDown(e: any) {
        console.log(typeof (e))
        if (e.code === 'Enter' || e.which === 13) {
            console.log('user pressed enter, submitting: ', e.target.value);
            const output = e.target.value;
            this.setState({input: ''});
            this.props.onSubmit(output);
        } else {
            console.log('target val: ', e.target.value);
        }
    }

    handleOnClear(e: React.MouseEvent<HTMLElement, MouseEvent>) {
        console.log("user cleared input")

        this.setState({input: ''}, () => {
            this.inputRef.current!.focus(); // Set focus after state is updated
        });

    }

    handleInputChange(e: any) {
        this.setState({input: e.target.value});
    }

    render() {

        return (
            <div>
                <InputGroup>
                    <Form.Control
                        className="shadow-none"
                        autoFocus
                        ref={this.inputRef}
                        type="text"
                        value={this.state.input}
                        onChange={this.handleInputChange}
                        onKeyDown={this.handleKeyDown}
                    />
                    <InputGroup.Text onClick={this.handleOnClear}>
                        <FaTimes/>
                    </InputGroup.Text>
                </InputGroup>
            </div>
        );
    }
}

export default TextField;
