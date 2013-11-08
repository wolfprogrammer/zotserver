#------------ zotserver Makefile --------------
#   
#


# Generate documentation
# 
doc:
	#epydoc --conf epydoc.conf
	doxygen 

# Open documentation
# 
open:
	firefox html/index.html

#-----------------------------------------#
#  Generates the dabase documentation     #
#                                         #
# schemaspy and javasql                   #
#                                         #
schema:
	java -jar /opt/schemaspy/schemaSpy_5.0.0.jar -t sqlite -db zotero.sqlite -o schema -sso  -dp /opt/schemaspy/javasql

clean:
	rm -rf doc html



