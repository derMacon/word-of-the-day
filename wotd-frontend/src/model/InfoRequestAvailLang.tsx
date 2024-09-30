import {Expose} from "class-transformer";
import {Language} from "./Language";

export class InfoRequestAvailLang {

    @Expose({name: 'dict_available_languages'})
    private _dictAvailableLanguages: Language[]

    constructor(
        dictAvailableLanguages: Language[],
    ) {
        this._dictAvailableLanguages = dictAvailableLanguages
    }

    set dictAvailableLanguages(value: Language[]) {
        this._dictAvailableLanguages = value;
    }

    get dictAvailableLanguages(): Language[] {
        return this._dictAvailableLanguages;
    }
}
