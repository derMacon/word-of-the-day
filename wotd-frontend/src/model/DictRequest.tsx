import {LanguageUUID} from "./LanguageUUID";
import {Expose} from "class-transformer";
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

export class DictRequest {

    @Expose({name: 'from_language_uuid'})
    private _fromLanguageUuid: LanguageUUID

    @Expose({name: 'to_language_uuid'})
    private _toLanguageUuid: LanguageUUID

    @Expose({name: 'input'})
    private _input: string

    constructor(
        fromLanguage: LanguageUUID,
        toLanguage: LanguageUUID,
        input: string
    ) {
        this._fromLanguageUuid = fromLanguage
        this._toLanguageUuid = toLanguage
        this._input = input
    }


    get fromLanguageUuid(): LanguageUUID {
        return this._fromLanguageUuid;
    }

    get toLanguageUuid(): LanguageUUID {
        return this._toLanguageUuid;
    }

    get input(): string {
        return this._input;
    }

    set fromLanguageUuid(value: LanguageUUID) {
        this._fromLanguageUuid = value;
    }

    set toLanguageUuid(value: LanguageUUID) {
        this._toLanguageUuid = value;
    }

    set input(value: string) {
        this._input = value;
    }
}
