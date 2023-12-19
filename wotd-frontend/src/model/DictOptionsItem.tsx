import {Expose} from "class-transformer";


export class DictOptionsItem {

    @Expose({name: 'dict_options_item_id'})
    private _dictOptionsItemId: number

    @Expose({name: 'dict_options_response_id'})
    private _dictOptionsResponseId: number

    @Expose({name: 'input'})
    private _input: string

    @Expose({name: 'output'})
    private _output: string


    constructor(
        dictOptionsItemId: number,
        dictOptionsResponseId: number,
        input: string,
        output: string
    ) {
        this._dictOptionsItemId = dictOptionsItemId;
        this._dictOptionsResponseId = dictOptionsResponseId;
        this._input = input;
        this._output = output;
    }


    get dictOptionsItemId(): number {
        return this._dictOptionsItemId;
    }

    get dictOptionsResponseId(): number {
        return this._dictOptionsResponseId;
    }

    get input(): string {
        return this._input;
    }

    get output(): string {
        return this._output;
    }


    set dictOptionsItemId(value: number) {
        this._dictOptionsItemId = value;
    }

    set dictOptionsResponseId(value: number) {
        this._dictOptionsResponseId = value;
    }

    set input(value: string) {
        this._input = value;
    }

    set output(value: string) {
        this._output = value;
    }
}
