from graphviz import Digraph

class ERDGraphviz:
    def __init__(self, metadata):
        """
        Initialiseert de ERD generator met de opgegeven metadata.
        """
        self.metadata = metadata
        self.graph = Digraph(format='png')
        self.graph.attr('node', shape='box', style='filled', fontname='Helvetica')

    def add_entities(self):
        """
        Voegt alle tabellen toe als knopen in de ERD, met kleur op basis van hun type.
        """
        for data in self.metadata.values():
            table_name = data["table_name"]
            pattern = data.get("pattern", "")

            if pattern == "sat":
                color = "lightyellow"
            elif pattern == "link":
                color = "red3"
            else:  # hub of onbekend
                color = "lightblue"

            self.graph.node(table_name, fillcolor=color)

    def add_relationships(self):
        """
        Voegt pijlen toe tussen tabellen op basis van PK/FK-relaties.
        """
        for data in self.metadata.values():
            table_name = data["table_name"]
            pattern = data.get("pattern", "")
            fk_list = data.get("fk", [])
            pk = data.get("pk", "")

            if pattern == "sat":
                # Sat → Hub via PK
                for other in self.metadata.values():
                    if other.get("pattern") == "hub" and pk == other.get("pk"):
                        self.graph.edge(other["table_name"], table_name)
            elif pattern == "link":
                # Link → Hubs via FK
                for fk in fk_list:
                    for other in self.metadata.values():
                        if other.get("pattern") == "hub" and fk == other.get("pk"):
                            self.graph.edge(other["table_name"], table_name)

    def generate(self, output_filename="erd_diagram"):
        """
        Genereert het ERD-diagram en slaat dit op als PNG-bestand.
        """
        self.add_entities()
        self.add_relationships()
        self.graph.render(filename=output_filename, cleanup=True)
        print(f"✅ ERD generated and saved as: {output_filename}.png")
