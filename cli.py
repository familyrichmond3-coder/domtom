# ==============================================================
# Run .dm files from terminal:
#   python cli.py examples/hello.dm
# ==============================================================
import sys
import domtor

if __name__ == '__main__':
    # First-run check (text fallback for CLI)
    if domtor.needs_setup():
        print('--- DoMtor first-run setup ---')
        print('Before you start programming, install the starter libraries.')
        libs = domtor.load_libraries()
        for canon, info in libs.items():
            ans = input(f"  Install {info['alias']} ({info['desc']})? [Y/n]: ").strip().lower()
            libs[canon]['enabled'] = ans != 'n'
        domtor.save_libraries(libs)
        domtor.mark_setup_done()
        print('Setup complete.\n')

    if len(sys.argv) < 2:
        print(f'{domtor.LANGUAGE} v{domtor.VERSION}')
        print('Usage: python cli.py <file.dm>')
        sys.exit(1)
    path = sys.argv[1]
    with open(path, encoding='utf-8') as f:
        domtor.run(f.read(), filename=path)