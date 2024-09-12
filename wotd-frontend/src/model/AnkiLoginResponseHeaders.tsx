import {Expose} from "class-transformer";

export class AnkiLoginResponseHeaders {

    @Expose({name: 'username'})
    private _signedUsername: string

    @Expose({name: 'uuid'})
    private _signedUuid: string


    constructor(signedUsername: string, signedUuid: string) {
        this._signedUsername = signedUsername;
        this._signedUuid = signedUuid;
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

}
