import json
import argparse

def convert_entry(itm, intent):
    text = ''.join([d['text'] for d in itm['data']])
    entities = []
    text = ''
    for el in itm['data']:
        etxt = el['text']
        if "\ufffd" in etxt:
            print('Warning: replacing unknown char in {} [{}]'.format(etxt, text))
            etxt = etxt.replace("\ufffd","")
        if 'entity' in el:
            entities.append({'start': len(text),
                             'end': len(text)+len(etxt),
                             'value': etxt,
                             'entity': el['entity']})
        text += etxt
    res = {'intent': intent, 'text': text, 'entities': entities}
    return res

def convert(input_path, output_path):
    with open(input_path, errors='replace') as f:
        data = json.load(f)
    assert len(data.keys()) == 1
    key = list(data.keys())[0]
    output = {'rasa_nlu_data':{
        'common_examples':[convert_entry(itm, key) for itm in data[key]]
    }}
    with open(output_path, 'w') as f:
        json.dump(output, f, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description="Convert to Rasa NLU format",
                usage="snips_nlu_benchmark.py <input_file> <output_file>")
    parser.add_argument('input_file', help='Input file')
    parser.add_argument('output_file', help='Output file')
    args = parser.parse_args()
    convert(args.input_file, args.output_file)
    print('Converted results saved in {}'.format(args.output_file))
