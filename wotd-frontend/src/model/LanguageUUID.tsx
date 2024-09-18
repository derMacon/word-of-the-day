import {Simulate} from "react-dom/test-utils";


export enum LanguageUUID {
    EN = 'EN',
    DE = 'DE'
}

export function convertToLanguageUUIDEnum(str: string | undefined): LanguageUUID | undefined {
    if (str === undefined) {
        return undefined
    }
    return LanguageUUID[str as keyof typeof LanguageUUID];
}
