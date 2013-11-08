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

clean:
	rm -rf doc html



