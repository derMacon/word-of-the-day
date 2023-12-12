import {Language} from "./Language";

export class InfoRequestAvailLang {
    private _dict_available_languages: Language[]

    constructor(
        dictAvailableLanguages: Language[],
    ) {
        this._dict_available_languages = dictAvailableLanguages
    }


    set dict_available_languages(value: Language[]) {
        this._dict_available_languages = value;
    }

    get dict_available_languages(): Language[] {
        return this._dict_available_languages;
    }
}
