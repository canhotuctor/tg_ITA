# Diretório onde os arquivos temporários e o PDF serão
# gerados por pdflatex.
#
# Mantenha sincronizado com o valor em .gitignore
FILE = tese
TEMP_DIR = tmp
TEX = pdflatex
BIB = biber
TEX_FLAGS = -output-directory=$(TEMP_DIR)
TEX_FLAGS_FAST = -output-directory=$(TEMP_DIR) -interaction=nonstopmode -halt-on-error
TEX_ENV = eval "$$(/usr/libexec/path_helper)";


.PHONY:	all complete fast pdf bib clean-win clean-linux-mac clean-biber-cache

all: complete

complete: $(TEMP_DIR)
	$(TEX_ENV) $(TEX) $(TEX_FLAGS) $(FILE).tex
	$(TEX_ENV) $(BIB) $(TEMP_DIR)/$(FILE)
	$(TEX_ENV) $(TEX) $(TEX_FLAGS) $(FILE).tex
	$(TEX_ENV) $(TEX) $(TEX_FLAGS) $(FILE).tex
	cp $(TEMP_DIR)/$(FILE).pdf $(FILE).pdf

fast: $(TEMP_DIR)
	$(TEX_ENV) $(TEX) $(TEX_FLAGS_FAST) $(FILE).tex
	$(TEX_ENV) $(BIB) $(TEMP_DIR)/$(FILE)
	$(TEX_ENV) $(TEX) $(TEX_FLAGS_FAST) $(FILE).tex
	$(TEX_ENV) $(TEX) $(TEX_FLAGS_FAST) $(FILE).tex
	cp $(TEMP_DIR)/$(FILE).pdf $(FILE).pdf

$(TEMP_DIR):
	mkdir -p $(TEMP_DIR)

pdf: $(TEMP_DIR)
	$(TEX_ENV) $(TEX) $(TEX_FLAGS) $(FILE).tex

bib: $(TEMP_DIR)/$(FILE).bcf
	$(TEX_ENV) $(BIB) $(TEMP_DIR)/$(FILE)

clean-win:
	@del /f /a /s $(TEMP_DIR)

clean-linux-mac:
	rm -r $(TEMP_DIR)/*

clean-biber-cache:
	rm -rf /var/folders/*/par-*/cache-*/ 2>/dev/null || true
