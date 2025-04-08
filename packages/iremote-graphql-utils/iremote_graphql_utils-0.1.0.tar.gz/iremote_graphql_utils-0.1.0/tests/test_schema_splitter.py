import unittest
from graphql_utils import SchemaSplitter


class TestSchemaSplitter(unittest.TestCase):
    def test_parse_schema(self):
        schema = """
        type Query {
            hello: String
        }
        """
        document = SchemaSplitter.parse_schema(schema)
        self.assertIsNotNone(document)
        self.assertEqual(document.kind, "document")
        self.assertEqual(len(document.definitions), 1)
        self.assertEqual(document.definitions[0].kind, "object_type_definition")
        self.assertEqual(document.definitions[0].name.value, "Query")

    def test_format_schema(self):
        schema = """type Query{hello:String}"""
        document = SchemaSplitter.parse_schema(schema)
        formatted_schema = SchemaSplitter.format_schema(document)
        self.assertEqual(formatted_schema.strip(), "type Query {\n  hello: String\n}")

    def test_get_named_type(self):
        schema = """
        type User {
            id: ID!
            name: String
            friends: [User!]
        }
        """
        document = SchemaSplitter.parse_schema(schema)
        user_type_def = next(d for d in document.definitions if d.name.value == "User")
        id_field = next(f for f in user_type_def.fields if f.name.value == "id")
        name_field = next(f for f in user_type_def.fields if f.name.value == "name")
        friends_field = next(
            f for f in user_type_def.fields if f.name.value == "friends"
        )

        self.assertEqual(SchemaSplitter.get_named_type(id_field.type.type), "ID")
        self.assertEqual(SchemaSplitter.get_named_type(name_field.type), "String")
        self.assertEqual(
            SchemaSplitter.get_named_type(friends_field.type.type.type), "User"
        )

    def test_extract_dependent_types_simple(self):
        schema = """
        type Query {
            user: User
        }
        type User {
            id: ID!
        }
        """
        document = SchemaSplitter.parse_schema(schema)
        type_definitions = {
            defn.name.value: defn
            for defn in document.definitions
            if defn.kind
            in (
                "object_type_definition",
                "input_object_type_definition",
                "enum_type_definition",
            )
        }
        query_type = type_definitions["Query"]
        user_field = next(f for f in query_type.fields if f.name.value == "user")
        dependent_types = SchemaSplitter.extract_dependent_types(
            user_field, type_definitions
        )
        self.assertEqual(dependent_types, {"User"})

    def test_extract_dependent_types_nested(self):
        schema = """
        type Query {
            profile: ProfileInfo
        }
        type ProfileInfo {
            user: User
        }
        type User {
            id: ID!
            address: Address
        }
        type Address {
            street: String
            city: String
        }
        """
        document = SchemaSplitter.parse_schema(schema)
        type_definitions = {
            defn.name.value: defn
            for defn in document.definitions
            if defn.kind
            in (
                "object_type_definition",
                "input_object_type_definition",
                "enum_type_definition",
            )
        }
        query_type = type_definitions["Query"]
        profile_field = next(f for f in query_type.fields if f.name.value == "profile")
        dependent_types = SchemaSplitter.extract_dependent_types(
            profile_field, type_definitions
        )
        self.assertEqual(dependent_types, {"ProfileInfo", "User", "Address"})

    def test_extract_dependent_types_input_object(self):
        schema = """
        type Mutation {
            createUser(input: UserInput): User
        }
        input UserInput {
            name: String!
            address: AddressInput
        }
        input AddressInput {
            street: String
            city: String
        }
        type User {
            id: ID!
            name: String!
        }
        """
        document = SchemaSplitter.parse_schema(schema)
        type_definitions = {
            defn.name.value: defn
            for defn in document.definitions
            if defn.kind
            in (
                "object_type_definition",
                "input_object_type_definition",
                "enum_type_definition",
            )
        }
        mutation_type = type_definitions["Mutation"]
        create_user_field = next(
            f for f in mutation_type.fields if f.name.value == "createUser"
        )
        dependent_types = SchemaSplitter.extract_dependent_types(
            create_user_field, type_definitions
        )
        self.assertEqual(dependent_types, {"UserInput", "AddressInput", "User"})

    def test_split_schema_query_simple(self):
        schema = """
        type Query {
            hello: String
        }
        """
        sub_graphs = SchemaSplitter.split_schema(schema)
        self.assertEqual(len(sub_graphs), 1)
        self.assertEqual(
            sub_graphs[0].strip(),
            "schema { query: Query }\n\ntype Query { hello(): String }",
        )

    def test_split_schema_mutation_simple(self):
        schema = """
        type Mutation {
            createUser: User
        }
        type User {
            id: ID!
        }
        """
        sub_graphs = SchemaSplitter.split_schema(schema)
        self.assertEqual(len(sub_graphs), 1)
        expected = """schema { mutation: Mutation }\n\ntype Mutation { createUser(): User }\n\ntype User {\n  id: ID!\n}"""
        self.assertEqual(sub_graphs[0].strip(), expected.strip())
