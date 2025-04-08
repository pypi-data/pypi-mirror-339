class QueryNotReady(Exception):
    def __init__(self,
                 query_id,
                 status="PENDING",
                 message='The result is not ready yet. Please call it later to get the result'):
        self.message = message.format(status.lower())
        self.query_id = query_id
        super().__init__(self.message)