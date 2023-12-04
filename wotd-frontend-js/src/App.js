import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Container from 'react-bootstrap/Container';
import TextField from "./components/TextField";
import SelectableTable from "./components/SelectableTable";
import DropdownSelect from "./components/DropdownSelect";
import DictMask from "./components/DictMask";

function App() {
    return (
        <div className="App">
            <DictMask/>
        </div>
    );
}

export default App;
