import pandas as pd
import sqlite3


def db_update(database_path):
    allconf_create_table = """ CREATE TABLE IF NOT EXISTS AllConf (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                organizer TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                country TEXT NOT NULL,
                website TEXT NOT NULL,
                organizer_email TEXT NOT NULL,
                deadline TEXT NOT NULL,
                about_conf TEXT
                ); """
    
    allconf_insert = """INSERT INTO AllConf (date, link, name, organizer, category, location, country, website,
                    organizer_email, deadline, about_conf) VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
    
    topconf_create_table = """ CREATE TABLE IF NOT EXISTS TopConf (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                link TEXT NOT NULL,
                name TEXT NOT NULL,
                organizer TEXT NOT NULL,
                location TEXT NOT NULL,
                country TEXT NOT NULL,
                website TEXT NOT NULL,
                deadline TEXT NOT NULL,
                hindex INTEGER NOT NULL
                ); """
    
    topconf_insert = """INSERT INTO TopConf (date, link, name, organizer, location, country, website,
                    deadline, hindex) VALUES(?,?,?,?,?,?,?,?,?)"""
    
    univ_create_table = """ CREATE TABLE IF NOT EXISTS UnivPgms (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                College TEXT NOT NULL,
                Courses TEXT NOT NULL
                ); """
    univ_insert = """INSERT INTO UnivPgms (College, Courses) VALUES(?,?)"""
    
    # create a database connection
    conn = sqlite3.connect(database_path)
    if conn is not None:
        c = conn.cursor()
        c.execute(allconf_create_table)
        c.execute(topconf_create_table)
        c.execute(univ_create_table)
        
        for tup in AllConf_list:
            try: c.execute(allconf_insert, tup)
            except: continue
                
        for tup in TopConf_list:
            try: c.execute(topconf_insert, tup)
            except: continue
                
        for tup in UnivPgms_list:
            try: c.execute(univ_insert, tup)
            except: continue
        conn.commit()
        conn.close()
        
    else:
        print("Error! cannot create the database connection.")



AllConf = pd.read_csv("AllConf.csv")
AllConf_list = list(map(tuple, AllConf.values))

TopConf = pd.read_csv("TopConf.csv")
TopConf_list = list(map(tuple, TopConf.values))

UnivPgms = pd.read_csv("UnivPgms.csv")
UnivPgms_list = list(map(tuple, UnivPgms.values))

        
if __name__ == '__main__':
    db_path = "KonfHub.db"
    db_update(db_path)



