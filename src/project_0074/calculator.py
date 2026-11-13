class Calculator:
    '''Simple arithmetic calculator.'''

    def add(self, a, b):
        '''Return the sum of a and b.'''
        return a + b

    def subtract(self, a, b):
        '''Return the difference of a and b.'''
        return a - b

    def multiply(self, a, b):
        '''Return the product of a and b.'''
        return a * b

    def divide(self, a, b):
        '''Return the division of a by b. Raises ZeroDivisionError if b is zero.'''
        if b == 0:
            raise ZeroDivisionError('division by zero')
        return a / b