import {Expose} from "class-transformer";
import {OptionStatus} from "./OptionStatus";
import {Simulate} from "react-dom/test-utils";


export class DictOptionsItem {

    @Expose({name: 'dict_options_item_id'})
    private _dictOptionsItemId: number

    @Expose({name: 'deck'})
    private _deck: string

    @Expose({name: 'input'})
    private _input: string

    @Expose({name: 'output'})
    private _output: string

    @Expose({name: 'selected'})
    private _selected: boolean

    @Expose({name: 'status'})
    private _status: OptionStatus

    @Expose({name: 'options_response_ts'})
    private _optionsResponseTs: string


    constructor(dictOptionsItemId: number, deck: string, input: string, output: string, selected: boolean, status: OptionStatus, optionsResponseTs: string) {
        this._dictOptionsItemId = dictOptionsItemId;
        this._deck = deck;
        this._input = input;
        this._output = output;
        this._selected = selected;
        this._status = status;
        this._optionsResponseTs = optionsResponseTs;
    }

    get dictOptionsItemId(): number {
        return this._dictOptionsItemId;
    }

    set dictOptionsItemId(value: number) {
        this._dictOptionsItemId = value;
    }

    get deck(): string {
        return this._deck;
    }

    set deck(value: string) {
        this._deck = value;
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

    get status(): OptionStatus {
        return this._status;
    }

    set status(value: OptionStatus) {
        this._status = value;
    }

    get optionsResponseTs(): string {
        return this._optionsResponseTs;
    }

    set optionsResponseTs(value: string) {
        this._optionsResponseTs = value;
    }
}
