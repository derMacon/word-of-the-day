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

    let json = JSON.stringify({
        input: word,
        from_language: fromLanguage,
        to_language: toLanguage
    })

    // try {

    let out = await fetch(DICTIONARY_BASE + '/lookup-option', {
        method: 'POST',
        headers: HEADERS,
        body: json
    })

    let jsonObject: Object = await out.json() as Object

    console.log('awaiting response: ', jsonObject)
    let requestWrapper: DictOptionsResponse = plainToClass(DictOptionsResponse, jsonObject)
    let originalRequest = plainToClass(DictRequest, requestWrapper.dictRequest)

    // let tmp: Option[] = requestWrapper.options.map<Option>(value => plainToClass(Option, value))
    // console.log('---- tmp: ', typeof tmp[0])
    // let options = plainToClass(Option[], requestWrapper.options)

    requestWrapper.dictRequest = originalRequest

    console.log('parsed options: ', requestWrapper)
    console.log('parsed request: ', originalRequest)

    return requestWrapper

    // } catch (error) {
    //     console.error(error)
    // }

    // return new DictOptionsResponse(-1, undefined, )
}

export async function dictGetAvailableLang(): Promise<Language[]> {

    try {

        let out = await fetch(DICTIONARY_BASE + '/available-lang', {
            method: 'GET',
            headers: HEADERS,
        })

        let jsonObject: Object = await out.json() as Object
        let requestWrapper: InfoRequestAvailLang = plainToClass(InfoRequestAvailLang, jsonObject)
        console.log('json resp: ', jsonObject)
        console.log('request wrapper: ', requestWrapper)
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
