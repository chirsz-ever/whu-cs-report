
all: demo.pdf

demo_processed.html: demo.html
	"../../preprocess.py" $< -o $@ -s '../../whu-cs-report-without-auto-number.css'

demo.pdf: demo_processed.html
	prince $< -o $@

.PRONY: clean all
clean:
	-rm *.html demo.pdf
	-del *.html demo.pdf
