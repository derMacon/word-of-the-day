// TODO read this from props or some kind .ini, do not hardcode it
import {InfoRequestAvailLang} from "../model/InfoRequestAvailLang";
import {instanceToPlain, plainToClass} from "class-transformer";
import {DictRequest} from "../model/DictRequest";
import {Language} from "../model/Language";
import {getPrincipal} from "./AuthService";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {AnkiLoginRequest} from "../model/AnkiLoginRequest";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";

const HTTP_STATUS_OK: number = 200

const WOTD_BACKEND_SERVER_ADDRESS: string = 'http://192.168.178.187:5000'
export const WOTD_API_BASE: string = WOTD_BACKEND_SERVER_ADDRESS + '/api/v1'
export const WOTD_ANKI_DOMAIN: string = WOTD_API_BASE + '/anki'
export const WOTD_DICTIONARY_BASE: string = WOTD_API_BASE + '/dict'


// TODO clean up communication with anki api only through wotd backend - delete info here
const ANKI_API_SERVER_ADDRESS: string = 'http://192.168.178.187:4000'
export const ANKI_API_BASE: string = ANKI_API_SERVER_ADDRESS + '/api/v1'


const DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


// ------------------- WOTD ------------------- //

// TODO fix header param type
export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language, headers: any | undefined): Promise<DictOptionsItem[]> {

    let input: DictRequest = new DictRequest(getPrincipal(), fromLanguage.language_uuid, toLanguage.language_uuid, word)
    console.log('headers: ', headers)
    console.log('dict lookup input: ', JSON.stringify(instanceToPlain(input)))

    try {

        // TODO insert auth headers

        let output = await fetch(WOTD_DICTIONARY_BASE + '/lookup-option', {
            method: 'POST',
            headers: headers || DEFAULT_HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        })

        let out: DictOptionsItem[] = plainToClass(DictOptionsItem, await output.json())
        return out

    } catch (error) {
        console.error(error)
        throw error
    }
}

export async function dictGetAvailableLang(): Promise<Language[]> {

    try {

        let out = await fetch(WOTD_DICTIONARY_BASE + '/available-lang', {
            method: 'GET',
            headers: DEFAULT_HEADERS,
        })

        let jsonObject: Object = await out.json() as Object
        let requestWrapper: InfoRequestAvailLang = plainToClass(InfoRequestAvailLang, jsonObject)

        return requestWrapper.dictAvailableLanguages

    } catch (error) {
        console.error(error)
        return []
    }
}

export async function wotdApiIsHealthy(): Promise<boolean> {
    try {
        return (await fetch(WOTD_API_BASE + '/health')).ok
    } catch (error) {
        return false
    }
}

export async function toggleSelectedOption(dictOptionsItemId: number): Promise<void> {
    console.log('toggle selected option: ', dictOptionsItemId)

    // TODO create / use special type

    let json: string = JSON.stringify({
        selected_dict_options_item_id: dictOptionsItemId
    })

    let response: Response = await fetch(WOTD_DICTIONARY_BASE + '/select-option', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: json
    })

    let jsonObject: Object = await response.json() as Object
    console.log("select out: ", jsonObject)
}


// ------------------- Anki API ------------------- //

export async function ankiApiLogin(email: string, password: string): Promise<AnkiLoginResponseHeaders | undefined> {
    try {

        let input: AnkiLoginRequest = new AnkiLoginRequest(email, password)
        console.log('anki login request: ', JSON.stringify(instanceToPlain(input)))

        let out: Response = (await fetch(WOTD_ANKI_DOMAIN + '/login', {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        }))

        const mainTokenKey: string = 'main-token'
        const cardTokenKey: string = 'card-token'
        const responseHeaders: Headers = out.headers;

        if (!out.ok || !responseHeaders.has(mainTokenKey) || !responseHeaders.has(cardTokenKey)) {
            console.log('invalid credentials')
            return undefined
        }

        const ankiResponseHeaders: AnkiLoginResponseHeaders = new AnkiLoginResponseHeaders(
            responseHeaders.get(mainTokenKey)!,
            responseHeaders.get(cardTokenKey)!
        )

        console.log('anki response headers: ', ankiResponseHeaders)
        return ankiResponseHeaders

    } catch (error) {
        console.log('anki api is not reachable')
        return undefined
    }
}

export async function ankiApiIsHealthy(): Promise<boolean> {
    try {
        return (await fetch(ANKI_API_BASE + '/health')).ok
    } catch (error) {
        console.log('anki api is not reachable')
        return false
    }
}

