
import os
import sys
import glob
import subprocess as sp


class Compiler:
    """
    """

    def __init__(self):
        """
        """
        self.work_dir = os.path.dirname(__file__)

        if sys.platform == 'win32':
            self.dic_cmd = {
                'tsp_compute_single_threaded': 'pythran {}.py',
                'tsp_compute_multi_threaded_omp': 'pythran -DUSE_XSIMD -fopenmp {}.py',
            }

        else:
            self.dic_cmd = {
                'tsp_compute_single_threaded': 'pythran -Ofast -march=native {}.py',
                'tsp_compute_multi_threaded_omp': 'pythran -DUSE_XSIMD -fopenmp -march=native {}.py',
            }

    def exists(self, filename):
        """
        """
        li_cand_so = glob.glob(self.work_dir+f'/{filename}.*.so')
        li_cand_pyd = glob.glob(self.work_dir+f'/{filename}.*.pyd')
        li_cand = li_cand_so + li_cand_pyd
        return len(li_cand)

    def run(self, force=False):
        """
        """
        work_dir = os.path.dirname(__file__)
        print(f'compile dir = {self.work_dir}')
        flag = False
        for filename, cmd in self.dic_cmd.items():
            if not self.exists(filename) or force:
                cmd = cmd.format(filename)
                print(f'\ncommand: {cmd}')
                flag = True

                p = sp.Popen(cmd,
                             stdout=sp.PIPE,
                             shell=True,
                             cwd=work_dir)
                res = p.communicate()

                stdout = res[0]
                if stdout is not None:
                    stdout = stdout.decode('utf-8')

                stderr = res[1]
                if stderr is not None:
                    stderr = stderr.decode('utf-8')

                print(f'stdout = {stdout}\nstderr = {stderr}')

            else:
                print(f'{filename} already compiled')

        if flag:
            print(f'\nrestart kernel to use native modules')

    def remove(self):
        """
        """
        li_compiled_so = glob.glob(self.work_dir+f'/tsp_compute_*.so')
        li_compiled_pyd = glob.glob(self.work_dir+f'/tsp_compute_*.pyd')
        li_compiled = li_compiled_so + li_compiled_pyd
        # print(li_compiled)

        for c in li_compiled:
            os.remove(c)

        li_filename = [os.path.basename(e) for e in li_compiled]
        if len(li_filename):
            print(f'removed from disk:')
            for e in li_filename:
                print(f'\t{e}')
            print(f'restart kernel to use Python modules')

        else:
            print(f'no native modules to remove')
