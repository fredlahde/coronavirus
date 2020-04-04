def parse_csv_line(line):
    """
    csv parser which is capable to parse quoted strings with commas
    """
    ret = []
    tmp = ""
    in_quotes = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_quotes:
                in_quotes = False
                ret.append(tmp)
                tmp = ""
                i += 1
            else:
                in_quotes = True
        elif c != ",":
            tmp += c
        else:
            if not in_quotes:
                ret.append(tmp)
                tmp = ""
            else:
                tmp += c
        i += 1

    return ret
