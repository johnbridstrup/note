from argparse import ArgumentParser
from sqlalchemy.exc import IntegrityError

try:
    from note_taker.pkg.sql import Session, Notebook, Note, Tag
except ModuleNotFoundError:
    from pkg.sql import Session, Notebook, Note, Tag


# Parser
parser = ArgumentParser(description="Note taking utility")
parser.add_argument("note", nargs="*", help="Note to be added")
parser.add_argument("-t", "--tags", nargs="*", help="Tags to be added or queried", required=False)
parser.add_argument("--list-tags", help="List tags", action="store_true", required=False)
parser.add_argument("-n", "--notebook", help="Notebook to be added to", required=False)
parser.add_argument("--notebooks", help="List notebooks", action="store_true", required=False)
parser.add_argument("-c", "--create", help="Create a new notebook", required=False)
parser.add_argument("-s", "--set-default", help="Set default notebook", required=False)
parser.add_argument("-l", "--notes", help="List notes", action="store_true", required=False)

def main():
    session = Session()
    args = parser.parse_args()

    if args.notebooks:
        print("Notebooks:")
        notebooks = session.query(Notebook)
        for notebook in notebooks:
            print(f"\t{notebook.name}{'*' if notebook.default else ''}")
        exit(0)
    
    if args.create is not None:
        try:
            Notebook.create(args.create, session)
            print(f"Created notebook {args.create}")
            exit(0)
        except IntegrityError:
            print(f"ERROR: Notebook \"{args.create}\" already exists!!")
            exit(1)
    
    if args.set_default is not None:
        new_default = session.query(Notebook).filter(Notebook.name == args.set_default).first()
        cur_default = session.query(Notebook).filter(Notebook.default == True).first()
        if new_default is None:
            print(f"ERROR: Notebook \"{args.set_default}\" does not exist!!")
            exit(1)
        new_default.default = True
        if cur_default:
            cur_default.default = False
        session.commit()
        print(f"Set default notebook to {args.set_default}")
        exit(0)
    
    if args.notebook is not None:
        notebook = session.query(Notebook).filter(Notebook.name == args.notebook).first()
    else:
        notebook = session.query(Notebook).filter(Notebook.default == True).first()

    if args.list_tags:  
        print(f"Tags in {notebook.name} notebook:")
        for tag in notebook.tags:
            print(f"\t{tag.name}")
        exit(0)
    
    tags = []
    if args.tags is not None:
        for tag in args.tags:
            tag_obj = session.query(Tag).filter(Tag.name == tag).first()
            if tag_obj is None:
                tag_obj = Tag(name=tag)
        tags.append(tag_obj)

    if args.notes:
        notes = session.query(Note).join(Note.tags).filter(
            Note.notebook == notebook.id,
        )
        if len(notes.all()) == 0:
            print(f"No notes found in {notebook.name} notebook")
            exit(0)
        if len(tags) > 0:
            notes = notes.filter(Tag.name.in_([tag.name for tag in tags]))
        for note in notes:
            print(note)
        exit(0)
    
    note = Note(
        note=" ".join(args.note),
        notebook=notebook.id,
        tags=tags
    )
    session.add(note)

    nb_tags = set(notebook.tags)
    nb_tags.update(tags)
    notebook.tags = list(nb_tags)
    
    session.commit()
    print(f"Note saved to {notebook.name} notebook")

if __name__ == "__main__":
    main()
