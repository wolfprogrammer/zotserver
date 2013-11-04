
conn= sq.connect(DATABASE2,timeout=10)
cur = conn.cursor()


sql =  """
      SELECT items.itemID,  items.key,  itemAttachments.path 
      FROM items, itemAttachments 
      WHERE  itemAttachments.itemID = items.itemID   
      ORDER BY items.itemID ASC    

       """

query=cur.execute(sql)      
rows=query.fetchall()


for row in rows:
	key = row[1]
	name = row[2]

	if name != None:
		name = name.split("storage:")
        name = name[1]
		
		path = STORAGE_PATH + key + "/" + name

		print "---------"
		print key
		print name
		print path