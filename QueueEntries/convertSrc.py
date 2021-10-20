import stringcase, tokenize, pathlib, tqdm, os

os.system("mkdir -p converted/src/")
os.system("rm -rf converted/src/*")
os.system("cp -r src/* converted/src/")

IGNORE = {'dictConfig', 'Box'}

keywords = set()
source_path = pathlib.Path('converted/src/')

for filename in source_path.glob('**/*.py'):
    print(f'Scanning tokens {filename} ...')
    tokens = tokenize.tokenize(open(filename, 'rb').__next__)
    for token in tokens:
        if token.type == 1 or token.type == '3' and ' ' not in token.string:
            keywords.add(token.string)

print(len(keywords))
conversions = [(old, stringcase.snakecase(old) if old[0].islower() and old not in IGNORE else old) for old in keywords]

for filename in list(source_path.glob('**/*.py')) + list(source_path.glob('**/*.json')):
    print(f'Converting file {filename} ...')
    code = open(filename, 'r').read()
    for old, new in tqdm.tqdm(conversions, desc="Converting"):
        code = code.replace(old, new)
    with open(filename, 'w') as wfile:
        wfile.write(code)
print('Done')