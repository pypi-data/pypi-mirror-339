import os
import json
import aiosqlite
import sqlite3 as sqlite
from enum import Enum
import asyncio
class ProjectManager():
    def __init__(self,parent):
        self.appmain = parent

    async def refresh_projects(self):
      



        for project_root in self.appmain.configuration["project_roots"]:
            if "project.json" in os.listdir(project_root):
                await self.refresh_project(project_root)
                continue
            for root, dirs, files in os.walk(project_root):
                if 'project.json' in files:
                    await self.refresh_project(root)
    async def refresh_project(self,path):
        project = await load_project(path)
        if not project:return
        if project.name in self.appmain.projects:
            if self.appmain.projects[project.name].path != path:    
                print(f"Project {project.name} already exists in {self.appmain.projects[project.name].path}, skipping {path}")
        else:
                self.appmain.projects[project.name] = project
async def load_project(path):   

    try:
        return Project(path) # not async, but this is not done often TODO: make async
    except json.JSONDecodeError:
        print(f"Error loading project {path}: project.json is not a valid JSON.")
    except FileNotFoundError:
        print(f"Error loading project {path}: project.json not found.")
    except Exception as e:
        print(f"Error loading project {path}: {e}")



class FieldType(Enum):
    BOOL = "bool"
    MULTIBOOL = "multibool"
    SELECT = "select"
    INT = "int"
    DECIMAL = "decimal"
    CATEGORY = "category"
    TEXT = "text"



class Project():
    def __init__(self,path):
        
        self.path = path
        self.project_data = None
        self.fields={}
        self.study_count=0
        self.async_db = None
        
        self.load_project_data()
    def load_project_data(self):

        with open(os.path.join(self.path, 'project.json'), 'r') as project_file:
                self.configuration = json.load(project_file)
                self.name=self.configuration["name"]
                if "description" in self.configuration:
                    self.description=self.configuration["description"]
                else:
                    self.description=""




        db_path = os.path.join(self.path, 'data.db')
        self.db= sqlite.connect(db_path)
        self.init_db()        
        self.refresh_data()
        print(f"Loaded project {self.name} from {self.path}")

    def init_db(self):

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS studies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,                                
            name TEXT,          
            source TEXT,
            source_collection TEXT,
            source_id TEXT,
            doi TEXT,
            comment TEXT,
            abstract TEXT,
            fulltext TEXT,
            year INT,
            month INT,
            day INT,
            study_data TEXT,
            state INTEGER,    
            excluded_reason INTEGER
            )
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_id ON studies (source_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source ON studies (source)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_collection ON studies (source_collection)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_source_id ON studies (source, source_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_year ON studies (year)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_state ON studies (state)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_excluded_reason ON studies (excluded_reason)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_doi ON studies (doi)
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT,
            caption TEXT,
            description TEXT,                
            type TEXT,
            reference TEXT,
            llm_query TEXT,
            style TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                validator TEXT, 
                ts INTEGER,
                data_changed INTEGER,
                data TEXT,               
                study_state INTEGER,
                validation_state INTEGER,      /* -1 invalid/deprecated/deleted 1 valid, 10 revision requested */
                consensus INTEGER   /* 1 if at ts time all validations are the same, 0 otherwise */
            )
        ''')
        # consensus = the newest validation of each user is the same, checked on save, data equals data

        
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_study_id ON validation (study_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_validator ON validation (validator)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_ts ON validation (ts)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_valid_state ON validation (validation_state)
        ''')



        self.db.commit()
    def refresh_data(self):
        new_data = {}
        cursor=self.db.execute('SELECT field_name, caption, description, type, reference, llm_query, style FROM fields')
        data=cursor.fetchall()
        for row in data:
            field_name, caption, description, type, reference, llm_query, style = row
            new_data[field_name] = {
                "name": field_name,
                "caption": caption,
                "description": description,
                "type": type,
                "reference": json.loads(reference),
                "llm_query": llm_query,
                "style": style
            }
        self.fields = new_data
        self.study_count = self.db.execute('SELECT COUNT(*) FROM studies').fetchone()[0]

    def register_field(self,field_name,caption="",description="",type=FieldType.DECIMAL,reference={},llm_query="",style=""):
    
        if len(caption)==0: caption=field_name
        cursor = self.db.execute('SELECT COUNT(*) FROM fields WHERE field_name = ?', (field_name,))
        if cursor.fetchone()[0] > 0:
            print(f"Field {field_name} already exists.")
            return
        
        self.db.execute('''
            INSERT INTO fields (field_name, caption, description, type, reference, llm_query, style)
            VALUES (?,?,?,?,?,?,?)
        ''',(field_name,caption,description,type.value,json.dumps(reference),llm_query,style))
        sqltype=None
        if type == FieldType.CATEGORY:
            sqltype = "TEXT"
        elif type=="bool":
            sqltype = "INTEGER"
        elif type == FieldType.SELECT:
            sqltype = "TEXT"
        
        elif type == FieldType.DECIMAL:
            sqltype = "REAL"
        elif type == FieldType.INT:
            sqltype = "INTEGER"
        elif type == FieldType.TEXT:
            sqltype = "TEXT"

        if sqltype:
            self.db.execute(f'''
                ALTER TABLE studies ADD COLUMN data_{field_name} {sqltype}
            ''')
        elif type == FieldType.MULTIBOOL:
            for ref in reference:
                self.db.execute(f'''
                    ALTER TABLE studies ADD COLUMN data_{field_name}_{ref} INTEGER
                ''')

        self.db.commit()
    def drop_field(self,field_name):
        cursor = self.db.execute('SELECT type FROM fields WHERE field_name = ?', (field_name,))
        ret=cursor.fetchone()
        if not ret:
            print(f"Field {field_name} does not exist.")
            return
        field_type = ret[0]
        if field_type == FieldType.MULTIBOOL.value:   
            cursor = self.db.execute("PRAGMA table_info(studies)")
            columns = [row[1] for row in cursor.fetchall()]
            for column in columns:
                if column.startswith(f"data_{field_name}_"):
                    self.db.execute(f'ALTER TABLE studies DROP COLUMN {column}')
        else:
            self.db.execute(f'''
                ALTER TABLE studies DROP COLUMN data_{field_name}
            ''')

        self.db.execute('DELETE FROM fields WHERE field_name = ?', (field_name,))
        
        self.db.commit()
        
    def register_pubmed(self, pid, type="journal_article",name="",abstract="",fulltext="",year=0,month=0,day=0,study_data="{}",state=0,excluded_reason=0,source_collection="default",doi=""):
        cursor=self.db.execute('SELECT COUNT(*) FROM studies WHERE source = ? AND source_id = ?', ("pubmed", pid))

        count = cursor.fetchone()
        if count[0] > 0:return

        self.db.execute('''
            INSERT INTO studies (type, name, source, source_id, comment, abstract, fulltext, year, month, day, study_data, state, excluded_reason,source_collection,doi)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',(type,name,"pubmed",pid,"",abstract,fulltext,year,month,day,study_data,state,excluded_reason,source_collection,doi))
        self.db.commit()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "fields": self.fields,
            "study_count": self.study_count
        }
    def get_study_list(self,q_from=0,limit=30):
        cursor = self.db.execute('SELECT * FROM studies LIMIT ? OFFSET ?', (limit,q_from))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]    
    
    async def get_study_list_async(self,data,session_data,limit=30,id_only=False):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))

 
        order = "ORDER BY id DESC"
        if "order_mode" in data:
            if data["order_mode"] == "asc":
                order = "ORDER BY id ASC"
            elif data["order_mode"] == "desc":
                order = "ORDER BY id DESC"
            elif data["order_mode"] == "date_desc":
                order = "ORDER BY year DESC, month DESC, day DESC"
            elif data["order_mode"] == "date_asc":
                order = "ORDER BY year ASC, month ASC, day ASC"
            elif data["order_mode"] == "pseudorandom": # linear congruential generator
                uid=session_data["user_id"]
                order = f"ORDER BY abs((id * 1103515245 + 12345 + {uid}) % 2147483647)"

        if "from" in data:
            q_from = data["from"]
        else:
            q_from=0
        q_filter = None

        if "filter" in data:
            q_filter = data["filter"]
            if len(q_filter) <3:
                q_filter=None
            else:
                q_filter = f"%{q_filter}%"

        if id_only:
            selector="id"
        else:
            selector="*"

        if q_filter:
            async with self.async_db.execute('SELECT '+selector+' FROM studies WHERE name LIKE ? '+order+' LIMIT ? OFFSET ? ', (f"%{q_filter}%",limit,q_from)) as cursor:
                rows = await cursor.fetchall()
                columns = [column[0] for column in cursor.description]

                if not id_only:
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return [row[0] for row in rows]
        else:
            async with self.async_db.execute('SELECT '+selector+' FROM studies '+order+' LIMIT ? OFFSET ?', (limit,q_from)) as cursor:
                rows = await cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                if not id_only:
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return [row[0] for row in rows]
    async def get_study_async(self,data):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        ret = {}
        async with self.async_db.execute('SELECT * FROM studies WHERE id = ?', (data["study_id"],)) as cursor:
            row = await cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            ret["study"]= dict(zip(columns, row))
        async with self.async_db.execute('SELECT * FROM validation WHERE study_id = ?', (data["study_id"],)) as cursor:
            rows = await cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            ret["validation"] = [dict(zip(columns, row)) for row in rows]
        ret["project"]=self.to_dict()
        return ret