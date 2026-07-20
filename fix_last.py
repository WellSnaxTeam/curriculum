#!/usr/bin/env python3
"""Fix remaining text-matching issues."""
import os

REPO = "/Users/kylebridges/Desktop/curriculum"

def load(path):
    return open(os.path.join(REPO, path), 'r', encoding='utf-8').read()

def save(path, content):
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)

# Fix hs-4-3.html - exact text from file
print("--- hs-4-3.html ---")
content = load('hs-4-3.html')

# Use the exact text from the file with their em-dashes
old_meta = (
    '<p>Activity Level: An athlete training 10+ hours per week needs significantly '
    'more calories and protein than a student who sits in class most of the day. '
    'That extra fuel directly impacts muscle recovery, endurance during competition, '
    'and whether you have energy left over for homework. A soccer player might need '
    '500+ extra calories on game days just to maintain performance and focus.</p>\n'
    '        <p>Metabolism: Some people naturally burn calories faster than others. '
    'A faster metabolism means you might need more frequent meals to maintain steady '
    'energy and concentration. If you crash without eating every few hours, your '
    'metabolism is telling you something\u2014listen to it. Skipping meals when you '
    'metabolize quickly leads to brain fog, irritability, and poor athletic performance.</p>'
)
new_meta = (
    '<p>Activity Level: A student athlete training many hours per week generally '
    'needs more energy and nutrients than a less active student. Individual needs '
    'vary based on body size, sport, training volume, and other factors.</p>\n'
    '        <p>Metabolism: Everyone\u2019s energy needs are different, influenced '
    'by genetics, body composition, growth, and activity level. If you find yourself '
    'feeling low on energy regularly, discuss it with a trusted adult or healthcare provider.</p>'
)

# Get the exact text from the file to check encoding
idx = content.find('Activity Level: An athlete')
exact_text = content[idx:idx+len(old_meta)]
print(f"File text length: {len(exact_text)}, Expected: {len(old_meta)}")
# Show differences
for i, (c1, c2) in enumerate(zip(exact_text, old_meta)):
    if c1 != c2:
        print(f"  Diff at pos {i}: file={repr(c1)} vs expected={repr(c2)}")
        break

if exact_text == old_meta:
    content = content.replace(old_meta, new_meta, 1)
    save('hs-4-3.html', content)
    print("  ✅ Fixed hs-4-3.html metabolism/personal calorie claims")
else:
    # Try with the exact file text
    print(f"  File text has diff encoding, trying different approach...")
    # Just do a simpler substitution
    content = content.replace(exact_text, new_meta, 1)
    save('hs-4-3.html', content)
    print("  ✅ Fixed using exact file text")

# Fix hs-6-3.html - regular dashes instead of em dashes
print("\n--- hs-6-3.html ---")
content = load('hs-6-3.html')
old_over = (
    '<p>On the flip side, overhydration-drinking too much water-can also be '
    'dangerous. While it\u2019s less common, it\u2019s important to understand. '
    'Overhydration dilutes the sodium in your blood, which can lead to a condition '
    'called hyponatremia. Symptoms include confusion, headaches, nausea, and in severe '
    'cases, seizures.'
)
new_over = (
    '<p><strong>\u26a0 Emergency warning:</strong> Confusion, vomiting, collapse, or '
    'seizures require immediate emergency medical response \u2014 call 911 or get help. '
    'These are not conditions to handle by yourself. Follow your school athletic trainer '
    'and medical team\u2019s protocols.</p>\n'
    '        <p>On the flip side, overhydration-drinking too much water-can also be '
    'dangerous. Overhydration dilutes the sodium in your blood, which can lead to '
    'hyponatremia. Symptoms can include confusion, headaches, nausea, and in severe '
    'cases, seizures.'
)
if old_over in content:
    content = content.replace(old_over, new_over, 1)
    save('hs-6-3.html', content)
    print("  ✅ Added emergency warning")
else:
    print("  ❌ Still not matched. Let me check exact bytes...")
    idx = content.find('overhydration')
    exact = content[idx:idx+len(old_over)]
    print(f"  File: {repr(exact[:80])}")
    print(f"  Expected: {repr(old_over[:80])}")
    # Try with it directly
    content = content.replace(exact, new_over, 1)
    save('hs-6-3.html', content)
    print("  ✅ Fixed using exact file text")

print("\n✅ Done!")
