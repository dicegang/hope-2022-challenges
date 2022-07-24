from pathlib import Path
import re
import json
import random


IDENTIFIER_REGEX = re.compile(r'\\[A-Z][a-zA-Z]*')


def collect_identifiers(code: str) -> list[str]:
    return sorted({x for x in IDENTIFIER_REGEX.findall(code)})


def load_names(path: Path) -> list[str]:
    with path.open('r') as f:
        raw = json.load(f)

    def clean(name: str) -> str:
        try:
            name.encode('ascii') # assert ascii
        except UnicodeEncodeError:
            raise ValueError(f'bad name: "{name}"')
        return ''.join(s.capitalize() for s in name.split())

    return [clean(name) for name in raw]

def create_identifier_map(identifiers: list[str], names: list[str]) -> dict[str, str]:
    mangle_map = dict()
    used_names: set[str] = set()
    for ident in identifiers:
        assert ident[0] == '\\'
        while (mangled := random.choice(names)) in used_names:
            if len(names) == len(used_names):
                raise ValueError('ran out of names to substitute')
        used_names.add(mangled)
        mangle_map[ident] = f'\\{mangled}'
    return mangle_map


MINIFY_DIRECTIVE_REGEX = re.compile(r'^\s*%\s*minifier\s+(.*)$')

def minify(code: str) -> str:
    enabled = True
    hidden = False
    output = ''
    for line in code.splitlines(keepends=False):
        if directive := MINIFY_DIRECTIVE_REGEX.match(line):
            match directive.group(1):
                case 'off':
                    enabled = False
                case 'on':
                    enabled = True
                case 'hide':
                    hidden = True
                case 'unhide':
                    hidden = False
            continue
        if hidden:
            continue
        if enabled:
            output += minify_line(line)
        else:
            output += '\n' + line
    if output[-1] != '\n':
        output += '\n'
    return output

# Stupid regex that should be good enough for our uses
COMMENT_REGEX = re.compile(r'(\s|^)%.*$')
WS_REGEX = re.compile(r'\s')

def minify_line(line: str) -> str:
    return WS_REGEX.sub('', COMMENT_REGEX.sub('', line))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', type=Path, required=True)
    parser.add_argument('--minify', action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path, nargs='?')
    parser.add_argument('--mangle-map-out', type=Path)
    parser.add_argument('--seed', type=int, default=0xd1ce)
    args = parser.parse_args()

    random.seed(args.seed)
    names = load_names(args.names)
    code: str = args.input.read_text()
    identifiers = collect_identifiers(code)
    mangle_map = create_identifier_map(identifiers, names)
    code_mangled = code
    for orig_ident, new_ident in mangle_map.items():
        code_mangled = re.sub(rf'\\{orig_ident[1:]}\b', lambda _: new_ident, code_mangled)
    if args.mangle_map_out:
        with args.mangle_map_out.open('w') as f:
            json.dump(mangle_map, f, indent=2)

    if args.minify:
        code_mangled = minify(code_mangled)

    if args.output:
        args.output.write_text(code_mangled)
    else:
        print(code_mangled, end='')
