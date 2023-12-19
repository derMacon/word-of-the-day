import {Expose} from "class-transformer";
import {DictRequest} from "./DictRequest";
import {Status} from "./Status";
import {DictOptionsItem} from "./DictOptionsItem";

export class DictOptionsResponse {

    @Expose({name: 'dict_options_response_id'})
    private _dictOptionsResponseId: number

    @Expose({name: 'dict_request'})
    private _dictRequest: DictRequest

    private _status: Status

    private _options: DictOptionsItem[]

    @Expose({name: 'options_request_ts'})
    private _optionsResponseTs: string


    constructor(dictOptionsResponseId: number, dictRequest: DictRequest, status: Status, options: DictOptionsItem[], optionsResponseTs: string) {
        this._dictOptionsResponseId = dictOptionsResponseId;
        this._dictRequest = dictRequest;
        this._status = status;
        this._options = options;
        this._optionsResponseTs = optionsResponseTs;
    }


    get dictOptionsResponseId(): number {
        return this._dictOptionsResponseId;
    }

    set dictOptionsResponseId(value: number) {
        this._dictOptionsResponseId = value;
    }

    get dictRequest(): DictRequest {
        return this._dictRequest;
    }

    set dictRequest(value: DictRequest) {
        this._dictRequest = value;
    }

    get status(): Status {
        return this._status;
    }

    set status(value: Status) {
        this._status = value;
    }

    get options(): DictOptionsItem[] {
        return this._options;
    }

    set options(value: DictOptionsItem[]) {
        this._options = value;
    }

    get optionsResponseTs(): string {
        return this._optionsResponseTs;
    }

    set optionsResponseTs(value: string) {
        this._optionsResponseTs = value;
    }
}
