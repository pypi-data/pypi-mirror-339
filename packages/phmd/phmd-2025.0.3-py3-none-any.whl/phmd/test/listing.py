from phmd import datasets

#datasets.describe('CMAPSS')

datasets.search()
datasets.search(target='rul', nature='time', features='vibra')
exit()

names = datasets.search(publisher="MFPT", return_names=True)
cites = []
for name in names:
    print(name)
    meta = datasets.read_meta(name)
    cite = meta['references']['bibitex']
    cites.append(cite.split(',')[0].split('{')[1])

print(len(cites))
print(', '.join(cites))


#print(metadata.search(domain="drive", nature='time-series', return_names=True))

#metadata.describe('CWRU')