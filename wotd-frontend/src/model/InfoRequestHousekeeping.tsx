import {Expose} from "class-transformer";
import {Language} from "./Language";

export class InfoRequestHousekeeping {

    @Expose({name: 'next_sync'})
    private _nextSync: string


    constructor(nextSync: string) {
        this._nextSync = nextSync;
    }


    get nextSync(): string {
        return this._nextSync;
    }

    set nextSync(value: string) {
        this._nextSync = value;
    }
}
