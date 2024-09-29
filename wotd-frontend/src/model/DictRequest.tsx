import {Expose} from "class-transformer";
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

export class DictRequest {

    @Expose({name: 'from_language_uuid'})
    private _fromLanguageUuid: string

    @Expose({name: 'to_language_uuid'})
    private _toLanguageUuid: string

    @Expose({name: 'input'})
    private _input: string


    constructor(
        fromLanguage: string,
        toLanguage: string,
        input: string
    ) {
        this._fromLanguageUuid = fromLanguage
        this._toLanguageUuid = toLanguage
        this._input = input
    }


    get fromLanguageUuid(): string {
        return this._fromLanguageUuid;
    }

    set fromLanguageUuid(value: string) {
        this._fromLanguageUuid = value;
    }

    get toLanguageUuid(): string {
        return this._toLanguageUuid;
    }

    set toLanguageUuid(value: string) {
        this._toLanguageUuid = value;
    }

    get input(): string {
        return this._input;
    }

    set input(value: string) {
        this._input = value;
    }
}
