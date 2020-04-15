import sys
import os
import json

from typing import Type, Iterator

__version__ = "0.1"

# f = CodeFile()
CHECKS = {
    "lineLength": {
        "check_function": lambda f, d: f.max_line_length(),
        "compare": lambda x, y: x < y
    }
}


class style():
    # Group of Different functions for different printing
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    chkmrk = f"{GREEN}✓{WHITE}"
    crs = f"{RED}✗{WHITE}"


class Config:
    '''Keep track of which options to have. Can construct from a file.'''
    config = []

    def read_from_file(self, file: str):
        '''Try to read file, throw error on failure'''
        raise NotImplementedError

    def set_default_config(self):
        '''Set the options to default'''
        self.config = [
            {'id': 'lineLength',            'data': 80},
            {'id': 'requireHeaderComment',  'data': True},
            {'id': 'requireFullStop',       'data': True}
        ]

    def get_config_options(self) -> Iterator:
        for n in self.config:
            yield n
        '''Set the options to default'''
        # raise NotImplementedError


class CodeFile:
    language = None
    filename = ""
    content = ""

    def __init__(self, filename):
        # TODO Implement this function.
        self.filename = filename

    def max_line_length(self):
        # TODO Implement this function.
        return 100


class CommandlineOptions:
    '''Get the file to check and the option config file.'''

    file_to_check = None
    config_file = None

    def parse_options(self, argv: list):
        # TODO Implement this function.
        raise NotImplementedError


class Check:
    # One type of check. For example the check if the lines are not too wide.
    check_function = staticmethod(lambda x, y: True)
    compare_function = staticmethod(lambda x, y: x == y)
    display_name = None
    crit_display = ""

    codefile = None
    required_result = None
    result = None
    passed = None

    def __init__(self, display_name: str, codefile: Type[CodeFile], crit_display: str = "result"):
        self.display_name = display_name
        self.crit_display = crit_display
        self.codefile = codefile

    def set_check(self, check_function, required_result, compare):
        self.check_function = check_function
        self.required_result = required_result
        self.compare_function = compare

    def check(self, data):
        self.result = self.check_function(self.codefile, data)
        self.passed: bool = self.compare_function(
            self.result, self.required_result)

    def print_ln(self):
        "Print a line with information regarding the result of the test."
        print(f"{self.display_name.ljust(40)}", end="")
        print(
            f"{(' - ' + self.crit_display + ' : ' + str(self.result)).ljust(37)}", end="")

        if self.passed:
            print(f"{style.chkmrk}")
        else:
            print(f"{style.crs}")


class Checker:

    config = None
    checks = []
    codefile = None

    def __init__(self, config: Type[Config], codefile: Type[CodeFile]):
        self.config = config
        self.codefile = codefile

    def set_checks(self):
        for config_option in self.config.get_config_options():
            chk = Check(config_option['id'], self.codefile)
            if config_option['id'] in CHECKS:
                chk_ops = CHECKS[config_option['id']]
                chk.set_check(
                    chk_ops['check_function'],
                    config_option['data'],
                    chk_ops['compare']
                )
            self.checks.append(chk)

    def check_all(self):
        ''' Execute all checks which are present in the Checker-object '''
        for c in self.checks:
            c.check(c)

    def print_result(self):
        total = 0
        passed = 0
        for c in self.checks:
            total += 1
            if c.passed:
                passed += 1
            c.print_ln()

        if passed == total:
            print(f" {'All passed'.ljust(75)} {style.chkmrk}")
        else:
            print(f"{'Failed some tests'.ljust(75)} {(passed/total):.2f}/1.00")

        return


def set_config(cli, cfg):
    # Set the config depending on the command line options.
    if cli.config_file == None:
        cfg.set_default_config()
    else:
        try:
            cfg.read_from_file(cli.config_file)
        except IOError:
            print(
                f"could not read {cli.config_file}. Falling back to default.")
            cfg.set_default_config()


def main():
    # cli = CommandlineOptions()
    cfg = Config()

    # cli.parse_options(sys.argv)

    # set_config(cli, cfg)
    cfg.set_default_config()
    codefile = CodeFile("a")
    chkr = Checker(cfg, codefile)
    chkr.set_checks()
    chkr.check_all()
    chkr.print_result()

    # raise NotImplementedError


if __name__ == "__main__":
    main()
    pass
