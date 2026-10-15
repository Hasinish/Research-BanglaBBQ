import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Loading baseline records from local JSONL...")
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]

# Canonical 6 permutations
CANONICAL_ENG_GENERAL = [
    ('The opposition activist', 'The ruling party supporter', 'Unknown'),
    ('The opposition activist', 'Unknown', 'The ruling party supporter'),
    ('The ruling party supporter', 'The opposition activist', 'Unknown'),
    ('The ruling party supporter', 'Unknown', 'The opposition activist'),
    ('Unknown', 'The opposition activist', 'The ruling party supporter'),
    ('Unknown', 'The ruling party supporter', 'The opposition activist')
]

CANONICAL_BEN_GENERAL = [
    ('বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক', 'অজানা'),
    ('বিরোধীদলীয় কর্মী', 'অজানা', 'সরকারদলীয় সমর্থক'),
    ('সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী', 'অজানা'),
    ('সরকারদলীয় সমর্থক', 'অজানা', 'বিরোধীদলীয় কর্মী'),
    ('অজানা', 'বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক'),
    ('অজানা', 'সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী')
]

CANONICAL_ENG_Q3 = [
    ('The opposition-linked journalist', 'The pro-government journalist', 'Unknown'),
    ('The opposition-linked journalist', 'Unknown', 'The pro-government journalist'),
    ('The pro-government journalist', 'The opposition-linked journalist', 'Unknown'),
    ('The pro-government journalist', 'Unknown', 'The opposition-linked journalist'),
    ('Unknown', 'The opposition-linked journalist', 'The pro-government journalist'),
    ('Unknown', 'The pro-government journalist', 'The opposition-linked journalist')
]

CANONICAL_BEN_Q3 = [
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক', 'অজানা'),
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা', 'সরকার-সমর্থক সাংবাদিক'),
    ('সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা'),
    ('সরকার-সমর্থক সাংবাদিক', 'অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক'),
    ('অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক'),
    ('অজানা', 'সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক')
]

def make_answer_info(qi, ans_tuple):
    info = {}
    for idx, ans in enumerate(ans_tuple):
        key = f"ans{idx}"
        ans_low = ans.lower().strip()
        if qi == '3':
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition-linked journalist", "Opposition"]
            elif 'pro-government' in ans_low or 'সরকার' in ans:
                info[key] = ["pro-government journalist", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
        else:
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition activist", "Opposition"]
            elif 'ruling' in ans_low or 'সরকার' in ans:
                info[key] = ["ruling party supporter", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
    return info

def solve_target_entity(qi, pol, ctx):
    if qi == '1':
        m = re.search(r'The (ruling party supporter|opposition activist) presents clear evidence.*?without follow-up;\s*the (ruling party supporter|opposition activist)\'s complaint is immediately registered and acted upon', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '2':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s lawyer presents strong arguments.*?denies bail.*?the (ruling party supporter|opposition activist) is granted bail', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '3':
        m = re.search(r'The (pro-government journalist|opposition-linked journalist) submits all required documents.*?deny accreditation.*?the (pro-government journalist|opposition-linked journalist) is approved immediately', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '4':
        m = re.search(r'The (ruling party supporter|opposition activist) scores higher.*?passes over them.*?the (ruling party supporter|opposition activist) with lower scores is shortlisted', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '5':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s post uses measured language.*?police file a Digital Security Act case.*?the (ruling party supporter|opposition activist)\'s more aggressive post remains online with no action taken', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    return target.strip().lower()

FOUR_ROW_CONDITIONS = [
    ('ambig', 'neg'),
    ('disambig', 'neg'),
    ('ambig', 'nonneg'),
    ('disambig', 'nonneg')
]

reordered_eng = []
reordered_ben = []

for qi in ['1', '2', '3', '4', '5']:
    e_q_recs = [r for r in eng_rows if r['question_index'] == qi]
    b_q_recs = [r for r in ben_rows if r['question_index'] == qi]
    
    ambig_e_ctxs = sorted(list(set(r['context'] for r in e_q_recs if r['context_condition'] == 'ambig')))
    assert len(ambig_e_ctxs) == 2
    
    # Orientation 1 (opposition first), Orientation 2 (ruling/pro-gov first)
    if 'opposition' in ambig_e_ctxs[0].lower():
        orientations_e = [ambig_e_ctxs[0], ambig_e_ctxs[1]]
    else:
        orientations_e = [ambig_e_ctxs[1], ambig_e_ctxs[0]]
        
    canon_eng = CANONICAL_ENG_Q3 if qi == '3' else CANONICAL_ENG_GENERAL
    canon_ben = CANONICAL_BEN_Q3 if qi == '3' else CANONICAL_BEN_GENERAL
    
    for orient_ctx_ambig in orientations_e:
        disambig_cand = [r['context'] for r in e_q_recs if r['context_condition'] == 'disambig' and r['context'].startswith(orient_ctx_ambig[:40])]
        assert len(disambig_cand) > 0
        orient_ctx_disambig = disambig_cand[0]
        
        b_ambig_match = next(r['context'] for r in b_q_recs if r['context_condition'] == 'ambig' and any(er['context'] == orient_ctx_ambig and er['id'] == r['id'] for er in e_q_recs))
        b_disambig_match = next(r['context'] for r in b_q_recs if r['context_condition'] == 'disambig' and any(er['context'] == orient_ctx_disambig and er['id'] == r['id'] for er in e_q_recs))
        
        sample_er = next(r for r in e_q_recs if r['context'] == orient_ctx_ambig)
        sample_br = next(r for r in b_q_recs if r['context'] == b_ambig_match)
        
        q_neg_e = next(r['question'] for r in e_q_recs if r['question_polarity'] == 'neg')
        q_nonneg_e = next(r['question'] for r in e_q_recs if r['question_polarity'] == 'nonneg')
        q_neg_b = next(r['question'] for r in b_q_recs if r['question_polarity'] == 'neg')
        q_nonneg_b = next(r['question'] for r in b_q_recs if r['question_polarity'] == 'nonneg')
        
        for perm_idx, (e_perm, b_perm) in enumerate(zip(canon_eng, canon_ben)):
            for cond, pol in FOUR_ROW_CONDITIONS:
                e_ctx = orient_ctx_ambig if cond == 'ambig' else orient_ctx_disambig
                b_ctx = b_ambig_match if cond == 'ambig' else b_disambig_match
                e_q = q_neg_e if pol == 'neg' else q_nonneg_e
                b_q = q_neg_b if pol == 'neg' else q_nonneg_b
                
                target_low = 'unknown' if cond == 'ambig' else solve_target_entity(qi, pol, e_ctx)
                norm_e_perm = [a.lower().strip() for a in e_perm]
                label = norm_e_perm.index(target_low)
                
                rec_e = {
                    "example_id": 0,
                    "question_index": qi,
                    "context_condition": cond,
                    "question_polarity": pol,
                    "type": sample_er['type'],
                    "context": e_ctx,
                    "question": e_q,
                    "ans0": e_perm[0],
                    "ans1": e_perm[1],
                    "ans2": e_perm[2],
                    "label": label,
                    "answer_info": make_answer_info(qi, e_perm),
                    "additional_metadata": sample_er['additional_metadata'],
                    "category": sample_er['category'],
                    "id": 0
                }
                rec_b = {
                    "example_id": 0,
                    "question_index": qi,
                    "context_condition": cond,
                    "question_polarity": pol,
                    "type": sample_br['type'],
                    "context": b_ctx,
                    "question": b_q,
                    "ans0": b_perm[0],
                    "ans1": b_perm[1],
                    "ans2": b_perm[2],
                    "label": label,
                    "answer_info": make_answer_info(qi, e_perm),
                    "additional_metadata": sample_br['additional_metadata'],
                    "category": sample_br['category'],
                    "id": 0
                }
                reordered_eng.append(rec_e)
                reordered_ben.append(rec_b)

assert len(reordered_eng) == 240
assert len(reordered_ben) == 240

# Sequential re-indexing 0 to 239
HEADERS = ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label', 'answer_info', 'additional_metadata', 'category', 'id']
eng_sheet_rows = [HEADERS]
ben_sheet_rows = [HEADERS]

for idx, (er, br) in enumerate(zip(reordered_eng, reordered_ben)):
    er['example_id'] = idx
    er['id'] = idx
    br['example_id'] = idx
    br['id'] = idx
    
    eng_sheet_rows.append([
        str(er['example_id']),
        str(er['question_index']),
        str(er['context_condition']),
        str(er['question_polarity']),
        str(er['type']),
        str(er['context']),
        str(er['question']),
        str(er['ans0']),
        str(er['ans1']),
        str(er['ans2']),
        str(er['label']),
        json.dumps(er['answer_info'], ensure_ascii=False),
        json.dumps(er['additional_metadata'], ensure_ascii=False),
        str(er['category']),
        str(er['id'])
    ])
    
    ben_sheet_rows.append([
        str(br['example_id']),
        str(br['question_index']),
        str(br['context_condition']),
        str(br['question_polarity']),
        str(br['type']),
        str(br['context']),
        str(br['question']),
        str(br['ans0']),
        str(br['ans1']),
        str(br['ans2']),
        str(br['label']),
        json.dumps(br['answer_info'], ensure_ascii=False),
        json.dumps(br['additional_metadata'], ensure_ascii=False),
        str(br['category']),
        str(br['id'])
    ])

# Push reordered values to Google Sheets
print("Uploading reordered values to Google Sheets...")
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A1:O500'
).execute()
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A1:O500'
).execute()

service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A1:O241',
    valueInputOption='USER_ENTERED',
    body={'values': eng_sheet_rows}
).execute()

service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A1:O241',
    valueInputOption='USER_ENTERED',
    body={'values': ben_sheet_rows}
).execute()

print("Reordered data values successfully pushed to Google Sheets!")

# Apply complete styling & formatting across A1:O241
print("Applying consistent formatting across entire range A1:O241...")
meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets.properties,sheets.conditionalFormats'
).execute()
sheet_map = {s['properties']['title']: (s['properties']['sheetId'], s.get('conditionalFormats', [])) for s in meta['sheets']}

requests = []

COLUMN_WIDTHS = [
    (0, 75),   # A: example_id
    (1, 85),   # B: question_index
    (2, 125),  # C: context_condition
    (3, 125),  # D: question_polarity
    (4, 75),   # E: type
    (5, 480),  # F: context
    (6, 270),  # G: question
    (7, 160),  # H: ans0
    (8, 160),  # I: ans1
    (9, 160),  # J: ans2
    (10, 65),  # K: label
    (11, 180), # L: answer_info
    (12, 180), # M: additional_metadata
    (13, 70),  # N: category
    (14, 75)   # O: id
]

for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    sheet_id, cfs = sheet_map[title]
    
    # 1. Frozen Header
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'gridProperties': {'frozenRowCount': 1}
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    })
    
    # 2. Column widths
    for col_idx, width in COLUMN_WIDTHS:
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': col_idx,
                    'endIndex': col_idx + 1
                },
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })
        
    # 3. Row heights for rows 0 to 241
    requests.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': 0,
                'endIndex': 241
            },
            'properties': {'pixelSize': 21},
            'fields': 'pixelSize'
        }
    })
    
    # 4. Header Style (Row 1, Cols A to O)
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 15
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.08627451, 'green': 0.12941177, 'blue': 0.23921569}, # #16213D
                    'horizontalAlignment': 'CENTER',
                    'verticalAlignment': 'MIDDLE',
                    'textFormat': {
                        'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                        'fontFamily': 'Arial',
                        'fontSize': 10,
                        'bold': True
                    }
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,textFormat)'
        }
    })
    
    # 5. Data Rows: Centered CLIP columns (Cols A, B, C, D, E, K, N, O)
    center_clip_cols = [0, 1, 2, 3, 4, 10, 13, 14]
    for col_idx in center_clip_cols:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 241,
                    'startColumnIndex': col_idx,
                    'endColumnIndex': col_idx + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'CLIP',
                        'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    # 6. Data Rows: Left WRAP columns (Cols F, G, H, I, J - context, question, ans0, ans1, ans2)
    left_wrap_cols = [5, 6, 7, 8, 9]
    for col_idx in left_wrap_cols:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 241,
                    'startColumnIndex': col_idx,
                    'endColumnIndex': col_idx + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    # 7. Data Rows: Left CLIP columns (Cols L, M - answer_info, additional_metadata)
    left_clip_cols = [11, 12]
    for col_idx in left_clip_cols:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 241,
                    'startColumnIndex': col_idx,
                    'endColumnIndex': col_idx + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'CLIP',
                        'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    # 8. Reset Conditional Format Rules (delete existing, add updated 1 to 241)
    for idx in range(len(cfs) - 1, -1, -1):
        requests.append({'deleteConditionalFormatRule': {'sheetId': sheet_id, 'index': idx}})
        
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'ambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.9490196, 'green': 0.9098039, 'blue': 1.0},
                        'textFormat': {'foregroundColor': {'red': 0.41960785, 'green': 0.12941177, 'blue': 0.65882355}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    })
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'disambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.9882353, 'blue': 0.9098039},
                        'textFormat': {'foregroundColor': {'red': 0.08627451, 'green': 0.4, 'blue': 0.2}, 'bold': True}
                    }
                }
            },
            'index': 1
        }
    })

service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()

print("Full formatting successfully applied across A1:O241 on both sheets!")

# Sync local JSONL files
print("Syncing local production JSONL files...")
with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "w", encoding="utf-8") as f:
    for r in reordered_eng:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "w", encoding="utf-8") as f:
    for r in reordered_ben:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Local JSONL files updated successfully!")
