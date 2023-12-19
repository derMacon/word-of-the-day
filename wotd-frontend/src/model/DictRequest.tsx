import {Language} from "./Language";
import {Expose} from "class-transformer";
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

export class DictRequest {

    @Expose({name: 'from_language_uuid'})
    private _fromLanguageUuid: Language

    @Expose({name: 'to_language_uuid'})
    private _toLanguageUuid: Language

    @Expose({name: 'input'})
    private _input: string

    constructor(
        fromLanguage: Language,
        toLanguage: Language,
        input: string
    ) {
        this._fromLanguageUuid = fromLanguage
        this._toLanguageUuid = toLanguage
        this._input = input
    }


    get fromLanguageUuid(): Language {
        return this._fromLanguageUuid;
    }

    get toLanguageUuid(): Language {
        return this._toLanguageUuid;
    }

    get input(): string {
        return this._input;
    }

    set fromLanguageUuid(value: Language) {
        this._fromLanguageUuid = value;
    }

    set toLanguageUuid(value: Language) {
        this._toLanguageUuid = value;
    }

    set input(value: string) {
        this._input = value;
    }
}
