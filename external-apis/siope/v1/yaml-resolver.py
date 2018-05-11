
import yaml
from sys import argv



def main(src_file, dst_file):
  # Resolve references in yaml file
  yaml.Dumper.ignore_aliases = lambda *args : True

  with open(src_file) as fh_src, open(dst_file, 'w') as fh_dst:
    ret = yaml.load(fh_src)
    content = yaml.dump(ret, default_flow_style=0)
    fh_dst.write(content)

if __name__ == '__main__':
  try:
    progname, src_file, dst_file = argv
  except:
    raise SystemExit("usage: src_file.yaml.src dst_file.yaml", argv)
  
  main(src_file, dst_file)
   
