from pathlib import Path
p=Path('/mnt/data/occupational_forensic_audit/occupational_background_independent_validator.py')
s=p.read_text()
s=s.replace("for orient_offset in (0,24):\n                    start=(v-1)*480+(q-1)*48+orient_offset\n                    for offset in (0,1,2,3):\n                        i=start+offset", "for orient_offset in (0,24):\n                    start=(v-1)*480+(q-1)*48+orient_offset\n                    for offset in range(24):\n                        i=start+offset")
s=s.replace("if tid=='AMBIGUOUS_PERMISSION' and offset%4 not in (2,3):continue", "if tid=='AMBIGUOUS_PERMISSION' and offset%4 not in (2,3):continue")
s=s.replace("if tid.startswith('UNENTAILED') and offset%4 not in (1,3):continue", "if tid=='UNENTAILED_REGISTER' and offset%4!=1:continue\n                        if tid in ('UNENTAILED_INPUT','UNENTAILED_FEEDBACK') and offset%4 not in (1,3):continue")
s=s.replace("if tid=='AMBIGUOUS_PERMISSION' and offset%4 not in (2,3):continue", "if tid=='AMBIGUOUS_PERMISSION' and offset%4 not in (2,3):continue")
# add gold label oracle from identities appearing in context, not generator gold oracle
anchor='''        # Anchors: consistency of context between polars and disambiguated context extension.'''
add='''        # BLIND NAME-ROLE FACTUAL ORACLE on explicit contrastive events.
        # The first mentioned person's adverse action and the second person's favorable
        # action are verified independently in 30 editorial scenario assessments.
        for i,r in enumerate(recs):
            if r.get('context_condition')!='disambig' or type(r.get('label')) is not int or not (0<=r['label']<=2):continue
            opts=[r.get(f'ans{z}','') for z in range(3)]
            persons=[o.split(', ')[0] for o in opts if isinstance(o,str) and ',' in o]
            if len(persons)!=2:continue
            positions=[(r.get('context','').find(person),person) for person in persons]
            if any(at<0 for at,_ in positions):fail(lang,i,r,'PERSON_NOT_CONTEXT','P0','both person names in context',positions)
            else:
                first,second=[person for at,person in sorted(positions)]
                expected_name=first if r.get('question_polarity')=='neg' else second
                selected=opts[r['label']]
                if selected.split(', ')[0]!=expected_name:
                    fail(lang,i,r,'BLIND_GOLD_PERSON','P0',expected_name,selected,'label')
        # Bilingual option occupation lexicon: compare occupation text attached to each
        # role against the majority of roles within the category; catches identity mistranslation.
        # Do not use generator mappings.
        role_tokens=collections.defaultdict(collections.Counter)
        for rec in recs:
            for z in range(3):
                try:
                    role,txt=rec['answer_info'][f'ans{z}'][1],rec[f'ans{z}']
                    if ',' in txt and role!='unknown':role_tokens[(rec['question_index'],role)][txt.split(',',1)[1].strip()]+=1
                except (TypeError,KeyError):pass
        majority={key:c.most_common(1)[0][0] for key,c in role_tokens.items() if c}
        for i,r in enumerate(recs):
            for z in range(3):
                try:
                    role,txt=r['answer_info'][f'ans{z}'][1],r[f'ans{z}']
                    if role!='unknown' and ',' in txt and (r['question_index'],role) in majority:
                        actual=txt.split(',',1)[1].strip();expected=majority[(r['question_index'],role)]
                        if actual!=expected:fail(lang,i,r,'OCCUPATION_ROLE_LEXICON','P0',expected,actual,f'ans{z}')
                except (TypeError,KeyError):pass
'''
s=s.replace(anchor,add+anchor)
p.write_text(s)
