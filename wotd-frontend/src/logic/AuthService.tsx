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

    get cookies(): Cookies {
        return this._cookies;
    }

    set cookies(value: Cookies) {
        this._cookies = value;
    }

    userIsLoggedIn() {
        return this._email != ''
            && this._mainToken != ''
            && this._cardToken != ''
    }

    cleanCookies() {
        let allCookies = this._cookies.getAll();
        Object.keys(allCookies).forEach(cookieName => {
            this._cookies.remove(cookieName);
        });
        window.location.reload();
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

    getHeaders() {
        const out: { [key: string]: string } = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        out[this.MAIN_TOKEN_COOKIE_KEY] = this._mainToken
        out[this.CARD_TOKEN_COOKIE_KEY] = this._cardToken
        out[this.EMAIL_COOKIE_KEY] = this._email
        return out
    }

    toString() {
        return `{email: ${this.email}, main-token: ${this.mainToken}, card-token: ${this.cardToken}}`
    }

}