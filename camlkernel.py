import pexpect
import os
import io
import sys
from ipykernel.ipkernel import Kernel
from pygments.lexers import LEXERS
from IPython.utils.tokenutil import token_at_cursor, line_at_cursor


class CamlKernel(Kernel):
    implementation = 'Caml Light'
    implementation_version = '1.0'
    language = 'camllight'
    language_version = '0.1'
    language_info = \
        {
            "name": "camllight",
            "file_extension": ".ml",
            "pygments_lexer": "OcamlLexer",
            "version": "1.0",
            "codemirror_mode":
                {
                    "name": "mllike"
                },
            "mimetype": "text/x-ocaml"
        }
    banner = "Caml Light banner"

    def get_output(self):
        try:
            self.caml_child.logfile_read.seek(0)
            s = self.caml_child.logfile_read.read()
            l = s.replace("\r\n#", "\r\n").split("print_char (char_of_int 127) ;;")[1].split("- : unit = ()")[0]
            self.caml_child.logfile_read.close()
            self.caml_child.logfile_read = io.StringIO()
            return l
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            try:
                print(self.caml_child.logfile_read.read())
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not hasattr(self, "caml_child"):
            self.count = 0
            self.caml_child = pexpect.spawnu("/usr/bin/camllight -g", maxread=100000, searchwindowsize=100,
                                             timeout=None)
            self.caml_child.logfile_read = io.StringIO()

        self.count += 1

        if code.rstrip()[-2:] not in [";;", "*)"]:
            code += ";"
            if code.rstrip()[-2:] != ";;":
                code += ";"

        code += '\nprint_char (char_of_int 127) ;;'

        self.caml_child.sendline(code)
        self.caml_child.expect(chr(127))

        if not silent:
            stream_content = {'name': 'stdout', 'text': self.get_output()}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.count,
                'payload': [],
                'user_expressions': {},
                }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=CamlKernel)
