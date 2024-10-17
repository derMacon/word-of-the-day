import {Expose} from "class-transformer";

// TODO insert backend api status
export class ApiHealthInformation {

    @Expose({name: 'anki_api_connection'})
    private _ankiApiConnection?: boolean

    @Expose({name: 'db_connection'})
    private _dbConnection?: boolean

    @Expose({name: 'wotd_api_connection'})
    private _wotdApiConnection?: boolean

    constructor(
        ankiApiConnection?: boolean,
        dbConnection?: boolean,
        wotdApiConnection?: boolean
    ) {
        this._ankiApiConnection = ankiApiConnection;
        this._dbConnection = dbConnection;
        this._wotdApiConnection = wotdApiConnection;
    }


    get ankiApiConnection(): boolean {
        return this._ankiApiConnection || true;
    }

    set ankiApiConnection(value: boolean) {
        this._ankiApiConnection = value;
    }

    get dbConnection(): boolean {
        return this._dbConnection || false;
    }

    set dbConnection(value: boolean) {
        this._dbConnection = value;
    }

    get wotdApiConnection(): boolean {
        return this._wotdApiConnection || false;
    }

    set wotdApiConnection(value: boolean) {
        this._wotdApiConnection = value;
    }

    static createInvalidStatus(): ApiHealthInformation {
        return new ApiHealthInformation(false, false, false)
    }


}
