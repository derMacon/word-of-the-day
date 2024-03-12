import {Expose} from "class-transformer";

export class AnkiLoginResponseHeaders {

    @Expose({name: 'main_token'})
    private _mainToken: string

    @Expose({name: 'card_token'})
    private _cardToken: string


    constructor(mainToken: string, cardToken: string) {
        this._mainToken = mainToken;
        this._cardToken = cardToken;
    }


    get mainToken(): string {
        return this._mainToken;
    }

    set mainToken(value: string) {
        this._mainToken = value;
    }

    get cardToken(): string {
        return this._cardToken;
    }

    set cardToken(value: string) {
        this._cardToken = value;
    }

}
