import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from 'react-bootstrap/Container';
import ItemInput from "./components/ItemInput";

function App() {
    return (
        <div className="App">
            <Container fluid="md">
                <ItemInput onSubmit={output => console.log("top level output: ", output)}/>
            </Container>
        </div>
    );
}

export default App;
