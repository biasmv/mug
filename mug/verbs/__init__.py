import importlib
VERBS = [
    'add',
    'status'
]

def execute(args):
  """
  Dispatches to the correct verb and executes it based on the
  passed command-line arguments.
  """
  verb = args[0]
  if verb not in VERBS:
    print 'ERROR: don\'t know what you mean by %s' % verb
    return False
  module = importlib.import_module('mug.verbs.%s' % verb)
  module.run(args[1:])
