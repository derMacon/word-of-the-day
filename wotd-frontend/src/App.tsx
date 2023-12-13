import React, {useEffect} from 'react';
import './App.css';
import {apiIsHealthy} from "./logic/ApiFetcher";
import {DictMask} from "./components/DictMask";

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
        </div>
    );
}

export default App;
