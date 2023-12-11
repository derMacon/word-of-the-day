// TODO read this from props or some kind .ini, do not hardcode it
import {Language} from "../data/Language";

const HTTP_STATUS_OK: number = 200

const SERVER_ADDRESS: string = 'http://localhost:5000'
export const API_BASE: string = SERVER_ADDRESS + '/api/v1'
export const DICTIONARY_BASE: string = API_BASE + '/dict'

const HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language): Promise<string[]> {

    let json = JSON.stringify({
        input: word,
        from_language: fromLanguage,
        to_language: toLanguage
    })

    try {

        let out = await fetch(DICTIONARY_BASE + '/lookup-option', {
            method: 'POST',
            headers: HEADERS,
            body: json
        })

        console.log('awaiting response: ', await out.json())

        // .then(data => {
        //     console.log("inside lookup: ", data.body)
        //     if (!data.ok) {
        //         alert(data.statusText)
        //     }
        // })
        // .catch(error => console.log(error))
    } catch(error) {
        console.error(error)
    }

    return ['test']
}

export async function dictGetAvailableLang(): Promise<Language[]> {

    try {

        let out = await fetch(DICTIONARY_BASE + '/available-lang', {
            method: 'GET',
            headers: HEADERS,
        })

        let data: Language[] = await out.json()
        console.log('awaiting response: ', data)
        return data

    } catch(error) {
        console.error(error)
        return []
    }
}

export async function apiIsHealthy(): Promise<boolean> {
    try {
        return (await fetch(API_BASE + '/health')).ok
    } catch (error) {
        return false
    }
}
