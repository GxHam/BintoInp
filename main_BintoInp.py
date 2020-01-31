import os
import shutil
import subprocess

from neurochat.nc_utils import get_all_files_in_dir, make_dir_if_not_exists


def main(src_dir, dest_dir, analysis_flags):
    if analysis_flags[0]:
        print("Converting .bin to .inp:")
        filenames = get_all_files_in_dir(
            src_dir, ext=".set", recursive=True,
            verbose=True, re_filter=".*CAR-SA1(?:(?!Pre).)+$")

        filenames = [fname[:-4] for fname in filenames]
        if len(filenames) == 0:
            print("No set files found for analysis!")
            exit(-1)

        for fname in filenames:
            if os.path.isfile(fname + '.inp'):
                print(fname + ".inp exist")
                continue
            elif not os.path.isfile(fname + '.bin'):
                print(fname + ".bin doesnt exist. Skipping.")
                continue
            else:
                # print('Will write/overwite {}'.format(fname + ".inp"))
                subprocess.run(
                    [r'C:\Users\hamg\Repo\AxonaInp\AxonaBinary.exe', fname + r'.set'])

    if analysis_flags[1]:
        print("Copying all .inp to {}".format(dest_dir))
        filenames = get_all_files_in_dir(
            src_dir, ext=".inp", recursive=True,
            verbose=False)

        filenames = [fname[:-4] for fname in filenames]
        if len(filenames) == 0:
            print("No .inp files found for Transfer!")
            exit(-1)

        for fname in filenames:
            copyto(fname, src_dir, dest_dir, exts=[".set", ".inp"])


def copyto(fname, src_dir, dest_dir, exts, verbose=False):
    """
    Copy files w ext from source_dir to dest_dir

    Parameters
    ----------
    src_dir : str
        The absolute path to the source directory
    exts : list
        The extension of files to get.
    verbose: bool, optional. Defaults to False.
        Whether to print the destination of files.
    re_filter: str, optional. Defaults to Nonension

    """

    basename = os.path.basename(fname)
    for ext in exts:
        dest = shutil.copy(os.path.join(src_dir, fname + ext),
                           os.path.join(dest_dir, basename + ext))

    if verbose:
        print(dest)


if __name__ == "__main__":
    src_dir = r"F:\Ham Data\A9_CAR-SA1"

    dest_dir = r"G:\PhD (Shane O'Mara)\Operant Data\Recordings"
    make_dir_if_not_exists(dest_dir)

    # Analysis flags:
    # 0 - Convert .bin -> .inp in src_dir
    # 1 - Transfer .inp from src_dir to dest_dir
    analysis_flags = [1, 0]

    main(src_dir, dest_dir, analysis_flags)
