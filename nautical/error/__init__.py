'''
The module contains the custom exception used in this package.
In the event of an error generated by this package,
the user should except NauticalError.
'''


class NauticalError(Exception):
    """
    Exception raised as errors occur in the nautical package.
    """
