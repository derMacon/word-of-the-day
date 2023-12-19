import {LanguageUUID} from "./LanguageUUID";
import {Expose, Type} from "class-transformer";
import {DictRequest} from "./DictRequest";
import {Status} from "./Status";
import {Option} from "./Option";

export class DictOptionsResponse {

    private _id: number

    @Expose({name: 'dict_request'})
    private _dictRequest: DictRequest

    private _status: Status

    private _options: Option[]

    constructor(
        id: number,
        dictRequest: DictRequest,
        status: Status,
        options: Option[]
    ) {
        this._id = id
        this._dictRequest = dictRequest
        this._status = status
        this._options = options
    }

    get id(): number {
        return this._id;
    }

    get dictRequest(): DictRequest {
        return this._dictRequest;
    }

    get status(): Status {
        return this._status;
    }

    get options(): Option[] {
        return this._options;
    }

    set id(value: number) {
        this._id = value;
    }

    set dictRequest(value: DictRequest) {
        this._dictRequest = value;
    }

    set status(value: Status) {
        this._status = value;
    }

    set options(value: Option[]) {
        this._options = value;
    }
}
