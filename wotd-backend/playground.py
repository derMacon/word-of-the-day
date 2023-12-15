class Test(object):

    def __init__(self, msg: str):
        self.msg = msg

    def _decorator(foo):
        def magic( self ) :
            print("start magic")
            foo( self )
            print("end magic")
        return magic

    @_decorator
    def bar( self ) :
        print(f"normal call: {self.msg}")

test = Test('testtest')

test.bar()