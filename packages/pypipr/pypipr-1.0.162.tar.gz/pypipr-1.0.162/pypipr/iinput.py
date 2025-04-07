import sys

args = sys.argv
args_iter = iter(sys.argv)


def iinput(msg=None, default=None):
    """
    improve input() function, dengan mengecek argv terlebih dahulu,
    jika tersedia maka gunakan argv,
    """
    global args_iter

    # RESET: buat iterator baru
    if msg is None:
        args_iter = iter(args)

    try:
        return next(args_iter)
    except StopIteration:
        return input(msg or "") or default
