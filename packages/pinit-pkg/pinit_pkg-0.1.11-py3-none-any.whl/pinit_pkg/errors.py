class ServerError(Exception):
    pass


class BadRequestError(Exception):
    def message(self):
        return self.args[0]

    def errors(self):
        return [
            {
                'type': error['type'],
                'field': error['loc'][-1] if error['loc'] else None,
                'msg': error['msg'],
            }
            for error in self.args[1]
        ] if self.args[1] is not None else None


class UnsupportedMediaTypeError(Exception):
    pass


class NotFoundError(Exception):
    pass
