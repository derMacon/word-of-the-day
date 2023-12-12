import {Language} from "./Language";
import {Expose} from "class-transformer";
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

export class DictRequest {

    @Expose({name: 'from_language'})
    private _fromLanguage: Language

    @Expose({name: 'to_language'})
    private _toLanguage: Language

    private _input: string

    constructor(
        fromLanguage: Language,
        toLanguage: Language,
        input: string
    ) {
        this._fromLanguage = fromLanguage
        this._toLanguage = toLanguage
        this._input = input
    }


    get fromLanguage(): Language {
        return this._fromLanguage;
    }

    get toLanguage(): Language {
        return this._toLanguage;
    }

    get input(): string {
        return this._input;
    }

    set fromLanguage(value: Language) {
        this._fromLanguage = value;
    }

    set toLanguage(value: Language) {
        this._toLanguage = value;
    }

    set input(value: string) {
        this._input = value;
    }
}
