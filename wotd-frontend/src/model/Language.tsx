import {Expose} from "class-transformer";

export class Language {

    @Expose({name: 'enchant_key'})
    private _enchant_key: string

    @Expose({name: 'language_uuid'})
    private _language_uuid: string

    @Expose({name: 'full_name'})
    private _full_name: string


    // constructor(language_uuid: string, full_name: string) {
    //     this._enchant_key = '';
    //     this._language_uuid = language_uuid;
    //     this._full_name = full_name;
    // }


    constructor(enchant_key: string, language_uuid: string, full_name: string) {
        this._enchant_key = enchant_key;
        this._language_uuid = language_uuid;
        this._full_name = full_name;
    }

    get enchant_key(): string {
        return this._enchant_key;
    }

    set enchant_key(value: string) {
        this._enchant_key = value;
    }

    get language_uuid(): string {
        return this._language_uuid;
    }

    set language_uuid(value: string) {
        this._language_uuid = value;
    }

    get full_name(): string {
        return this._full_name;
    }

    set full_name(value: string) {
        this._full_name = value;
    }
}
