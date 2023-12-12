import React, {useEffect, useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import Table from 'react-bootstrap/Table';
import {apiIsHealthy, dictGetAvailableLang} from "../logic/ApiFetcher";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {Option} from "../model/Option";
import './SelectableTable.css';
import {Language} from "../model/Language";
import DropdownSelect from "./DropdownSelect";


interface LanguageSelectProps {
    selectedFromLanguage: Language
    selectedToLanguage: Language

}

export function LanguageSelect(props: LanguageSelectProps) {

    // const [availLang, setAvailLang] = useState<Map<Language, string>>(new Map())
    //
    // // const handleOnClick = (e: React.MouseEvent<HTMLTableRowElement>, selectedOption: Option) => {
    // //     console.log(e)
    // //     // console.log(apiIsHealthy())
    // //     apiIsHealthy().then(e => console.log(selectedOption))
    // // }
    // //
    // // console.log('in table options: ', props.apiResponse.options)
    // //
    // // const items: JSX.Element[] = []
    // // props.apiResponse.options.forEach((option: Option) => items.push(
    // //     <tr onClick={(e: React.MouseEvent<HTMLTableRowElement>) => handleOnClick(e, option)}>
    // //         <td>{option.input}</td>
    // //         <td>{option.output}</td>
    // //     </tr>
    // // ))
    //
    //
    // useEffect(() => {
    //     dictGetAvailableLang().then((languages: Language[]) => {
    //             console.log('languages: ', languages.length)
    //             const langMap: Map<Language, string> = new Map<Language, string>()
    //             for (let i = 0; i < languages.length; i++) {
    //                 langMap.set(languages[i], languages[i].toString())
    //             }
    //             setAvailLang(langMap)
    //         }
    //     )
    // }, []);
    //
    //
    // return (
    //     <>
    //         <DropdownSelect
    //             selectedElem={props.selectedFromLanguage}
    //             onSelect={props.selectedToLanguage}>
    //             {availLang}
    //         </DropdownSelect>
    //         <DropdownSelect
    //             selectedElem={selectedToLang}
    //             onSelect={setSelectedToLang}>
    //             {availLang}
    //         </DropdownSelect>
    //     </>
    // );
}
