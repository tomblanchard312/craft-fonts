"""Freeze Inter's public tnum substitutions for renderers without shaping features.
Run with fonttools==4.60.1. Inputs are public LumaFoundry Inter 4.001 assets;
see fonts/ui-manifest.txt. No private design-system sources are required.
"""
from pathlib import Path
from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parents[1] / 'fonts/inter-tabular'
for style in ('Regular', 'SemiBold'):
    font = TTFont(root / f'Inter-{style}.ttf', recalcTimestamp=False)
    gsub = font['GSUB'].table
    indices = {index for feature in gsub.FeatureList.FeatureRecord
               if feature.FeatureTag == 'tnum' for index in feature.Feature.LookupListIndex}
    replacements = {}
    for index in sorted(indices):
        lookup = gsub.LookupList.Lookup[index]
        for table in lookup.SubTable:
            replacements.update(getattr(table.ExtSubTable if lookup.LookupType == 7 else table, 'mapping', {}))
    assert replacements, 'Expected Inter tabular substitutions'
    for table in font['cmap'].tables:
        if table.isUnicode():
            table.cmap = {code: replacements.get(glyph, glyph) for code, glyph in table.cmap.items()}
    for name in font['name'].names:
        replacement = {1: 'Inter Tabular', 16: 'Inter Tabular',
                       4: f'Inter Tabular {style}', 6: f'InterTabular-{style}'}.get(name.nameID)
        if replacement:
            name.string = replacement.encode(name.getEncoding())
    target = root / f'InterTabular-{style}.ttf'
    font.save(target)
    result = TTFont(target)
    cmap = result.getBestCmap()
    assert len({result['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}) == 1
    print(target.name)
