'''
    Note: docvs uses 3 seperate databases: docvs.db, wiki.db and log.db
    Reason for splitting is backup and multiprocess managment, also wiki.db can easily be shared, or backed up 

    docvs.db: Contains all the files and resources
        Deleting this file will result in full reindexing of all files and resources
        Note: this will remove all changes made to resources and remove all manual entries
    log.db: Contains all the log entries
        Deleting this file will result in loss of all log entries
        In an multi process environment, this file will be locked by the process that is writing to it
        Further logfiles will be written to a new file named log_x.db

'''

import aiosqlite
import os
async def connect_db(main):
    db = await aiosqlite.connect(os.path.join(main.indexdir,"docvs.db"))
    await db.execute("""
                         CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,    -- Unique internal identifier
                            caption TEXT,                            -- Caption of the file or entry (overrides path name)
                            path TEXT NOT NULL,                      -- Unique internal path
                            source TEXT NOT NULL,                    -- Source location
                            type INTEGER NOT NULL,                   -- Type of the entry (docvs.util.ResourceType)
                            entity TEXT DEFAULT '',                  -- Entity keyword
                            search_text TEXT DEFAULT '',             -- Indexed text
                            search_keywords TEXT DEFAULT '',         -- Indexed keywords (Additional keywords)
                            last_changed INTEGER NOT NULL,           -- Last modification timestamp
                            indexed INTEGER DEFAULT 0,               -- Indexed status (0 pending, -1 not indexed,  >0 timestamp of indexing)
                            description TEXT,                        -- Description of the file or entry
                            valid_to INTEGER,                        -- Expiry or validity timestamp
                            sha256 TEXT,                             -- SHA256 hash of the file
                            permission_group_filter TEXT DEFAULT '', -- Permission group filter (empty inherits from category)
                            updated_module TEXT NOT NULL,            -- i.e."docvs.fileindexer, "docvs.wiki", "manual", ...
                            updated_module_version TEXT NOT NULL)     -- module version
            """)
    await db.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier
                name TEXT NOT NULL,                    -- Name of the file or entry
                permission INTEGER DEFAULT 0,          -- Permission level
                permission_groups TEXT DEFAULT ''    -- Permission groups
                     
            )
            """)   




        #create indexes
    await db.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_path ON items(path)
    """)

    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_type ON items(type)
    """)
    await db.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_uid ON user(id)
    """)
    await db.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_name ON user(name)
    """)


    await db.execute("""
            CREATE TABLE IF NOT EXISTS changelog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_id INTEGER,
                timestamp INTEGER,
                new_content TEXT,
                user INTEGER
                )
            """)
    # create indexes

    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_resourceid ON changelog(resource_id)
    """)
    await db.commit()
    main.db = db
    main.wikidb = await aiosqlite.connect(os.path.join(main.indexdir,"wiki.db"))


    await main.wikidb.execute("""
            CREATE TABLE IF NOT EXISTS wiki (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier
                name TEXT NOT NULL,                    -- Title of the wiki entry
                path TEXT NOT NULL,                    -- Path of the wiki entry ( i.e. "/category/name")
                content TEXT NOT NULL,                 -- Content of the wiki entry
                search_words TEXT DEFAULT '',          -- Searchable content (i.e. fulltext without images)
                index_mode TEXT,
                last_changed INTEGER NOT NULL         -- Last modification timestamp
            )
            """)
    await main.wikidb.execute("""
            CREATE TABLE IF NOT EXISTS wiki_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier
                wiki_id INTEGER NOT NULL,              -- Wiki identifier
                timestamp INTEGER NOT NULL,            -- Timestamp of the history entry
                content TEXT NOT NULL,                 -- Content of the history entry
                user TEXT NOT NULL                  -- User identifier
            )
            """)
    await main.wikidb.execute("""
                              CREATE UNIQUE INDEX IF NOT EXISTS idx_path ON wiki(path)
                                """)
  
    await main.wikidb.commit()
    logdb = await aiosqlite.connect(os.path.join(main.indexdir,"log.db"))
    await logdb.execute("""
            CREATE TABLE IF NOT EXISTS log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier
                logtype INTEGER NOT NULL,               -- Type of the log entry
                timestamp INTEGER NOT NULL,            -- Timestamp of the log entry
                message TEXT NOT NULL,                 -- Log message
                level INTEGER NOT NULL,                -- Log level
                user INTEGER,                           -- User identifier
                expires INTEGER                      -- Expiry timestamp
            )
            """)
    await logdb.commit()
    main.logdb = logdb  

    

