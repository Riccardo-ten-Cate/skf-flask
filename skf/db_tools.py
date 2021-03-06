import os
from flask import Flask
from skf import settings
from shutil import copyfile
from skf.database import db
from skf.database.kb_items import kb_items
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(os.path.join(app.root_path, settings.DATABASE))
    rv.row_factory = sqlite3.Row
    return rv


def init_db(testing=False):
    """Initializes the database.""" 
    if testing == True:
        db = connect_db()
        print(app.root_path)
        with app.open_resource(os.path.join(app.root_path, '../tests/selenium/clean-test.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    else:
        os.remove(os.path.join(app.root_path, settings.DATABASE))
        open(os.path.join(app.root_path, 'db.sqlite_schema'), 'a')
        os.remove(os.path.join(app.root_path, 'db.sqlite_schema'))
        copyfile(os.path.join(app.root_path, "schema.sql"), os.path.join(app.root_path, 'db.sqlite_schema'))
        init_md_code_examples()
        init_md_knowledge_base()
        db = connect_db()
        with app.open_resource(os.path.join(app.root_path, 'db.sqlite_schema'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def update_db():
    """Update the database."""
    os.remove(os.path.join(app.root_path, 'db.sqlite_schema'))
    db = connect_db()
    with app.open_resource(os.path.join(app.root_path, 'clean.sql'), mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    init_md_code_examples()
    init_md_knowledge_base()
    with app.open_resource(os.path.join(app.root_path, 'db.sqlite_schema'), mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, settings.DATABASE):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_md_knowledge_base():
    """Converts markdown knowledge-base items to DB."""
    kb_dir = os.path.join(app.root_path, 'markdown/knowledge_base')
    try:
        for filename in os.listdir(kb_dir):
            if filename.endswith(".md"):
                name_raw = filename.split("-")
                kbID = name_raw[0].replace("_", " ")
                title = name_raw[3].replace("_", " ")
                file = os.path.join(kb_dir, filename)
                data = open(file, 'r')
                file_content = data.read()
                data.close()
                content_escaped = file_content.translate(str.maketrans({"'":  r"''", "-":  r"", "#":  r""}))
                query = "INSERT OR REPLACE INTO kb_items (kbID, content, title) VALUES ('"+kbID+"','"+content_escaped+"', '"+title+"'); \n"
                with open(os.path.join(app.root_path, 'db.sqlite_schema'), 'a') as myfile:
                        myfile.write(query)
        print('Initialized the markdown knowledge-base.')
        return True
    except:
        return False


def init_md_code_examples():
    """Converts markdown code-example items to DB."""
    kb_dir = os.path.join(app.root_path, 'markdown/code_examples/')
    code_langs = ['asp', 'java', 'php', 'flask', 'django', 'go', 'ruby']
    try:
        for lang in code_langs:
            for filename in os.listdir(kb_dir+lang):
                if filename.endswith(".md"):
                    name_raw = filename.split("-")
                    title = name_raw[3].replace("_", " ")
                    file = os.path.join(kb_dir+lang, filename)
                    data = open(file, 'r')
                    file_content = data.read()
                    data.close()
                    content_escaped = file_content.translate(str.maketrans({"'":  r"''", "-":  r"", "#":  r""}))
                    query = "INSERT OR REPLACE INTO code_items (content, title, code_lang) VALUES ('"+content_escaped+"', '"+title+"', '"+lang+"'); \n"
                    with open(os.path.join(app.root_path, 'db.sqlite_schema'), 'a') as myfile:
                            myfile.write(query)
        print('Initialized the markdown code-example.')
        return True
    except:
        return False
