from sqlalchemy import create_engine

eng = create_engine("sqlite://")
conn = eng.connect()
conn.execute("attach 'appdatabase' as my_schema")
