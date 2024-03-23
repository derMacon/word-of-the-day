import Cookies from 'universal-cookie';
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";


export class AuthService {

    readonly EMAIL_COOKIE_KEY: string = 'anki-email'
    readonly MAIN_TOKEN_COOKIE_KEY: string = 'main-token'
    readonly CARD_TOKEN_COOKIE_KEY: string = 'card-token'
    readonly IGNORE_LOGIN_PROMPT_COOKIE_KEY: string = 'ignore-login-prompt'

    private _email: string;
    private _mainToken: string;
    private _cardToken: string;
    private _ignoreLoginPrompt: boolean;
    private _cookies: Cookies;


    constructor() {
        this._cookies = new Cookies(null, {path: '/'})
        this._email = this._cookies.get(this.EMAIL_COOKIE_KEY) ?? ''
        this._mainToken = this._cookies.get(this.MAIN_TOKEN_COOKIE_KEY) ?? '';
        this._cardToken = this._cookies.get(this.CARD_TOKEN_COOKIE_KEY) ?? '';
        this._ignoreLoginPrompt = this._cookies.get(this.IGNORE_LOGIN_PROMPT_COOKIE_KEY) ?? false;
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

    get ignoreLoginPrompt(): boolean {
        return this._ignoreLoginPrompt;
    }

    set ignoreLoginPrompt(value: boolean) {
        this._ignoreLoginPrompt = value;
    }

    get cookies(): Cookies {
        return this._cookies;
    }

    set cookies(value: Cookies) {
        this._cookies = value;
    }

    userIsLoggedIn(): boolean {
        return this._email != ''
            && this._mainToken != ''
            && this._cardToken != ''
    }

    showLoginPrompt(): boolean {
        return !this.userIsLoggedIn()
            && !this.ignoreLoginPrompt
    }

    writeIgnoreLoginPromptCookie(): void {
        this._cookies.set(this.IGNORE_LOGIN_PROMPT_COOKIE_KEY, this._ignoreLoginPrompt);
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
        this.writeIgnoreLoginPromptCookie()
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