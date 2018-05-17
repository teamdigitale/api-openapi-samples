YAML=$(shell find * -name \*yaml)
YAMLSRC=$(shell find . -name \*yaml.src)
YAMLGEN=$(patsubst %.yaml.src,%.yaml,$(YAMLSRC))

yaml: $(YAMLGEN)

%.yaml: %.yaml.src
	. .tox/python/bin/activate
	yamllint $<
	python ./yaml-resolver.py $< $@


yamllint: $(YAML)
	. .tox/python/bin/activate
	yamllint $?
