
import argparse
# from pathlib import Path
import traceback, sys
from datetime import datetime, timezone
# import re, json
from pathlib import Path






if __name__ == '__main__':
    # run as a program
    from reader_mdd import ReaderMDD
    from reader_spss import ReaderSPSS
    from reader_csv import ReaderCSV
elif '.' in __name__:
    # package
    from .reader_mdd import ReaderMDD
    from .reader_spss import ReaderSPSS
    from .reader_csv import ReaderCSV
else:
    # included with no parent package
    from reader_mdd import ReaderMDD
    from reader_spss import ReaderSPSS
    from reader_csv import ReaderCSV







def call_read_records_count_program():
    time_start = datetime.now()
    parser = argparse.ArgumentParser(
        description="Readometer",
        prog='mdmtoolsap readometer'
    )
    parser.add_argument(
        '-1',
        '--inpfile',
        help='Data file to read',
        type=str,
        required=True
    )
    parser.add_argument(
        '--format',
        default='autodetect',
        help='Data file type, or "autodetect"',
        choices=['autodetect','mdd','spss','csv'],
        type=str,
        required=False
    )
    args = None
    args_rest = None
    if True:
        args, args_rest = parser.parse_known_args()
    # else:
    #     args = parser.parse_args() # strict - it's not strict
    inp_file = None
    if args.inpfile:
        inp_file = Path(args.inpfile)
        inp_file = '{inp_file}'.format(inp_file=inp_file.resolve())
    else:
        raise FileNotFoundError('Data file: file not provided; please use --inpfile')

    if not(Path(inp_file).is_file()):
        raise FileNotFoundError('file not found: {fname}'.format(fname=inp_file))

    config = {
    }

    # print('MDM read script: script started at {dt}'.format(dt=time_start))

    format = None
    if args.format and args.format=='mdd':
        format = 'mdd'
    elif args.format and args.format=='spss':
        format = 'spss'
    elif args.format and args.format=='csv':
        format = 'csv'
    elif args.format and args.format=='autodetect':
        if Path(inp_file).suffix.strip().lower() in ['.sav']:
            format = 'spss'
        elif Path(inp_file).suffix.strip().lower() in ['.mdd','.ddf']:
            format = 'mdd'
        elif Path(inp_file).suffix.strip().lower() in ['.csv','.tsv']:
            format = 'csv'
        else:
            raise Exception('auto-detect failed: input file format not recognized, or can\'t be handled yet: {fname}'.format(fname=Path(inp_file).name))

    Reader = None
    if format=='spss':
        Reader = ReaderSPSS
    elif format=='mdd':
        Reader = ReaderMDD
    elif format=='csv':
        Reader = ReaderCSV
    else:
        raise Exception('format not supported: {fmt}'.format(fmt=format))


    with Reader(inp_file) as doc:

        result = doc.count_records()

        print(result)

    time_finish = datetime.now()
    # print('MDM read script: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start))


def call_test_program():
    msg = '''
hello, world!
    '''
    print(msg)
    return True




run_programs = {
    'read_records_count': call_read_records_count_program,
    'test': call_test_program,
}



def main():
    try:
        parser = argparse.ArgumentParser(
            description="Universal caller of mdmtoolsap-py utilities"
        )
        parser.add_argument(
            #'-1',
            '--program',
            choices=dict.keys(run_programs),
            type=str,
            required=True
        )
        args, args_rest = parser.parse_known_args()
        if args.program:
            program = '{arg}'.format(arg=args.program)
            if program in run_programs:
                run_programs[program]()
            else:
                raise AttributeError('program to run not recognized: {program}'.format(program=args.program))
        else:
            print('program to run not specified',file=sys.stderr)
            raise AttributeError('program to run not specified')
    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro()"
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print('{e}'.format(e=e),file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
