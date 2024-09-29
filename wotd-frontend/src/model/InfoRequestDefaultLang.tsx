import {Expose} from "class-transformer";
import {Language} from "./Language";

export class InfoRequestDefaultLang {

    @Expose({name: 'dict_default_from_language'})
    private _dictDefaultFromLanguage: Language

    @Expose({name: 'dict_default_to_language'})
    private _dictDefaultToLanguage: Language


    constructor(dictDefaultFromLanguage: Language, dictDefaultToLanguage: Language) {
        this._dictDefaultFromLanguage = dictDefaultFromLanguage;
        this._dictDefaultToLanguage = dictDefaultToLanguage;
    }


    get dictDefaultFromLanguage(): Language {
        return this._dictDefaultFromLanguage;
    }

    set dictDefaultFromLanguage(value: Language) {
        this._dictDefaultFromLanguage = value;
    }

    get dictDefaultToLanguage(): Language {
        return this._dictDefaultToLanguage;
    }

    set dictDefaultToLanguage(value: Language) {
        this._dictDefaultToLanguage = value;
    }

}
