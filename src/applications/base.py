def transaction(func):
    def wrapper(self, *args, **kwargs):
        with self.session.begin():
            return func(self, *args, **kwargs)

    return wrapper
