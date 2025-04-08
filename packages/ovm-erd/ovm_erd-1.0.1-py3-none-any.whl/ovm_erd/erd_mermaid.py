import os

def generate_mermaid_erd(metadata: dict, ensemble: str = "all") -> str:
    """
    Genereert een Mermaid ERD voor een bepaald ensemble of alle entiteiten.
    """

    filtered = metadata if ensemble == "all" else {
        fn: d for fn, d in metadata.items()
        if ensemble in d.get("tags", [])
    }

    if not filtered:
        return f"%% ⚠️ No tables found for ensemble: {ensemble}"

    lines = ["```mermaid", "erDiagram"]

    # Entiteiten
    for data in filtered.values():
        table = data["table_name"]
        pk = data.get("pk", "")
        fks = data.get("fk", [])
        attributes = []

        if pk:
            attributes.append(f"{pk} PK")
        for fk in fks:
            attributes.append(f"{fk} FK")

        attr_line = " ".join(attributes)
        lines.append(f"    {table} {{ {attr_line} }}")

    # Relaties (FK → PK koppeling)
    hubs = {
        d["pk"]: d["table_name"]
        for d in filtered.values() if d.get("pattern") == "hub"
    }

    for data in filtered.values():
        table = data["table_name"]
        fks = data.get("fk", [])
        for fk in fks:
            if fk in hubs:
                lines.append(f"    {table} }}o--|| {hubs[fk]} : links")

    lines.append("```")
    return "\n".join(lines)


def export_mermaid_markdown(metadata: dict, ensemble: str = "all", output_folder="ovm_erd/output"):
    """
    Genereert één of meerdere Markdown-bestanden met Mermaid ERD's.
    """

    os.makedirs(output_folder, exist_ok=True)

    if ensemble == "distinct":
        all_tags = set(tag for d in metadata.values() for tag in d.get("tags", []))
        for tag in all_tags:
            filtered = {
                fn: d for fn, d in metadata.items()
                if tag in d.get("tags", [])
            }
            if filtered:
                md = generate_mermaid_erd(filtered, ensemble=tag)
                with open(f"{output_folder}/erd_{tag}.md", "w", encoding="utf-8") as f:
                    f.write(md)
                print(f"✅ Mermaid ERD saved: erd_{tag}.md")
    else:
        md = generate_mermaid_erd(metadata, ensemble=ensemble)
        filename = f"erd_{ensemble}.md" if ensemble != "all" else "erd_all.md"
        with open(f"{output_folder}/{filename}", "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Mermaid ERD saved: {filename}")