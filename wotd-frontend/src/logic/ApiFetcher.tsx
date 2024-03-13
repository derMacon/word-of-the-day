// TODO read this from props or some kind .ini, do not hardcode it
import {LanguageUUID} from "../model/LanguageUUID";
import {InfoRequestAvailLang} from "../model/InfoRequestAvailLang";
import {instanceToPlain, plainToClass, serialize} from "class-transformer";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {DictRequest} from "../model/DictRequest";
import {Option} from "../model/Option";
import {type} from "os";
import {Language} from "../model/Language";
import {getPrincipal} from "./AuthService";
import {DictOptionsItem} from "../model/DictOptionsItem";
import AnkiSyncLogin from "../components/dict_input/AnkiSyncLogin";
import {AnkiLoginRequest} from "../model/AnkiLoginRequest";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";

const HTTP_STATUS_OK: number = 200

const WOTD_BACKEND_SERVER_ADDRESS: string = 'http://192.168.178.187:5000'
export const WOTD_API_BASE: string = WOTD_BACKEND_SERVER_ADDRESS + '/api/v1'
export const WOTD_DICTIONARY_BASE: string = WOTD_API_BASE + '/dict'


const ANKI_API_SERVER_ADDRESS: string = 'http://192.168.178.187:4000'
export const ANKI_API_BASE: string = ANKI_API_SERVER_ADDRESS + '/api/v1'


const HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


// ------------------- WOTD ------------------- //

export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language): Promise<DictOptionsResponse> {

    let input: DictRequest = new DictRequest(getPrincipal(), fromLanguage.language_uuid, toLanguage.language_uuid, word)
    console.log('dict lookup input: ', JSON.stringify(instanceToPlain(input)))

    try {

        let output = await fetch(WOTD_DICTIONARY_BASE + '/lookup-option', {
            method: 'POST',
            headers: HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        })

        let jsonObject: Object = await output.json() as Object

        let requestWrapper: DictOptionsResponse = plainToClass(DictOptionsResponse, jsonObject)
        let originalRequest: DictRequest = plainToClass(DictRequest, requestWrapper.dictRequest)

        let optionsUpdated: DictOptionsItem[] = []
        for (let i = 0; i < requestWrapper.options.length; i++) {
            let curr = requestWrapper.options[i] as Object
            optionsUpdated.push(plainToClass(DictOptionsItem, curr))
        }

        requestWrapper.dictRequest = originalRequest
        requestWrapper.options = optionsUpdated

        // console.log('parsed options: ', requestWrapper)
        // console.log('parsed request: ', originalRequest)

        return requestWrapper

    } catch (error) {
        console.error(error)
        throw error
    }
}

export async function dictGetAvailableLang(): Promise<Language[]> {

    try {

        let out = await fetch(WOTD_DICTIONARY_BASE + '/available-lang', {
            method: 'GET',
            headers: HEADERS,
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
        headers: HEADERS,
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

        let out: Response = (await fetch(ANKI_API_BASE + '/login', {
            method: 'POST',
            headers: HEADERS,
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

