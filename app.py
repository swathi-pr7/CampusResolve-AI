import os, json
from pathlib import Path
import streamlit as st
from engine import Retriever, load_sample, load_upload, answer_question, grievance

st.set_page_config(page_title='CampusResolve AI',page_icon='🎓',layout='wide')
st.markdown('''<style>.block-container{max-width:1100px;padding-top:2rem} .hero{background:linear-gradient(120deg,#10243d,#205c69);padding:28px;border-radius:16px;color:white;margin-bottom:20px}.hero h1{color:white;margin:0;font-size:2.2rem}.hero p{color:#d9ecee;margin:8px 0 0} </style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>CampusResolve AI</h1><p>Student support • Evidence-based answers • Grievance drafting</p></div>',unsafe_allow_html=True)
local_key_file=Path(__file__).resolve().parent / '.gemini_key'
configured_key=os.getenv('GEMINI_API_KEY','').strip()
if not configured_key and local_key_file.is_file():
    configured_key=local_key_file.read_text(encoding='utf-8').strip()
with st.sidebar:
    st.header('Workspace settings')
    mode=st.radio('Generation mode',['Offline demo (retrieval + template)','Live Gemini LLM'],index=1 if configured_key else 0)
    key=st.text_input('Gemini API key',value=configured_key,type='password') if mode.startswith('Live') else ''
    model=st.text_input('Gemini model','gemini-2.5-flash') if mode.startswith('Live') else 'gemini-2.5-flash'
    use_sample=st.checkbox('Include synthetic sample policies',True)
    files=st.file_uploader('Upload official policy PDFs or TXT files',type=['pdf','txt'],accept_multiple_files=True)
    st.caption('Live mode sends your question and retrieved passages to Google. Do not enter sensitive personal information. Offline mode makes no API calls.')
passages=load_sample() if use_sample else []
for file in files:
    try:
        if file.size>10*1024*1024: raise ValueError('Maximum 10 MB per file.')
        added=load_upload(file)
        if not added: st.sidebar.warning(f'{file.name}: no extractable text. Scanned PDFs require OCR outside this app.')
        passages.extend(added)
    except Exception as e: st.sidebar.error(f'{file.name}: {e}')
try: retriever=Retriever(passages)
except ValueError:
    st.warning('No usable document terms. Upload a readable policy.'); retriever=Retriever([])
a,b,c=st.columns(3)
a.metric('Knowledge passages',len(passages)); b.metric('Document sources',len(set(p.source for p in passages))); c.metric('Mode','Live LLM' if key else 'Offline')
if use_sample: st.warning('Sample policies are synthetic, not official university rules. Disable them when using verified university documents.')
if mode.startswith('Live') and not key: st.info('Enter an API key to activate live generation. Requests otherwise remain offline.')
t1,t2,t3=st.tabs(['Ask CampusResolve','Draft a grievance','Evaluation & knowledge base'])
with t1:
    st.subheader('What can we help you resolve?')
    st.caption('Example: How do I get an internship NOC?')
    with st.form('question'):
        question=st.text_area('Your question',max_chars=2000,placeholder='Describe your university-related question…')
        submitted=st.form_submit_button('Find answer',type='primary')
    if submitted:
        if not question.strip(): st.warning('Enter a question.')
        else:
            hits=retriever.search(question)
            with st.spinner('Retrieving evidence and preparing your answer…'):
                try: response=answer_question(question,hits,key,model)
                except Exception as e:
                    st.error(str(e)); response=answer_question(question,hits)
            st.session_state['result']=(response,hits)
    if 'result' in st.session_state:
        response,hits=st.session_state['result']
        st.markdown('### Response'); st.markdown(response)
        if hits:
            st.markdown('### Retrieved evidence')
            for i,(p,s) in enumerate(hits,1):
                with st.expander(f'[S{i}] {p.source} — similarity {s:.3f}'):
                    st.write(p.text)
            st.caption('Similarity is a lexical retrieval score, not a probability of correctness. Citations are checked for valid IDs, not semantic entailment.')
        st.download_button('Download response',response,'campus_answer.txt')
with t2:
    st.subheader('Create a professional grievance letter')
    with st.form('letter'):
        issue=st.text_area('Describe the issue (avoid personal identifiers)',max_chars=2000)
        department=st.selectbox('Department',['Auto-suggest']+sorted(set(p.department for p in passages)))
        generate=st.form_submit_button('Generate draft',type='primary')
    if generate:
        if not issue.strip(): st.warning('Describe your issue first.')
        else:
            hits=retriever.search(issue)
            target=department if department!='Auto-suggest' else (hits[0][0].department if hits else 'Appropriate university office')
            try: letter=grievance(issue,target,key,model)
            except Exception as e: st.error(str(e)); letter=grievance(issue,target)
            st.session_state['letter']=letter
            st.session_state['editable_letter']=letter
    if 'letter' in st.session_state:
        st.text_area('Review your draft',height=320,key='editable_letter')
        st.download_button('Download edited letter',st.session_state['editable_letter'],'grievance_letter.txt')
        st.caption('Review and submit yourself. The app does not send complaints.')
with t3:
    st.subheader('Retrieval benchmark')
    st.caption('The benchmark always uses the bundled synthetic data, not your uploads. It measures retrieval, not LLM accuracy.')
    if st.button('Run benchmark'):
        from evaluate import run
        result=run(); st.metric('Top-1 category accuracy',f"{result['accuracy']:.1%}"); st.metric('Out-of-scope abstention',f"{result['abstention']:.1%}"); st.dataframe(result['rows'],use_container_width=True)
    st.subheader('Current knowledge base')
    for p in passages:
        with st.expander(p.source): st.write(p.text)
