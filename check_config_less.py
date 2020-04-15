import sys
import os
import json

from typing import Type, Iterator, Callable, List, Any

__version__ = "0.1"

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

    checkmark = f"{GREEN}✓{WHITE}"
    crs = f"{RED}✗{WHITE}"


class Config:
    '''Keep track of which options to have. Can construct from a file.'''
    config: List[dict] = []

    def read_from_file(self, file: str):
        ''' Try to read file, throw error on failure. '''
        raise NotImplementedError

    def set_default_config(self):
        ''' Set the options to default. '''
        self.config = [
            {'id': 'lineLength',            'data': 80},
            {'id': 'requireHeaderComment',  'data': True},
            {'id': 'requireFullStop',       'data': True}
        ]

    def get_config_options(self) -> Iterator:
        ''' Iterator over all set options. '''
        for n in self.config:
            yield n


class CodeFile:
    language = None
    filename = ""
    fileobj = None
    content = ""

    def __init__(self, filename: str):
        # TODO Implement this function.
        self.filename = filename
        self.fileobj = open(filename)
        self.content = self.fileobj.read()

    def max_line_length(self) -> int:
        return max([len(x) for x in self.content.split("\n")])


class CommandlineOptions:
    '''Get the file to check and the option config file.'''

    file_to_check = None
    config_file = None

    def parse_options(self, argv: list):
        # TODO Implement this function.
        # Check if there is at least one argument.
        if len(argv) < 2:
            raise ValueError("Expected at least one argument, got 0")

        self.file_to_check = argv[1]


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

    def __init__(self, display_name, codefile, crit_display="result"):
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
        print(f" - {self.crit_display} : {self.result}".ljust(37), end="")

        if self.passed:
            print(f"{style.checkmark}")
        else:
            print(f"{style.crs}")


class Checker:
    '''
    Object to keep track of all Checks which need to be executed. Can run
    all checks and print their results.
    '''
    config = None
    checks: List[Type[Check]] = []
    codefile = None

    def __init__(self, config: Type[CodeFile], codefile: Type[CodeFile]):
        self.config = config
        self.codefile = codefile

    def set_checks(self):
        for config_option in self.config.get_config_options():
            if config_option['id'] in CHECKS:
                chk = Check(config_option['id'], self.codefile)
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
            print(f"{'All passed'.ljust(76)} {style.checkmark}")
        else:
            print(f"{'Failed'.ljust(75)} {(passed/total):.2f}/1.00")

        return


def set_config(cli: Type[CommandlineOptions], cfg: Type[Config]):
    # Set the config depending on the CommandlineOptions line options.
    if cli.config_file is None:
        cfg.set_default_config()
    else:
        try:
            cfg.read_from_file(cli.config_file)
            return
        except IOError:
            print(
                f"could not read {cli.config_file}. Falling back to default.")
    cfg.set_default_config()


def main():
    cli = CommandlineOptions()
    cfg = Config()

    cli.parse_options(sys.argv)
    codefile = CodeFile(cli.file_to_check)
    set_config(cli, cfg)
    chkr = Checker(cfg, codefile)
    chkr.set_checks()
    chkr.check_all()
    chkr.print_result()

    # raise NotImplementedError


if __name__ == "__main__":
    main()
    pass
