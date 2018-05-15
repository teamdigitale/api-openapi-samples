
import yaml
from sys import argv

def should_use_block(value):
    for c in u"\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if c in value:
            return True
    return False

def my_represent_scalar(self, tag, value, style=None):
    if should_use_block(value):
        style='|'
        import ipdb; ipdb.set_trace()
    else:
        style = self.default_style

    node = yaml.representer.ScalarNode(tag, value, style=style)
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    return node



def main(src_file, dst_file):
  # Resolve references in yaml file.
  yaml.Dumper.ignore_aliases = lambda *args : True

  # Dump long lines as "|".
  yaml.representer.BaseRepresenter.represent_scalar = my_represent_scalar


  with open(src_file) as fh_src, open(dst_file, 'w') as fh_dst:
    ret = yaml.load(fh_src)

    # Remove x-commons containing references and aliases.
    del ret['x-commons']

    content = yaml.dump(ret, default_flow_style=False, allow_unicode=True)
    fh_dst.write(content)

if __name__ == '__main__':
  try:
    progname, src_file, dst_file = argv
  except:
    raise SystemExit("usage: src_file.yaml.src dst_file.yaml", argv)
  
  main(src_file, dst_file)
   
