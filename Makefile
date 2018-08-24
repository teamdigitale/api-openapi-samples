YAML=$(shell find * -name \*yaml)
YAMLSRC=$(shell find . -name \*yaml.src)
YAMLGEN=$(patsubst %.yaml.src,%.yaml,$(YAMLSRC))

yaml: $(YAMLGEN)

.ONESHELL:
%.yaml: %.yaml.src
	. .tox/py36/bin/activate
	yamllint $<
	python -m openapi_resolver $< $@


yamllint: $(YAML)
	. .tox/py36/bin/activate
	yamllint $?
