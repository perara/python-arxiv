import os
dir_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(dir_path, "categories.txt"), "r") as file:
    data = file.readlines()

structure = {}

for line in data:
    line = line.strip()
    splt = line.split(",", 1)

    # Original data
    key = splt[0]
    description = splt[1]

    # Create classes
    classes = key.split(".")
    last_class = []
    n_classes = len(classes)
    for i, clazz in enumerate(classes):
        is_last = i == n_classes
        original_clazz = clazz
        hyphens_pos = [pos for pos, char in enumerate(clazz) if char == "-"]
        clazz = clazz.replace("-", "")
        clazz = list(clazz)
        for hyphen in hyphens_pos:
            clazz[hyphen] = clazz[hyphen].upper()
        clazz = ''.join(clazz)

        last_class.append(clazz)

        struct = structure
        comb_clazz = []
        for l_c in last_class:
            comb_clazz.append(l_c)
            if l_c not in struct:
                struct[l_c] = {} if is_last else {"description": description, "value": ".".join(comb_clazz)}
            struct = struct[l_c]

    assert(len(splt) == 2)


# Create classes
def spaces(num=1):
    __ = ""
    for i in range(num):
        __ += "    "
    return __

def newline():
    return "\n"

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, [key] + pre):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, [key] + pre):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield indict

class_str = "class Subject:"
class_str += newline()



def walk(node, counter=1):
    global class_str

    for key, item in node.items():
        if isinstance(item, dict):
            class_str += newline() + spaces(counter + 1) + "class %s: " % (key)
            class_str += newline()
            walk(item, counter+1)
        else:
            class_str += spaces(counter + 1) + "%s = \"%s\"" % (key, item)
            class_str += newline()

for k, v in structure.items():

    class_str += newline() + spaces() + "class %s:" % (k)
    class_str += newline() + newline()

    walk(v)



with open(os.path.join(dir_path, "..", "subject.py"), "w") as f:
    f.write(class_str)