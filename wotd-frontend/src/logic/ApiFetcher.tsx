// TODO read this from props or some kind .ini, do not hardcode it
import {Language} from "../model/Language";
import {InfoRequestAvailLang} from "../model/InfoRequestAvailLang";
import {plainToClass} from "class-transformer";
import {DictOptionsResponse} from "../model/DictOptionsResponse";
import {DictRequest} from "../model/DictRequest";
import {Option} from "../model/Option";
import {type} from "os";

const HTTP_STATUS_OK: number = 200

const SERVER_ADDRESS: string = 'http://192.168.178.187:5000'
export const API_BASE: string = SERVER_ADDRESS + '/api/v1'
export const DICTIONARY_BASE: string = API_BASE + '/dict'

const HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language): Promise<DictOptionsResponse> {

    // TODO use special type instead of json

    let json = JSON.stringify({
        input: word,
        from_language_uuid: fromLanguage,
        to_language_uuid: toLanguage
    })

    let out = await fetch(DICTIONARY_BASE + '/lookup-option', {
        method: 'POST',
        headers: HEADERS,
        body: json
    })

    let jsonObject: Object = await out.json() as Object

    let requestWrapper: DictOptionsResponse = plainToClass(DictOptionsResponse, jsonObject)
    let originalRequest = plainToClass(DictRequest, requestWrapper.dictRequest)

    requestWrapper.dictRequest = originalRequest

    // console.log('parsed options: ', requestWrapper)
    // console.log('parsed request: ', originalRequest)

    return requestWrapper
}

export async function dictGetAvailableLang(): Promise<Language[]> {

    try {

        let out = await fetch(DICTIONARY_BASE + '/available-lang', {
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

export async function apiIsHealthy(): Promise<boolean> {
    try {
        return (await fetch(API_BASE + '/health')).ok
    } catch (error) {
        return false
    }
}

export async function pushSelectedOption(batchId: number, option: Option) {
    console.log('pushing selected option: ', option)

    // TODO create / use special type

    let json = JSON.stringify({
        options_response_id: batchId,
        selected_option_id: option.id
    })

    let out = await fetch(DICTIONARY_BASE + '/select-option', {
        method: 'POST',
        headers: HEADERS,
        body: json
    })

    let jsonObject: Object = await out.json() as Object
    console.log("select out: ", jsonObject)
}
