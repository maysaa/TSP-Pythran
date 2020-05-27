
import sys
import subprocess as sp


def show_hardwre():
    """
    """
    cmd = {
        'darwin': 'sysctl hw.physicalcpu hw.logicalcpu',
        'linux': '',
    }
    if sys.platform == 'darwin':

        def exists(self, filename):
            """
            """
            li_cand = glob.glob(self.work_dir+f'/{filename}.*.so')
            return len(li_cand)

        def run(self, force=False):
            """
            """
            work_dir = os.path.dirname(__file__)
            print(f'compile dir = {self.work_dir}')

            for filename, cmd in self.dic_cmd.items():
                if not self.exists(filename) or force:
                    cmd = cmd.format(filename)
                    print(f'\ncommand: {cmd}')

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
