import json
from pathlib import Path
from engine import Retriever,load_sample

def run():
    data=Path(__file__).parent/'data'
    r=Retriever(load_sample()); rows=[]
    for item in json.loads((data/'evaluation_dataset.json').read_text()):
        hits=r.search(item['query']); pred=hits[0][0].category if hits else 'Abstain'
        rows.append({'Query':item['query'],'Expected':item['expected_category'],'Predicted':pred,'Correct':pred==item['expected_category']})
    o=json.loads((data/'out_of_scope.json').read_text())
    return {'accuracy':sum(x['Correct'] for x in rows)/len(rows),'abstention':sum(not r.search(q) for q in o)/len(o),'rows':rows}
if __name__=='__main__':
    result=run(); print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
    for row in result['rows']:
        if not row['Correct']: print(row)
