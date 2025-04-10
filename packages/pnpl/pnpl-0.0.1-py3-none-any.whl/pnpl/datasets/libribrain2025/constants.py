PHONEMES = ['aa', 'ae', 'ah', 'ao', 'aw', 'ax-h', 'ax', 'axr', 'ay', 'b', 'bcl', 'ch', 'd', 'dcl', 'dh', 'dx', 'eh', 'el', 'em', 'en', 'eng', 'er', 'ey', 'f', 'g', 'gcl', 'hh', 'hv', 'ih',
            'ix', 'iy', 'jh', 'k', 'kcl', 'l', 'm', 'n', 'ng', 'nx', 'ow', 'oy', 'p', 'pcl', 'q', 'r', 's', 'sh', 't', 'tcl', 'th', 'uh', 'uw', 'ux', 'v', 'w', 'y', 'z', 'zh', 'sil', 'h#', 'epi', 'pau']
# CAREFUL NOT ALL PHONEMES ARE PRESENT IN LABELS
PHONATION_BY_PHONEME = {'aa': 'v', 'ae': 'v', 'ah': 'v', 'ao': 'v', 'aw': 'v', 'ax-h': 'v', 'ax': 'v', 'axr': 'v', 'ay': 'v', 'b': 'v', 'bcl': 'uv', 'ch': 'uv', 'd': 'v', 'dcl': 'uv', 'dh': 'v', 'dx': 'v', 'eh': 'v', 'el': 'v', 'em': 'v', 'en': 'v', 'eng': 'v', 'er': 'v', 'ey': 'v', 'f': 'uv', 'g': 'v', 'gcl': 'uv', 'hh': 'uv', 'hv': 'v', 'ih': 'v', 'ix': 'v',
                        'iy': 'v', 'jh': 'v', 'k': 'uv', 'kcl': 'uv', 'l': 'v', 'm': 'v', 'n': 'v', 'ng': 'v', 'nx': 'v', 'ow': 'v', 'oy': 'v', 'p': 'uv', 'pcl': 'uv', 'q': 'uv', 'r': 'v', 's': 'uv', 'sh': 'uv', 't': 'uv', 'tcl': 'uv', 'th': 'v', 'uh': 'v', 'uw': 'v', 'ux': 'v', 'v': 'v', 'w': 'v', 'y': 'v', 'z': 'v', 'zh': 'v', 'sil': 's', 'h#': 's', 'epi': 's', 'pau': 's'}

RUN_KEYS = [('0', '1', 'Sherlock1', '1'),
            ('0', '2', 'Sherlock1', '1'),
            ('0', '3', 'Sherlock1', '1'),
            ('0', '4', 'Sherlock1', '1'),
            ('0', '5', 'Sherlock1', '1'),
            ('0', '6', 'Sherlock1', '1'),
            ('0', '7', 'Sherlock1', '1'),
            ('0', '8', 'Sherlock1', '1'),
            ('0', '9', 'Sherlock1', '1'),
            ('0', '10', 'Sherlock1', '1'),
            ('0', '11', 'Sherlock1', '2'),
            ('0', '12', 'Sherlock1', '2'),
            ('0', '1', 'Sherlock2', '1'),
            # ('0', '2', 'Sherlock2', '1'),
            ('0', '3', 'Sherlock2', '1'),
            ('0', '4', 'Sherlock2', '1'),
            ('0', '5', 'Sherlock2', '1'),
            ('0', '6', 'Sherlock2', '1'),
            ('0', '7', 'Sherlock2', '1'),
            ('0', '8', 'Sherlock2', '1'),
            ('0', '9', 'Sherlock2', '1'),
            ('0', '10', 'Sherlock2', '1'),
            ('0', '11', 'Sherlock2', '1'),
            ('0', '12', 'Sherlock2', '1'),
            ('0', '1', 'Sherlock3', '1'),
            ('0', '2', 'Sherlock3', '1'),
            ('0', '3', 'Sherlock3', '1'),
            ('0', '4', 'Sherlock3', '1'),
            ('0', '5', 'Sherlock3', '1'),
            ('0', '6', 'Sherlock3', '1'),
            ('0', '7', 'Sherlock3', '1'),
            ('0', '8', 'Sherlock3', '1'),
            ('0', '9', 'Sherlock3', '1'),
            ('0', '10', 'Sherlock3', '1'),
            ('0', '11', 'Sherlock3', '1'),
            ('0', '12', 'Sherlock3', '1')
            ]

VALIDATION_RUN_KEYS = [
    ('0', '11', 'Sherlock1', '2'),
    ('0', '12', 'Sherlock1', '2')
]
