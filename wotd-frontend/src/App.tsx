import React, {useEffect} from 'react';
import './App.css';
// import 'bootstrap/dist/css/bootstrap.min.css'
import {apiIsHealthy} from "./logic/ApiFetcher";
import {DictMask} from "./components/dict_input/DictMask";
import {Trainer} from "./components/trainer/Trainer";

function App() {

    useEffect(() => {
        apiIsHealthy().then((isHealthy: boolean) => {
                if (!isHealthy) {
                    alert('API not available')
                }
            }
        )
    }, []);


    return (
        <div className="App">
            <DictMask/>
            {/*<Trainer/>*/}
        </div>
    );
}

export default App;
