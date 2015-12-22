""" A pipeline that generates analysis pipelines. 

author: Brian Schrader
since: 2015-12-22
"""

from __future__ import print_function
import argparse, pickle, sys

from parser import Parser
from models.command import Command
from template import make_script


def main():
    """ Given a config file, spit out the script to run the analysis. """
    parser = argparse.ArgumentParser(
        description='A pipeline that generates analysis pipelines.')
    parser.add_argument('input',
                   help='A valid metapipe configuration file.')
    parser.add_argument('-o', '--output',
                   help='An output destination. If none is provided, the results will be printed to stdout.', default=sys.stdout)
    parser.add_argument('-t', '--temp',
                   help='A desired metapipe binary file. This is used to store temp data between generation and execution. (Default: "%(default)s")', default='.metapipe')
    parser.add_argument('-s', '--shell',
                   help='The path to the shell to be used when executing the pipeline. (Default: "%(default)s)"', default='/bin/bash')
    parser.add_argument('-r', '--run',
                   help='Run the pipeline as soon as it\'s ready.', action='store_true')
    args = parser.parse_args()
    
    try:
        with open(args.input) as f:
            config = f.read()    
    except IOError:
        print('No valid config file found.')
        return 
    
    parser = Parser(config)
    
    try:
        commands = parser.consume()
    except ParseError as e:
        print('Syntax Error: Invalid config file. \n%s' % e)
        return 
    
    # TODO: Construct pipeline.
    pipeline = None
    
    with open(args.temp, 'wb') as f:
        pickle.dump(pipeline, f)
    
    script = make_script(temp=args.temp, shell=args.shell)
    
    if args.run:
        print('Initiating pipeline...')
        pass
    try:
        f = open(args.output, 'w')
        args.output = f
    except TypeError:
        pass

    args.output.write(script)
    f.close()
    

if __name__ == '__main__':
    main()
