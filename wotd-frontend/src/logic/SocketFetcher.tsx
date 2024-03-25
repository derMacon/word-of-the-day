import {Language} from "../model/Language";
import {DictRequest} from "../model/DictRequest";
import {instanceToPlain} from "class-transformer";
import {socket} from "./ApiFetcher";


const AUTOCORRECT_OPTION_COUNT = 8

export function initSocket(
    optionSetter: (autocorrectOptions: string[]) => void
) {

    function onConnect() {
        console.log('connected to socket')
    }

    function onDisconnect() {
        console.log('disconnected from socket')
    }

    function onAutocorrectReceive(options: string[]) {
        options = options.slice(0, AUTOCORRECT_OPTION_COUNT)
        console.log('executing test call: ', options)
        optionSetter(options)
    }

    console.log('before trying to connect')
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('update_autocorrect', onAutocorrectReceive);
    console.log('after trying to connect')

    return () => {
        socket.off('connect', onConnect);
        socket.off('disconnect', onDisconnect);
        socket.off('update_autocorrect', onAutocorrectReceive);
    };
}

export function socketAutocompleteWord(word: string, fromLanguage: Language, toLanguage: Language) {

    let input: DictRequest = new DictRequest(fromLanguage.language_uuid, toLanguage.language_uuid, word)
    let json = JSON.stringify(instanceToPlain(input))
    console.log('dict lookup input: ', json)

    socket.emit('autocomplete-query-event', json, () => {
        console.log('sent autocomplete-query-event')
    })
}
