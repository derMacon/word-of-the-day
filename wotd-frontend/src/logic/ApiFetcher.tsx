import {InfoRequestAvailLang} from "../model/InfoRequestAvailLang";
import {instanceToPlain, plainToClass} from "class-transformer";
import {DictRequest} from "../model/DictRequest";
import {Language} from "../model/Language";
import {DictOptionsItem} from "../model/DictOptionsItem";
import {AnkiLoginRequest} from "../model/AnkiLoginRequest";
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";
import {ApiHealthInformation} from "../model/ApiHealthInformation";
import {InfoRequestHousekeeping} from "../model/InfoRequestHousekeeping";
import {ApiAnkiUserLoggedIn} from "../model/ApiAnkiUserLoggedIn";

const WOTD_BACKEND_HOST: string = process.env.REACT_APP_WOTD_BACKEND_HOST || 'localhost'
const WOTD_BACKEND_PORT: string = process.env.REACT_APP_WOTD_BACKEND_PORT || '5000'

export const WOTD_BACKEND_SERVER_ADDRESS: string = 'http://' + WOTD_BACKEND_HOST + ":" + WOTD_BACKEND_PORT
export const WOTD_API_BASE: string = WOTD_BACKEND_SERVER_ADDRESS + '/api/v1'
export const WOTD_ANKI_DOMAIN: string = WOTD_API_BASE + '/anki'
export const WOTD_DICTIONARY_BASE: string = WOTD_API_BASE + '/dict'

console.log('backend address: ', WOTD_BACKEND_SERVER_ADDRESS)

const DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


export async function wotdApiHealthStatus(): Promise<ApiHealthInformation> {
    try {
        let response: Response = await fetch(WOTD_API_BASE + '/health')
        let jsonObject: Object = await response.json() as Object
        let apiHealthInformation: ApiHealthInformation = plainToClass(ApiHealthInformation, jsonObject)
        console.log('api health information: ', apiHealthInformation)
        return apiHealthInformation
    } catch (error) {
        let defaultErrorMsg: string = 'Backend API not available - not possible to lookup words. Please try again later.'
        console.log(defaultErrorMsg)
        return ApiHealthInformation.createInvalidStatus()
    }
}

// TODO fix header param type
export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language, headers: any | undefined): Promise<DictOptionsItem[] | null> {

    let input: DictRequest = new DictRequest(fromLanguage.language_uuid, toLanguage.language_uuid, word)
    console.log('headers: ', headers)
    console.log('dict lookup input: ', JSON.stringify(instanceToPlain(input)))

    try {
        let output: Response = await fetch(WOTD_DICTIONARY_BASE + '/lookup-option', {
            method: 'POST',
            headers: headers || DEFAULT_HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        })

        return plainToClass(DictOptionsItem, await output.json())

    } catch (error) {
        console.error(error)
        alert("Sorry we're having trouble connecting to the background api. Please try again later.")
    }
    return null
}

export async function dictAutocompleteWord(word: string, fromLanguage: Language, toLanguage: Language): Promise<string[]> {

    let input: DictRequest = new DictRequest(fromLanguage.language_uuid, toLanguage.language_uuid, word)
    console.log('dict lookup input: ', JSON.stringify(instanceToPlain(input)))

    try {

        let output = await fetch(WOTD_DICTIONARY_BASE + '/autocomplete-option', {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        })

        return await output.json();

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


export async function dictGetInfoHousekeeping(): Promise<InfoRequestHousekeeping> {

    try {

        let out = await fetch(WOTD_ANKI_DOMAIN + '/housekeeping-info', {
            method: 'GET',
            headers: DEFAULT_HEADERS,
        })

        let jsonObject: Object = await out.json() as Object
        let requestWrapper: InfoRequestHousekeeping = plainToClass(InfoRequestHousekeeping, jsonObject)
        console.log('info housekeeping: ', requestWrapper)
        return requestWrapper

    } catch (error) {
        console.error(error)
        throw error
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


export async function ankiApiLogin(email: string, password: string): Promise<AnkiLoginResponseHeaders | undefined> {
    try {

        let input: AnkiLoginRequest = new AnkiLoginRequest(email, password)
        const url: string = WOTD_ANKI_DOMAIN + '/login'
        console.log('anki login request: ' + input.username + ' - ' + url)

        let out: Response = (await fetch(url, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify(instanceToPlain(input))
        }))

        const signedUsername: string = 'X-Wotd-Username'
        const signedUuid: string = 'X-Wotd-Uuid'
        const responseHeaders: Headers = out.headers;

        console.log('response headers: ', responseHeaders)

        if (!out.ok || !responseHeaders.has(signedUsername) || !responseHeaders.has(signedUuid)) {
            console.log('invalid credentials')
            return undefined
        }

        console.log('valid headers')

        const ankiResponseHeaders: AnkiLoginResponseHeaders = new AnkiLoginResponseHeaders(
            responseHeaders.get(signedUsername)!,
            responseHeaders.get(signedUuid)!
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
        return (await fetch(WOTD_API_BASE + '/health')).ok
    } catch (error) {
        console.log('anki api is not reachable')
        return false
    }
}


// TODO fix param type
export async function ankiApiTriggerManualHousekeeping(auth_headers: any) {
    try {
        let out: Response = (await fetch(WOTD_ANKI_DOMAIN + '/trigger-housekeeping', {
            method: 'GET',
            headers: auth_headers
        }))
        console.log('response triggering manual housekeeping: ', out)

    } catch (error) {
        console.log('cannot trigger manual housekeeping in the backend')
        return false
    }
}

export async function ankiApiUserLoggedIn(auth_headers: any): Promise<ApiAnkiUserLoggedIn> {
    try {
        let out: Response = (await fetch(WOTD_ANKI_DOMAIN + '/user-is-logged-in', {
            method: 'GET',
            headers: auth_headers
        }))
        let jsonObject: Object = await out.json() as Object
        let requestWrapper: ApiAnkiUserLoggedIn = plainToClass(ApiAnkiUserLoggedIn, jsonObject)
        console.log('response to anki user is logged in: ', requestWrapper)
        return requestWrapper
    } catch (error) {
        console.log('cannot get information about the users login status')
        return new ApiAnkiUserLoggedIn(false)
    }
}

