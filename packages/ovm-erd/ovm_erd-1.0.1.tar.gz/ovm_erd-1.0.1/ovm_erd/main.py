import argparse
from ovm_erd import erd_graphviz
from ovm_erd.erd_sql import erd_sql
from ovm_erd.erd_drawio import generate_drawio_xml
from ovm_erd.erd_mermaid import export_mermaid_markdown
from ovm_erd.validator import validate_metadata
from ovm_erd.repository_reader import read_repository, build_metadata_dict


def main():
    parser = argparse.ArgumentParser(
        description="📦 OVM ERD Toolkit — Generate ERDs and SQL from your repository"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Graphviz ERD
    graphviz_parser = subparsers.add_parser("graphviz", help="Generate ERD as Graphviz PNG")
    graphviz_parser.add_argument("--path", type=str, default="./examples", help="Path to SQL repository")
    graphviz_parser.add_argument("--ensemble", type=str, default=None, help="Filter by tag (ensemble)")

    # Draw.io ERD
    drawio_parser = subparsers.add_parser("drawio", help="Generate ERD as draw.io XML")
    drawio_parser.add_argument("--path", type=str, default="./examples", help="Path to SQL repository")
    drawio_parser.add_argument("--ensemble", type=str, required=True, help="Ensemble name or 'distinct'")

    # SQL Generator
    sql_parser = subparsers.add_parser("sql", help="Generate SQL query for an ensemble")
    sql_parser.add_argument("--path", type=str, default="./examples", help="Path to SQL repository")
    sql_parser.add_argument("--ensemble", type=str, required=True, help="Tag/ensemble to query")

    # Mermaid ERD
    mermaid_parser = subparsers.add_parser("mermaid", help="Generate Mermaid ERD markdown")
    mermaid_parser.add_argument("--path", type=str, default="./examples", help="Path to SQL repository")
    mermaid_parser.add_argument("--ensemble", type=str, default="all", help="Tag/ensemble to export")

    # Metadata Validator
    validate_parser = subparsers.add_parser("validate", help="Validate metadata and generate HTML report")
    validate_parser.add_argument("--path", type=str, default="./examples", help="Path to SQL repository")

    args = parser.parse_args()

    if args.command == "graphviz":
        erd_graphviz(path=args.path, ensemble=args.ensemble)

    elif args.command == "drawio":
        files = read_repository(args.path)
        metadata = build_metadata_dict(files)

        if args.ensemble == "distinct":
            all_tags = set(tag for d in metadata.values() for tag in d.get("tags", []))
            for tag in all_tags:
                filtered = {
                    fn: d for fn, d in metadata.items()
                    if tag in d.get("tags", [])
                }
                if filtered:
                    output_file = f"ovm_erd/output/erd_{tag}.drawio.xml"
                    generate_drawio_xml(filtered, output_file=output_file, diagram_title=f"ERD - {tag}")
        else:
            filtered_metadata = {
                fn: d for fn, d in metadata.items()
                if args.ensemble in d.get("tags", [])
            }
            if not filtered_metadata:
                print(f"⚠️ No metadata found for ensemble '{args.ensemble}'")
            else:
                output_file = f"ovm_erd/output/erd_{args.ensemble}.drawio.xml"
                generate_drawio_xml(filtered_metadata, output_file=output_file, diagram_title=f"ERD - {args.ensemble}")

    elif args.command == "sql":
        erd_sql(path=args.path, ensemble=args.ensemble)

    elif args.command == "mermaid":
        files = read_repository(args.path)
        metadata = build_metadata_dict(files)
        export_mermaid_markdown(metadata, ensemble=args.ensemble)

    elif args.command == "validate":
        files = read_repository(args.path)
        metadata = build_metadata_dict(files)
        validate_metadata(metadata)

    else:
        parser.print_help()
