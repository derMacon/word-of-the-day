import {Language} from "./Language";

export class DictRequest {
    private readonly _fromLanguage: Language
    private readonly _toLanguage: Language
    private readonly _input: string

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
}
