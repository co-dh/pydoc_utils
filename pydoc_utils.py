import inspect
from pydoc import ModuleScanner, visiblename, locate, ErrorDuringImport, allmethods

def getmodules():
    """get all built-in modules and installed"""
    modules = {}
    def callback(path, modname, desc, modules=modules):
        if modname and modname[-9:] == '.__init__':
            modname = modname[:-9] + ' (package)'
        if modname.find('.') < 0:
            modules[modname] = 1
    def onerror(modname):
        callback(None, modname, None)
    ModuleScanner().run(callback, onerror=onerror)
    return modules


def getclasses(module):
    try:
        module = locate(module)
    except ErrorDuringImport:
        return []
    all = getattr(module, '__all__', None)
    classes = []
    for key, value in inspect.getmembers(module, inspect.isclass):
        # if __all__ exists, believe it.  Otherwise use old heuristic.
        if (all is not None
            or (inspect.getmodule(value) or module) is module):
            if visiblename(key, all, module):
                classes.append((key, value))
    return classes


def getfuncs(module):
    try:
        module = locate(module)
    except ErrorDuringImport:
        return []
    all = getattr(module, '__all__', None)
    funcs = []
    for key, value in inspect.getmembers(module, inspect.isroutine):
        # if __all__ exists, believe it.  Otherwise use old heuristic.
        if (all is not None or
                inspect.isbuiltin(value) or inspect.getmodule(value) is module):
            if visiblename(key, all, module):
                funcs.append((key, value))
    return funcs

def _fullname(module, name):
    return module + '.' + name if module != 'builtins' else name

def getall():
    "get all modules, classes, functions"
    all = []
    ms = getmodules()

    all += [m for m in ms if m != 'setup']
    for m in ms:
        if m in 'setup this antigravity'.split():
            continue
        if m.startswith('_'):
            continue
        clss = getclasses(m)

        for name, cls in clss:
            try:
                all += [ _fullname(m, name) + '.' +  x for x in allmethods(cls).keys() if not x.startswith('_')]
            except AttributeError:
                pass
        all += [_fullname(m, x[0]) for x in clss ]
        all += [_fullname(m, x[0]) for x in getfuncs(m)]

    return list(filter(lambda x: not x.startswith('_'), sorted(list(set(all)))))

def main():
    print('\n'.join(getall()))

if __name__ == '__main__':
    main()
