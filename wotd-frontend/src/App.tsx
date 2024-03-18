import React, {useEffect} from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import {apiHealthStatus} from "./logic/ApiFetcher";
import {DictMask} from "./components/DictMask";
import {Trainer} from "./components/trainer/Trainer";

function App() {

    useEffect(() => {
    }, []);


    return (
        <div className="App">
            <DictMask/>
        </div>
    );
}

export default App;
