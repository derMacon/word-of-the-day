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

    @Expose({name: 'selected'})
    private _selected: boolean


    constructor(
        dictOptionsItemId: number,
        dictOptionsResponseId: number,
        input: string,
        output: string,
        selected: boolean
    ) {
        this._dictOptionsItemId = dictOptionsItemId;
        this._dictOptionsResponseId = dictOptionsResponseId;
        this._input = input;
        this._output = output;
        this._selected = selected
    }


    get dictOptionsItemId(): number {
        return this._dictOptionsItemId;
    }

    set dictOptionsItemId(value: number) {
        this._dictOptionsItemId = value;
    }

    get dictOptionsResponseId(): number {
        return this._dictOptionsResponseId;
    }

    set dictOptionsResponseId(value: number) {
        this._dictOptionsResponseId = value;
    }

    get input(): string {
        return this._input;
    }

    set input(value: string) {
        this._input = value;
    }

    get output(): string {
        return this._output;
    }

    set output(value: string) {
        this._output = value;
    }

    get selected(): boolean {
        return this._selected;
    }

    set selected(value: boolean) {
        this._selected = value;
    }
}
