export class Option {

    private _id: number
    private _input: string
    private _output: string

    constructor(
        id: number,
        input: string,
        output: string
    ) {
        this._id = id
        this._input = input
        this._output = output
    }

    get id(): number {
        return this._id;
    }

    get input(): string {
        return this._input;
    }

    get output(): string {
        return this._output;
    }

    set id(value: number) {
        this._id = value;
    }

    set input(value: string) {
        this._input = value;
    }

    set output(value: string) {
        this._output = value;
    }
}
