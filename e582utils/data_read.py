"""
  e582utils.data_read 
  ___________________

  downloads a file named filename from the atsc301 downloads directory
  and save it as a local file with the same name. 

  to run from the command line::

    python -m e582utils.data_read photon_data.csv

    or

    python -m e582utils.data_read A20162092016216.L3m_8D_PAR_par_9km.nc --root https://oceandata.sci.gsfc.nasa.gov/cgi/getfile

  to run from a python script::

    from e582utils.data_read import download
    download('photon_data.csv')

  or

    from e582utils.data_read import download
    root="https://oceandata.sci.gsfc.nasa.gov/cgi/getfile"
    filename="A20162092016216.L3m_8D_PAR_par_9km.nc"
    download(filename,root=root)

"""
import argparse
import requests
from pathlib import Path
import shutil

def download(filename,root='https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads'):
    """
    copy file filename from http://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads to 
    the local directory.  If local file exists, report file size and quit.

    
    Parameters
    ----------

    filename: string
      name of file to fetch from 

    Returns
    -------

    Side effect: Creates a copy of that file in the local directory
    """
    url = '{}/{}'.format(root,filename)
    print('trying {}'.format(url))
    filepath = Path('./{}'.format(filename))
    print('writing to: {}'.format(str(filepath)))
    if filepath.exists():
        the_size = filepath.stat().st_size
        print(('\n{} already exists\n'
               'and is {} bytes\n'
               'will not overwrite\n').format(filename,the_size))
        return None

    tempfile = str(filepath) + '_tmp'
    temppath = Path(tempfile)
    with open(tempfile, 'wb') as localfile:
        response = requests.get(url, stream=True)

        if not response.ok:
            print('response: ',response)
            raise Exception('Something is wrong, requests.get() failed with filename {}'.format(filename))

        for block in response.iter_content(1024):
            if not block:
                break

            localfile.write(block)
            
    the_size=temppath.stat().st_size
    if the_size < 10.e3:
        print('Warning -- your file is tiny (smaller than 10 Kbyte)\nDid something go wrong?')
    shutil.move(str(temppath),str(filepath))
    the_size=filepath.stat().st_size
    print('downloaded {}\nsize = {}'.format(filename,the_size))
    return None

def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    parser.add_argument('filename', type=str, help='name of file to download')
    parser.add_argument("--root", default="https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads",
                        help="root of url, detaults to https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads")
    return parser


if __name__ == "__main__":

    parser = make_parser()
    args=parser.parse_args()
    download(args.filename, root=args.root)
   
    


