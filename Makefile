
build: zip exe

install: build
	cp pj ~/.local/bin/

zip: clean
	cd pjpy && zip -r ../pj.zip . -x "*/__pycache__/*"

exe:
	echo '#!/usr/bin/env python3' | cat - pj.zip > pj && chmod +x pj
	rm pj.zip

deploy: build
	mv pj ~/.local/bin/

clean:
	rm -f pj.zip pj
	rm -rf pjpy/**/*.pyc
	rm -rf pjpy/**/__pycache__
