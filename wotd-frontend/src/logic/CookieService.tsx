import Cookies from 'universal-cookie';
import {AnkiLoginResponseHeaders} from "../model/AnkiLoginResponseHeaders";


export class CookieService {

    readonly PLAIN_EMAIL_COOKIE_KEY: string = 'plain-email'
    readonly UNSIGNED_EMAIL_COOKIE_KEY: string = 'X-Wotd-Username'
    readonly UNSIGNED_UUID_COOKIE_KEY: string = 'X-Wotd-Uuid'
    readonly IGNORE_LOGIN_PROMPT_COOKIE_KEY: string = 'ignore-login-prompt'
    readonly FIRST_TIME_USER_COOKIE_KEY: string = 'FIRST-TIME-USER'

    private _plainUsername: string;
    private _signedUsername: string;
    private _signedUuid: string;
    private _ignoreLoginPrompt: boolean;
    private _firstTimeUser: boolean;
    private _cookies: Cookies;


    constructor() {
        this._cookies = new Cookies(null, {path: '/'})
        this._plainUsername = this._cookies.get(this.PLAIN_EMAIL_COOKIE_KEY) ?? ''
        this._signedUsername = this._cookies.get(this.UNSIGNED_EMAIL_COOKIE_KEY) ?? ''
        this._signedUuid = this._cookies.get(this.UNSIGNED_UUID_COOKIE_KEY) ?? '';
        this._firstTimeUser = this._cookies.get(this.FIRST_TIME_USER_COOKIE_KEY) ?? true;
        this._ignoreLoginPrompt = this._cookies.get(this.IGNORE_LOGIN_PROMPT_COOKIE_KEY) ?? false;
    }


    get plainUsername(): string {
        return this._plainUsername;
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

    set plainUsername(value: string) {
        this._plainUsername = value;
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

    get firstTimeUser(): boolean {
        return this._firstTimeUser;
    }

    set firstTimeUser(value: boolean) {
        this._firstTimeUser = value;
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

    cleanAllCookies(
        reload: boolean = true,
        value_exceptions: string[] = [this.FIRST_TIME_USER_COOKIE_KEY, this.IGNORE_LOGIN_PROMPT_COOKIE_KEY]
    ): void {
        let allCookies = this._cookies.getAll();

        Object.keys(allCookies).forEach(cookieName => {
            if (!value_exceptions.includes(cookieName)) {
                this._cookies.remove(cookieName);
            }
        });

        if (reload) {
            window.location.reload();
        }
    }


    loadAnkiLoginResponse(response: AnkiLoginResponseHeaders): void {
        this._signedUsername = response.signedUsername
        this._signedUuid = response.signedUuid
        this.setCookies()
    }

    setCookies() {
        if (this._plainUsername != null && this._plainUsername.length > 0) {
            this._cookies.set(this.PLAIN_EMAIL_COOKIE_KEY, this._plainUsername);
        }
        if (this._signedUsername != null && this._signedUsername.length > 0) {
            this._cookies.set(this.UNSIGNED_EMAIL_COOKIE_KEY, this._signedUsername);
        }
        if (this._signedUuid != null && this._signedUuid.length > 0) {
            this._cookies.set(this.UNSIGNED_UUID_COOKIE_KEY, this._signedUuid);
        }
        if (this._firstTimeUser != null) {
            this._cookies.set(this.FIRST_TIME_USER_COOKIE_KEY, this._firstTimeUser);
        }
        this.writeIgnoreLoginPromptCookie()
    }

    getHeaders() {
        const out: { [key: string]: string } = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if (this._signedUuid != null && this._signedUuid.length > 0) {
            out[this.UNSIGNED_UUID_COOKIE_KEY] = this._signedUuid
        }
        if (this._signedUsername != null && this._signedUsername.length > 0) {
            out[this.UNSIGNED_EMAIL_COOKIE_KEY] = this._signedUsername
        }
        return out
    }

    toString() {
        return `{signed-username: ${this.signedUsername}, signed-uuid: ${this.signedUuid}}`
    }

}