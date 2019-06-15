from graphene import Schema
from adapter.gql.query.query import Query
from adapter.gql.mutation.mutation import MutationC

schema = Schema (
    query = Query,
    mutation = MutationC,
    auto_camelcase = False
)

