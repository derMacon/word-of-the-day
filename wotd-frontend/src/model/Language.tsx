import {Expose} from "class-transformer";
import {LanguageUUID} from "./LanguageUUID";

export class Language {

    @Expose({name: 'language_uuid'})
    private _language_uuid: LanguageUUID

    @Expose({name: 'name'})
    private _name: string

    constructor(
        languageUUID: LanguageUUID,
        name: string
    ) {
        this._language_uuid = languageUUID
        this._name = name
    }


    get language_uuid(): LanguageUUID {
        return this._language_uuid;
    }

    get name(): string {
        return this._name;
    }


    set language_uuid(value: LanguageUUID) {
        this._language_uuid = value;
    }

    set name(value: string) {
        this._name = value;
    }
}
