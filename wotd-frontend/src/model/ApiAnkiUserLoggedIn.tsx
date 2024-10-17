import {Expose} from "class-transformer";

export class ApiAnkiUserLoggedIn {

    @Expose({name: 'anki_user_logged_in'})
    private _ankiUserLoggedIn?: boolean


    constructor(ankiUserLoggedIn: boolean) {
        this._ankiUserLoggedIn = ankiUserLoggedIn;
    }

    get ankiUserLoggedIn(): boolean {
        return this._ankiUserLoggedIn || false;
    }

    set ankiUserLoggedIn(value: boolean) {
        this._ankiUserLoggedIn = value;
    }
}
