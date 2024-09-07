import Cookies from 'universal-cookie';
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";


export class AuthService {

    readonly EMAIL_COOKIE_KEY: string = 'anki-signed-email'
    readonly UUID_COOKIE_KEY: string = 'anki-signed-profile-uuid'
    readonly IGNORE_LOGIN_PROMPT_COOKIE_KEY: string = 'ignore-login-prompt'

    private _signedUsername: string;
    private _signedUuid: string;
    private _ignoreLoginPrompt: boolean;
    private _cookies: Cookies;


    constructor() {
        this._cookies = new Cookies(null, {path: '/'})
        this._signedUsername = this._cookies.get(this.EMAIL_COOKIE_KEY) ?? ''
        this._signedUuid = this._cookies.get(this.UUID_COOKIE_KEY) ?? '';
        this._ignoreLoginPrompt = this._cookies.get(this.IGNORE_LOGIN_PROMPT_COOKIE_KEY) ?? false;
    }


    get signedUsername(): string {
        return this._signedUsername;
    }

    set signedUsername(value: string) {
        this._signedUsername = value;
    }

    get signedUuid(): string {
        return this._signedUuid;
    }

    set signedUuid(value: string) {
        this._signedUuid = value;
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
        return this._signedUsername != ''
            && this._signedUuid != ''
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


    loadAnkiLoginResponse(response: AnkiLoginResponseHeaders): void {
        this._signedUsername = response.signedUsername
        this._signedUuid = response.signedUuid
        this.setCookie()
    }

    setCookie() {
        this._cookies.set(this.EMAIL_COOKIE_KEY, this._signedUsername);
        this._cookies.set(this.UUID_COOKIE_KEY, this._signedUuid);
        this.writeIgnoreLoginPromptCookie()
    }

    getHeaders() {
        const out: { [key: string]: string } = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        out[this.UUID_COOKIE_KEY] = this._signedUuid
        out[this.EMAIL_COOKIE_KEY] = this._signedUsername
        return out
    }

    toString() {
        return `{signed-username: ${this.signedUsername}, signed-uuid: ${this.signedUuid}}`
    }

}