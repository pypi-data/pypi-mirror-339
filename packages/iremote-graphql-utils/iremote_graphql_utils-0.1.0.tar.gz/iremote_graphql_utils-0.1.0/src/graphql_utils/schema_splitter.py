from __future__ import annotations

from typing import List, Any, Dict, Set

from graphql import parse, print_ast
from graphql.language.ast import (
    DocumentNode,
    ObjectTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    EnumTypeDefinitionNode,
    FieldDefinitionNode,
    NamedTypeNode,
    NonNullTypeNode,
    ListTypeNode,
)


class SchemaSplitter:
    @staticmethod
    def parse_schema(schema: str) -> DocumentNode:
        return parse(schema)

    @staticmethod
    def format_schema(document: DocumentNode) -> str:
        return print_ast(document)

    @staticmethod
    def get_named_type(
        type_node: NamedTypeNode | NonNullTypeNode | ListTypeNode,
    ) -> str:
        if type_node.kind == "named_type":
            return type_node.name.value
        elif type_node.kind == "non_null_type":
            return SchemaSplitter.get_named_type(type_node.type)
        elif type_node.kind == "list_type":
            return SchemaSplitter.get_named_type(type_node.type)
        else:
            raise ValueError(f"Unexpected type node kind: {type_node.kind}")

    @staticmethod
    def extract_dependent_types(
        field: FieldDefinitionNode,
        type_definitions: Dict[
            str,
            ObjectTypeDefinitionNode
            | InputObjectTypeDefinitionNode
            | EnumTypeDefinitionNode,
        ],
        visited: Set[str] = None,
    ) -> Set[str]:
        """
        Extracts all dependent types (input and output) for a given field, including transitive dependencies.
        """
        if visited is None:
            visited = set()

        dependent_types = set()

        # Get the named type of the field (e.g., UserInput or User)
        try:
            dep_type = SchemaSplitter.get_named_type(field.type)
        except ValueError:
            return dependent_types  # Skip if the field type is unexpected

        # Avoid re-processing types that have already been visited
        if dep_type in visited:
            return dependent_types

        visited.add(dep_type)

        # Add the type to the dependent types if it exists in type_definitions
        if dep_type in type_definitions:
            dependent_types.add(dep_type)
            type_def = type_definitions[dep_type]

            # Handle ObjectTypeDefinitionNode and InputObjectTypeDefinitionNode
            if isinstance(
                type_def, (ObjectTypeDefinitionNode, InputObjectTypeDefinitionNode)
            ):
                fields_to_process = type_def.fields or []
                for sub_field in fields_to_process:
                    dependent_types.update(
                        SchemaSplitter.extract_dependent_types(
                            sub_field, type_definitions, visited
                        )
                    )

            # Handle EnumTypeDefinitionNode (no fields to process, but still a dependent type)
            elif isinstance(type_def, EnumTypeDefinitionNode):
                dependent_types.add(dep_type)

        # Process arguments of the field (for input types)
        if hasattr(field, "arguments") and field.arguments:
            for argument in field.arguments:
                try:
                    arg_type = SchemaSplitter.get_named_type(argument.type)
                except ValueError:
                    continue  # Skip if the argument type is unexpected

                if arg_type not in visited and arg_type in type_definitions:
                    dependent_types.update(
                        SchemaSplitter.extract_dependent_types(
                            argument, type_definitions, visited
                        )
                    )

        return dependent_types

    @staticmethod
    def split_schema(schema: str) -> List[str]:
        document: DocumentNode = SchemaSplitter.parse_schema(schema)
        type_definitions: Dict[
            str,
            ObjectTypeDefinitionNode
            | InputObjectTypeDefinitionNode
            | EnumTypeDefinitionNode,
        ] = {
            defn.name.value: defn
            for defn in document.definitions
            if isinstance(
                defn,
                (
                    ObjectTypeDefinitionNode,
                    InputObjectTypeDefinitionNode,
                    EnumTypeDefinitionNode,
                ),
            )
        }

        sub_graphs = []
        for op_type_name in ["Query", "Mutation"]:
            if op_type_name in type_definitions:
                op_def: ObjectTypeDefinitionNode = type_definitions[op_type_name]
                if hasattr(op_def, "fields") and op_def.fields:
                    for field in op_def.fields:
                        dependent_types = SchemaSplitter.extract_dependent_types(
                            field, type_definitions
                        )
                        sub_schema_parts = []

                        # Add the schema definition for the operation type (Query or Mutation)
                        sub_schema_parts.append(
                            f"schema {{ {op_type_name.lower()}: {op_type_name} }}"
                        )

                        # Add the definition for the current operation type and its field
                        field_args_str = ", ".join(
                            print_ast(arg).strip() for arg in field.arguments
                        )
                        field_type_str = print_ast(field.type).strip()
                        sub_schema_parts.append(
                            f"type {op_type_name} {{ {field.name.value}({field_args_str}): {field_type_str} }}"
                        )

                        # Add the definitions of the dependent types
                        for dep_type_name in sorted(list(dependent_types)):
                            if dep_type_name in type_definitions:
                                sub_schema_parts.append(
                                    print_ast(type_definitions[dep_type_name]).strip()
                                )

                        sub_graphs.append("\n\n".join(sub_schema_parts) + "\n")
        return sub_graphs
