import importlib
import mug.repo
import os
import output

VERBS = [
    'add',
    'status',
    'commit'
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
  repo = mug.repo.MugRepository.discover(os.getcwd())
  output_stream = output.Output()
  module.run(repo, output_stream, args[1:])
  print output_stream.value()
