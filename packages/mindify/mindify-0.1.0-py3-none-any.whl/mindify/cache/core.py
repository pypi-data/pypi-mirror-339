class Constant(tuple):
    """Pretty display of immutable constant."""

    def __new__(cls, name):
        return tuple.__new__(cls, (name,))

    def __repr__(self):
        return '%s' % self[0]


ENOVAL = Constant('ENOVAL')
