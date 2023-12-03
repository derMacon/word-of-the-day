import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from 'react-bootstrap/Container';
import ItemInput from "./components/ItemInput";

function App() {
    return (
        <div className="App">
            <Container fluid="md">
                <div className='my-3 shadow bg-white rounded border-1'>
                    <ItemInput onSubmit={output => console.log("top level output: ", output)}/>
                </div>
            </Container>
        </div>
    );
}

export default App;
