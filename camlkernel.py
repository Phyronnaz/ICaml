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
        l = self.caml_child.before.split("print_char (char_of_int 126);;")[1].replace("\r\n#", "\r\n").split('\r\n')
        r = l[0]
        if len(l) > 1:
            r = l[1]
            for s in l[2:-1]:
                r += "\r\n" + s
        return r

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not hasattr(self, "caml_child"):
            self.caml_child = pexpect.spawnu("/usr/bin/camllight -g")
            self.caml_child.expect('\r\n')
            self.caml_child.maxread = 10 ** 6
            self.count = 0

        if code.rstrip()[-2:] != ";;":
            code += ";"
            if code.rstrip()[-2:] != ";;":
                code += ";"
                
        self.count += 1

        self.caml_child.sendline(code + " \n print_char (char_of_int 126);;")
        self.caml_child.expect("#~- : unit = ()")

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
