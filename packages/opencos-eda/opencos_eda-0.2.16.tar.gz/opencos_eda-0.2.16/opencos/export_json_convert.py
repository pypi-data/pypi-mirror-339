
'''Converts eda style export.json or export.jsonl to a format suitable for test runner schema.'''

import uuid
import json
import yaml
import argparse
import sys
import os

def convert(input_json_fname:str, output_json_fname:str) -> None:

    data = None
    new_tests_list = list()
    assert os.path.exists(input_json_fname), f'{input_json_fname=} does not exist'
    with open(input_json_fname) as f:

        if input_json_fname.lower().endswith('.jsonl'):
            data = list()
            for line in f.readlines():
                data.append(json.loads(line.rstrip()))
        else:
            data = json.load(f)

    if type(data) is dict and 'eda' in data:
        # 1 test, make it a list:
        data = [data]
    elif type(data) is dict and 'tests' in data and type(data['tests'])  is list:
        data = data['tests']


    assert data is not None and type(data) is list, f'unknown schmea for {input_json_fname=}'

    for test in data:

        new_test_item = {
            'top': '',
            'files_list': list(),
            'correlation_id': str(uuid.uuid4()),
        }

        assert 'files' in test
        for entry in test['files']:
            new_test_item['files_list'].append({
                'filename': entry['name'],
                'content': entry['content'],
            })

            # load the DEPS.yml (from str) to find the value for 'top', because reasons.
            if entry['name'] == 'DEPS.yml':
                yaml_str = entry['content']
                deps_data = yaml.safe_load(yaml_str)
                assert len(deps_data.keys()) == 1
                #print(f'{deps_data=}')
                target_entry = deps_data[list(deps_data.keys())[0]]
                #print(f'{target_entry=}')
                top = target_entry.get('top', '')
                if not top:
                    # then pick the last file?
                    top = target_entry.get('deps', [''])[-1]
                #print(f'{top=}')
                assert top
                new_test_item['top'] = top


        new_tests_list.append(new_test_item)

    new_data = {
        'tests': new_tests_list
    }

    with open(output_json_fname, 'w') as f:
        json.dump(new_data, f)

    print(f'Wrote: {output_json_fname=}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='export_json_convert', add_help=True, allow_abbrev=False)

    parser.add_argument('--input-json', '-i', type=str)
    parser.add_argument('--output-json', '-o', type=str)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    parsed, unparsed = parser.parse_known_args(sys.argv[1:])

    if not parsed.input_json or not parsed.output_json:
        parser.print_help()
        sys.exit(1)

    convert(parsed.input_json, parsed.output_json)
