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

const HTTP_STATUS_OK: number = 200

const SERVER_ADDRESS: string = 'http://192.168.178.187:5000'
export const API_BASE: string = SERVER_ADDRESS + '/api/v1'
export const DICTIONARY_BASE: string = API_BASE + '/dict'

const HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


export async function dictLookupWord(word: string, fromLanguage: Language, toLanguage: Language): Promise<DictOptionsResponse> {

    let input: DictRequest = new DictRequest(getPrincipal(), fromLanguage.language_uuid, toLanguage.language_uuid, word)
    console.log('dict lookup input: ', JSON.stringify(instanceToPlain(input)))

    try {

        let output = await fetch(DICTIONARY_BASE + '/lookup-option', {
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

export async function pushSelectedOption(dictOptionsItemId: number) {
    console.log('pushing selected option: ', dictOptionsItemId)

    // TODO create / use special type

    let json = JSON.stringify({
        selected_dict_options_item_id: dictOptionsItemId
    })

    let out = await fetch(DICTIONARY_BASE + '/select-option', {
        method: 'POST',
        headers: HEADERS,
        body: json
    })

    let jsonObject: Object = await out.json() as Object
    console.log("select out: ", jsonObject)
}
