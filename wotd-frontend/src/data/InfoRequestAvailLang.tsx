import {Language} from "./Language";

export class InfoRequestAvailLang {
    private readonly _dictAvailableLanguages: Language[]

    constructor(
        dictAvailableLanguages: Language[],
    ) {
        this._dictAvailableLanguages = dictAvailableLanguages
    }

    get dictAvailableLanguages(): Language[] {
        return this._dictAvailableLanguages;
    }
}
