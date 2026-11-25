from engine import Retriever,load_sample,answer_question,grievance,chunk
from evaluate import run

def test_noc():
    hits=Retriever(load_sample()).search('internship NOC')
    assert hits[0][0].category=='Internship'
    assert '[S1]' in answer_question('internship NOC',hits)

def test_abstain():
    assert not Retriever(load_sample()).search('quantum entanglement')
    assert 'Insufficient evidence' in answer_question('unknown',[])

def test_letter():
    assert 'paid twice' in grievance('paid twice','Finance Office')

def test_chunk():
    assert len(chunk('word '*400))==4

def test_benchmark():
    assert run()['accuracy']>=.85
