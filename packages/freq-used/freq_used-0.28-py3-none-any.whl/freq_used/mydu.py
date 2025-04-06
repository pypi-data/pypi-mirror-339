from typing import Dict
import os
from logging import Logger, getLogger

from freq_used.logging_utils import set_logging_basic_config

logger: Logger = getLogger()


def is_yes(msg: str) -> bool:
    answer: str = input(msg)
    logger.info(f"{msg}{answer}")

    return answer.lower().startswith("y")


def add_commas(num: int, num_digits: int = 3, delim: str = ",") -> str:
    num_str = str(num)

    str_list = []
    while len(num_str):
        str_list.append(num_str[-num_digits:])
        num_str = num_str[:-num_digits]

    str_list.reverse()

    return delim.join(str_list)


def mydu() -> None:
    set_logging_basic_config(__file__)

    while True:
        d = input("directory? ")
        logger.info(f"directory? {d}")
        if len(d) == 0:
            break

        d = os.path.abspath(d)

        sort_by_ext: Dict[str, int] = {}

        dir_names = []
        dir_sizes = []
        file_number_list = []
        cnt = 1
        number_of_errors = 0
        for root, dirs, files in os.walk(d, followlinks=True):
            dir_names.append(root)
            try:
                dir_sizes.append(sum([os.path.getsize(os.path.join(root, name)) for name in files]))
            except (FileNotFoundError, OSError):
                dir_sizes.append(0)
                number_of_errors += 1

            file_number_list.append(len(files))

            for file in files:
                r, e = os.path.splitext(file)

                if e in sort_by_ext:
                    sort_by_ext[e] += 1
                else:
                    sort_by_ext[e] = 1

            print(f"\r{cnt}", end="")
            cnt += 1

        print("")
        logger.info(f"{cnt - 1} directories...")
        logger.info(f"Errors occurred in {number_of_errors} directories...")

        n = len(dir_names)

        if n == 0:
            continue

        assert len(dir_sizes) == n
        assert len(file_number_list) == n

        assert dir_names[0] == d
        dir_size_dict = {"": dir_sizes[0]}
        total_size = dir_sizes[0]

        dir_name_length = len(d)

        if d[-1] == os.path.sep:
            dir_name_length -= 1

        for i in range(1, n):
            dir_name = dir_names[i]
            dir_size = dir_sizes[i]

            assert len(dir_name) > dir_name_length
            rel_name = dir_name[dir_name_length + 1:]

            depth1_subdir, sep, tail = rel_name.partition(os.path.sep)

            if (depth1_subdir) in dir_size_dict:
                dir_size_dict[depth1_subdir] += dir_size
            else:
                dir_size_dict[depth1_subdir] = dir_size

            total_size += dir_size

        max_length = len(add_commas(total_size))
        logger.info(add_commas(total_size))

        dir_list = [(dirname, dir_size_dict[dirname]) for dirname in dir_size_dict]

        def cmp(x, y, kind):
            if kind == "name":
                x = x[0].lower()
                y = y[0].lower()
            elif kind == "size":
                x = x[1]
                y = y[1]
            else:
                assert False

            if x < y:
                return -1
            elif x > y:
                return 1
            else:
                return 0

        if is_yes("sort by name? "):
            dir_list.sort(key=lambda x: x[0])
        else:
            dir_list.sort(key=lambda x: x[1])

        for dir_name, size in dir_list:
            logger.info(f"{add_commas(size).rjust(max_length)} {os.curdir}{os.path.sep}{dir_name}")

        keys = list(sort_by_ext.keys())
        keys.sort()

        logger.info("")
        if is_yes("Do you want to print # files for each extension? "):
            for key in keys:
                logger.info("{key}: {sort_by_ext[key}")

        logger.info("")


if __name__ == "__main__":
    mydu()
