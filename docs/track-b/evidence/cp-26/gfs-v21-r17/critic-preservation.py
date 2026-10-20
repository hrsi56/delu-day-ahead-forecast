import collections
import hashlib
import json
import pathlib
import re
import subprocess

CHECKOUT = pathlib.Path('/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-gfs-r17')
OUTPUT = pathlib.Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/gfs-v21-r17')
BASE = '252725e0431826b6d32f1fc8200cfa3baf3750f6'
CANDIDATE = 'f014e5b2f09dc7defa103b3c4ec5796d199c262d'
OLD_CANDIDATE = '6f57febe3659b1f902c17f3db31ba41e41136178'
EV = 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/'
records = []

def git(*args, expected=0):
    p = subprocess.run(['git', *args], cwd=CHECKOUT, text=True, capture_output=True)
    records.append({'command': 'git ' + ' '.join(args), 'exit_code': p.returncode,
                    'stdout': p.stdout, 'stderr': p.stderr})
    assert p.returncode == expected, records[-1]
    return p.stdout

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):h.update(chunk)
    return h.hexdigest()

def bar(s):
    a=s.index('### 24.7 CP-26:')
    return s[a:s.index('### 24.8 ',a)]

assert git('rev-parse','HEAD').strip()==CANDIDATE
assert git('status','--porcelain=v1')==''
assert git('symbolic-ref','-q','HEAD',expected=1)==''
main=git('rev-parse','main').strip()
assert main=='647d6eb81b2cf6e0cfaf4152f659d689ff973578'
git('merge-base','--is-ancestor',OLD_CANDIDATE,BASE)
git('merge-base','--is-ancestor',BASE,CANDIDATE)
changed=git('diff','--name-status',BASE,'HEAD')
git('diff','--check',BASE,'HEAD')
expected={'capstone_v21.md','docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md',
 'docs/track-b/cp-26-gfs-ruling-2026-10-19.md',
 'docs/track-b/evidence/cp-26/cp28-gfs-postresults-addendum-v21-r17.md',
 'docs/track-b/evidence/cp-26/gfs-v21-r17/document-validation.json',
 'docs/track-b/evidence/cp-26/gfs-v21-r17/integration-review-brief.md'}
assert {line.split('\t')[-1] for line in changed.splitlines()}==expected

def tree(ref):
    s=git('ls-tree','-r',ref)
    return {line.split('\t',1)[1]:line.split('\t',1)[0] for line in s.splitlines()}

base_tree=tree(BASE); candidate_tree=tree(CANDIDATE)
unchanged=[p for p in base_tree if p!='capstone_v21.md']
assert all(candidate_tree.get(p)==base_tree[p] for p in unchanged)
current=(CHECKOUT/'capstone_v21.md').read_text()
old=git('show',BASE+':capstone_v21.md')
current_bar=bar(current); old_bar=bar(old)
assert current_bar==old_bar
brief=(CHECKOUT/'docs/track-b/evidence/cp-26/gfs-v21-r17/integration-review-brief.md').read_text()
quoted=brief.split('## Verbatim complete checkpoint bar\n\n',1)[1]
assert quoted=='\n'.join('> '+line if line else '>' for line in current_bar.rstrip().split('\n'))+'\n'
prior=(CHECKOUT/EV/'integration-final-r16-2-PASS.md').read_text()
prior_quote=prior.split('## Verbatim complete §24.7\n\n',1)[1].split('\n## Supporting requirements',1)[0]
assert prior_quote.strip()==quoted.strip()
rows=[]
norm=lambda s:' '.join(s.split())
for line in prior.splitlines():
    if re.match(r'^\| \d+ — ',line):
        parts=line.split('|')
        assert len(parts)==6
        ident, clause, verdict, inherited=[p.strip() for p in parts[1:5]]
        assert norm(clause) in norm(current_bar), ident
        rows.append({'id':ident,'clause':clause,'inherited_assessment':inherited})
assert [int(r['id'].split(' — ')[0]) for r in rows]==list(range(1,112))

validation=json.loads((CHECKOUT/'docs/track-b/evidence/cp-26/gfs-v21-r17/document-validation.json').read_text())
document_hashes={p:sha(CHECKOUT/p) for p in validation['documents']}
assert document_hashes==validation['documents']
assert document_hashes['capstone_v21.md']=='3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc'
protocol='docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md'
assert sha(CHECKOUT/protocol)=='2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8'
assert candidate_tree[protocol]==base_tree[protocol]
custody=json.loads((CHECKOUT/EV/'final-integration-custody-v21-r16.json').read_text())
assert custody['candidate']==OLD_CANDIDATE and custody['result']=='PASS'
assert sha(CHECKOUT/custody['verdict_path'])==custody['verdict_sha256']

inventories={}
index_files=['final-analysis-artifact-index-v21-r16.json','presentation-correction-v21-r16.json']
for name in index_files:
    idx_path=CHECKOUT/EV/name; idx=json.loads(idx_path.read_text()); root=pathlib.Path(idx['artifact_root'])
    missing=[];wrong=[];count=0;total=0;prefix=collections.Counter();hashed=[]
    # Availability and exact size checks for EVERY indexed artifact; no full payload rehash.
    for entry in idx['files']:
        p=root/entry['path'];count+=1;total+=entry['bytes']
        if not p.is_file():missing.append(entry['path']);continue
        if p.stat().st_size!=entry['bytes']:wrong.append(entry['path'])
        prefix['/'.join(entry['path'].split('/')[:4])]+=1
    assert not missing and not wrong, (missing,wrong)
    # Hash decision-bearing manifests, small score tables, report/packet markdown and
    # all six preserved presentation files. Reading bytes is not regeneration.
    for entry in idx['files']:
        p=root/entry['path'];rel=entry['path']
        select=(name.startswith('presentation-') or
                pathlib.PurePosixPath(rel).name in {'scores-manifest.json','inference-manifest.json','diagnostics-manifest.json','report.md','publication-packet.md','publication-packet.json','MLflow-export.json'} or
                ('/scores/' in rel and entry['bytes']<3000000))
        if select:
            actual=sha(p);assert actual==entry['sha256'],rel
            tracked=CHECKOUT/rel
            if tracked.is_file():assert sha(tracked)==actual,rel
            hashed.append({'path':rel,'bytes':entry['bytes'],'sha256':actual})
    inventories[name]={'root':str(root),'index_raw_sha256':sha(idx_path),'content_sha256':idx['content_sha256'],
       'file_count':count,'bytes':total,'missing':missing,'wrong_sizes':wrong,'prefix_counts':dict(prefix),
       'freshly_hashed_files':hashed}

assert inventories[index_files[0]]['index_raw_sha256']=='7495b0808bccf1f972c52c175a4df46805093e2032fb68b58b6c89b2edd717e2'
assert inventories[index_files[1]]['index_raw_sha256']=='221888837817cee0a88650e261daf8d38e8b2e7feb8e70edc8ea1c87f469e774'
assert git('status','--porcelain=v1')==''
assert git('rev-parse','HEAD').strip()==CANDIDATE
assert git('rev-parse','main').strip()==main
result={'candidate':CANDIDATE,'base':BASE,'main':main,'all_prior_tracked_blobs_unchanged_except_anchor':len(unchanged),
 'complete_bar_lines':len(current_bar.splitlines()),'complete_bar_sha256':hashlib.sha256(current_bar.encode()).hexdigest(),
 'complete_bar_brief_exact':True,'clause_count':len(rows),'document_hashes':document_hashes,
 'prior_verdict_sha256':custody['verdict_sha256'],'inventories':inventories,
 'payload_wide_rehash':False,'scientific_regeneration':False,'tests_rerun':False}
(OUTPUT/'critic-preservation-result.json').write_text(json.dumps(result,indent=2)+'\n')
(OUTPUT/'critic-command-records.json').write_text(json.dumps(records,indent=2)+'\n')
(OUTPUT/'critic-clause-inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
(OUTPUT/'critic-complete-bar.md').write_text(quoted)
print(json.dumps({k:v for k,v in result.items() if k not in ['inventories','document_hashes']},indent=2))
for name,inv in inventories.items():
    print(name, 'files', inv['file_count'],'bytes', inv['bytes'],'freshly_hashed',len(inv['freshly_hashed_files']),
          'missing',len(inv['missing']),'wrong_sizes',len(inv['wrong_sizes']))
