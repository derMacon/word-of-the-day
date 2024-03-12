import Cookies from 'universal-cookie';
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";

export function getPrincipal(): string {
    // TODO
    return 'test-user'
}


export class AuthService {

    readonly EMAIL_COOKIE_KEY: string = 'anki-email'
    readonly MAIN_TOKEN_COOKIE_KEY: string = 'main-token'
    readonly CARD_TOKEN_COOKIE_KEY: string = 'card-token'

    private _email: string;
    private _mainToken: string;
    private _cardToken: string;
    private _cookies: Cookies;


    constructor() {
        this._cookies = new Cookies(null, {path: '/'})
        this._email = this._cookies.get(this.EMAIL_COOKIE_KEY) ?? ''
        this._mainToken = this._cookies.get(this.MAIN_TOKEN_COOKIE_KEY) ?? '';
        this._cardToken = this._cookies.get(this.CARD_TOKEN_COOKIE_KEY) ?? '';
    }

    get email(): string {
        return this._email;
    }

    set email(value: string) {
        this._email = value;
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

    userIsLoggedIn() {
        return this._email != ''
            && this._mainToken != ''
            && this._cardToken != ''
    }

    cleanCookies() {
        this._cookies.remove(this.EMAIL_COOKIE_KEY)
        this._cookies.remove(this.MAIN_TOKEN_COOKIE_KEY)
        this._cookies.remove(this.CARD_TOKEN_COOKIE_KEY)
    }


    loadAnkiLoginResponse(email: string, response: AnkiLoginResponseHeaders): void {
        this._email = email
        this._mainToken = response.mainToken
        this._cardToken = response.cardToken
        this.setCookie()
    }

    setCookie() {
        this._cookies.set(this.EMAIL_COOKIE_KEY, this._email);
        this._cookies.set(this.MAIN_TOKEN_COOKIE_KEY, this._mainToken);
        this._cookies.set(this.CARD_TOKEN_COOKIE_KEY, this._cardToken);
    }

    toString() {
        return `{email: ${this.email}, main-token: ${this.mainToken}, card-token: ${this.cardToken}}`
    }

}