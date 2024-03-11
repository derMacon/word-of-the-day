import {Expose} from "class-transformer";

export class AnkiLoginRequest {

    @Expose({name: 'username'})
    private _username: string

    @Expose({name: 'password'})
    private _password: string


    constructor(
        username: string,
        password: string
    ) {
        this._username = username
        this._password = password
    }

    get username(): string {
        return this._username;
    }

    set username(value: string) {
        this._username = value;
    }

    get password(): string {
        return this._password;
    }

    set password(value: string) {
        this._password = value;
    }
}
