import argparse
from graphql_utils import SchemaSplitter


def main():
    parser = argparse.ArgumentParser(
        description="Load and print the contents of a file."
    )
    parser.add_argument("--input", required=True, help="Path to the input file")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as file:
            contents = file.read()
            print(contents)
            sub_graphs = SchemaSplitter.split_schema(contents)
            for i, sub_graph in enumerate(sub_graphs):
                print(f"Subgraph {i + 1}:\n{sub_graph}\n")
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
