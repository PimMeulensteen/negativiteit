from check_config_less import Check


def getlinecount(_, x):
    return x*2


def eq(x, y):
    return x == y


def gt(x, y):
    return x > y


def main():
    check = Check("Test check. Data should be greater than 0")
    check.set_check(getlinecount, 0, gt)
    check.check(10)
    check.print_ln()
    check.check(-10)
    check.print_ln()


if __name__ == "__main__":
    main()
