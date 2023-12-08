// TODO read this from props or some kind .ini, do not hardcode it
const HTTP_STATUS_OK: number = 200

const SERVER_ADDRESS: string = 'http://localhost:5000'
export const API_BASE: string = SERVER_ADDRESS + '/api/v1'
export const DICTIONARY_BASE: string = API_BASE + '/dict'


export function dictLookupWord(word: string): string {
    fetch(API_BASE + '/health')
        .then(data => console.log(data))
        .catch(error => console.log(error))

    return 'test'
}

export async function apiIsHealthy(): Promise<boolean> {
    try {
        return (await fetch(API_BASE + '/health')).ok
    } catch (error) {
        return false
    }
}

dictLookupWord('test')
