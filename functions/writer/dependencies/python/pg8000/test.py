import pg8000

conn = pg8000.connect(user="postgres", password="C.P.Snow", port=5438)
cursor = conn.cursor()

cursor.execute("create temporary table a ( foo numeric(20, 7));")
cursor.execute('insert into a(foo) values(%s)', [1560704964.331047])
conn.commit()

print(list(cursor.execute('select foo from a')))
# [[Decimal('1560704964.3310500')]]


cursor.execute("create temporary table b ( foo double precision);")
cursor.execute('insert into b(foo) values(%s)', [1560704964.331047])
conn.commit()

print(list(cursor.execute('select foo from b')))
# [[1560704964.331047]]

cursor.execute("create temporary table c ( foo numeric(20, 7));")
cursor.execute('insert into c(foo) values(%s)', ['1560704964.331047'])
conn.commit()

print(list(cursor.execute('select foo from c')))
# [[Decimal('1560704964.3310470')]]

conn.close()
