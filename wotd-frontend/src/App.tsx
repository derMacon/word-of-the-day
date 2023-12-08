import React, {useEffect} from 'react';
import './App.css';
import DictMask from "./components/DictMask";
import {apiIsHealthy} from "./logic/ApiFetcher";

function App() {

    useEffect(() => {
        apiIsHealthy().then(isHealthy => {
                if (isHealthy) {
                    console.log('API available')
                } else {
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
