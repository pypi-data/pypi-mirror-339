from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

class Sonar:
    def __init__(self, sonar_url, token):
        self.client = Client(
            transport=RequestsHTTPTransport(
                url=sonar_url,
                headers={
                    'Authorization': 'Bearer ' + token
                }
            )
        )

    def graphql(self, query, variables=None):
        return self.client.execute(gql(query), variable_values=variables)
