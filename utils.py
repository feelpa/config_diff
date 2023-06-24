from collections import OrderedDict


def recursively_order_dict(dictionary):
    if isinstance(dictionary, dict):
        ordered_dict = OrderedDict()
        for key in sorted(dictionary.keys()):
            ordered_dict[key] = recursively_order_dict(dictionary[key])
        return ordered_dict
    elif isinstance(dictionary, list):
        return [recursively_order_dict(item) for item in dictionary]
    else:
        return dictionary


def prettyprint(d, offset=0, indent=4, filename="output.txt"):
    empty_str = ""

    def write_line(line):
        with open(filename, 'a') as file:
            file.write(line + "\n")

    def write_value(fields, value):
        line = '{0}{1} {2}'.format(empty_str.rjust(offset), ' '.join(fields), value)
        write_line(line)

    def write_multiline_value(value):
        for line in value:
            write_line(line + '\r')

    def write_section_header(fields):
        line = '{0}{1}'.format(empty_str.rjust(offset), ' '.join(fields))
        write_line(line)

    def write_section_footer(method):
        if method == 'config':
            line = empty_str.rjust(offset) + 'end'
        elif method == 'edit':
            line = empty_str.rjust(offset) + 'next'
        write_line(line)

    if d.get("config global") and d.get("config vdom"):
        for k, v in d.items():
            if v == {}:
                write_line(k)
        write_line("")
        write_line("config vdom")
        for k, _ in d["config vdom"].items():
            write_line(k)
            write_line("next")
        write_line("end")
        write_line("")
        write_line("config global")
        prettyprint(d["config global"], filename=filename)
        write_line("end")
        for k, v in d["config vdom"].items():
            write_line("")
            write_line("config vdom")
            write_line(k)
            prettyprint(v, offset=offset, indent=indent, filename=filename)
            write_line("end")
    else:
        for k, v in d.items():
            if isinstance(v, dict):  # sub-section
                fields = k.strip().split(" ")
                method = fields[0]
                write_section_header(fields)  # print sub-section header
                prettyprint(v, offset + indent, filename=filename)  # print sub-section
                if method == "config":
                    write_section_footer(method)  # print sub-section footer
                elif method == "edit":
                    write_section_footer(method)  # print sub-section footer
            else:  # leaf
                if k == "":
                    return
                fields = k.strip().split(" ")
                if len(v):
                    write_value(fields, v[0])  # print value
                    for xx in range(1, len(v)):  # print multiline value if exists
                        write_line(v[xx] + '\r')
                else:
                    write_line('{0}{1}'.format(empty_str.rjust(offset), ' '.join(fields)))  # print unset without value
