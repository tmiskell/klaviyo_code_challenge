class Email( object ):
    def __init__( self, address, subject, body ):
        self._address = address
        self._subject = subject
        self._body = body
    def address( ):
        return self._address
    def subject( ):
        return self._subject
    def body( ):
        return self._body
