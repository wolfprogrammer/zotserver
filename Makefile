#------------ zotserver Makefile --------------
#   
#


all: tar


tar: sdist

sdist:
	python setup.py sdist


build:
	python setup.py build

install:
	python setup.py install

uninstall:
	rm -rf /usr/local/lib/python2.7/dist-packages/zotserver
	rm -rf /usr/local/lib/python2.7/dist-packages/zotserver*.egg-info
	rm -rf /etc/init.d/zotserver


# Generate documentation
# 
doc:
	epydoc --conf epydoc.conf zotserver
	mv zotserver/doc .
	#doxygen

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
	rm -rf build dist *.egg-info doc



