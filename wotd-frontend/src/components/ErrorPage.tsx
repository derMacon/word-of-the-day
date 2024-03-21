import React from 'react';


export function ErrorPage() {

    // TODO when selecttable in own component, maybe its useful to put the search also in a seperate component
    return (
        <div className="py-5">
            <h1 className="text-lg-center">Oops something went wrong</h1>
            <h2 className={'text-left'}>We're working on it, please try again later</h2>
        </div>
    );
}
