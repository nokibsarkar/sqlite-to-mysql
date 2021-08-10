import sqlite3, re
TYPE = re.compile("\t`([^`]+)` ([\S])")
TABLE_NAMES = """
SELECT
  name, sql
FROM
  sqlite_master
WHERE
  type ='table'
  AND name NOT LIKE 'sqlite_%';
"""
def test_sql(from_file):
    print("Creating a temporary database")
    with sqlite3.connect(":memory:") as conn:
        print("\tCreated a temprary database\n\tTrying to open the SQL file")
        with open(from_file, 'r') as fp:
            print('\tThe SQL file opened')
            commands = fp.read().split(';')
            num_commands = len(commands)
            for i in range(num_commands):
                print('Trying the Command No #',i)
                conn.executescript(commands[i])
    print("Successfully Tested")
conn = sqlite3.connect("database.db")
#conn.row_factory
tables = conn.execute(TABLE_NAMES).fetchall()
st = [
f"""
-- Sqlite3 to SQL format converted with the tool created by @nokibsarkar
-- Sqlite3 Version {sqlite3.version}
"""
]
for table in tables:
    name, scheme = table
    print(f"Creating SQL FOR `{name}`....")
    st.append(f"""
-- Table Scheme for the Table named `{name}`
    	""")
    st.append(f"{scheme};")
    print("\tBasic Definition Added\n\tAdding Indices")
    st.append(f"-- Start Adding all the Indices for table `{name}`")
    indices = conn.execute(f"SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='{name}'")
    for index in indices:
        st.append(f"{index[1]};")
    st.append(f"-- Index for `{name}` Completed")
    print("\tIndex Added Successfully")
    types = TYPE.findall(scheme)
    rows = []#conn.execute(f"SELECT * FROM `{name}`")
    field_count = len(types)
    st.append("-- INSERTing all the rows")
    st.append(f"INSERT INTO `{name}` ({', '.join('`%s`' % i[0] for i in types)}) VALUES")
    for row in rows:
        fields = []
        for pos in range(field_count):
            if types[pos][1] == 'T':
                #Text field
                fields.append(f"'{row[pos]}'")
            elif types[pos][1] == 'B':
                #binary
                fields.append(f"b'{row[post]}'")
            else:
                #print(types[pos])
                #break
                fields.append(str(row[pos]))
        st.append(f"\t({', '.join(fields)})")
    st[-1] = f"{st[-1]};"
filename = 'database_backup.sql'
with open(filename,'w') as fp:
    fp.write('\n'.join(st))
    print('Saved the SQL to ', filename)
#conn.row_factory = sqlite3.Row
#res = conn.execute("SELECT * FROM sqlite_master")
#print(res.fetchall())
conn.close()
test_sql(filename)
