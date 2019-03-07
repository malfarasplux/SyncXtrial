# midfile MIDI to JSON Conversion (using MIDO)
# Example taken from https://easymusicnotes.com/index.php?option=com_content&view=article&id=199:midi-files-piano-level-6&catid=82:piano&Itemid=155
import json
import mido


def midifile_to_dict(mid):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])

    return {
        'ticks_per_beat': mid.ticks_per_beat,
        'tracks': tracks,
    }

fname = './mid/lullaby-brahms-classical-piano-level-6'
mid = mido.MidiFile(fname + '.mid')
print(json.dumps(midifile_to_dict(mid), indent=2))
JSONstring = json.dumps(midifile_to_dict(mid), indent=2)
JSONdict = json.loads(JSONstring)  

with open(fname + '.json', 'w') as outfile:
    json.dump(JSONdict, outfile, sort_keys=True, indent=4)
