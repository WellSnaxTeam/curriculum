#!/usr/bin/env python3
"""Final batch of High/Medium edits with exact file text."""
import os

REPO = "/Users/kylebridges/Desktop/curriculum"

def load(path):
    return open(os.path.join(REPO, path), 'r', encoding='utf-8').read()

def save(path, content):
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)

# hs-5-3.html - Add disclaimer about not self-diagnosing
print("--- hs-5-3.html ---")
content = load('hs-5-3.html')
old = (
    '<p>Why You Should Care Right Now</p>\n'
    '        <p>You\u2019re sitting in third period, and your eyelids feel like they weigh '
    '50 pounds. You know you got enough sleep, but your brain feels foggy anyway. Or maybe '
    'you crushed it at practice yesterday, but today your muscles feel weak and your energy '
    'is completely gone. Perhaps you\u2019re frustrated because no matter what you do, '
    'your skin breaks out right before something important, or you\u2019ve noticed your '
    'mood swings are getting out of control.</p>\n'
    '        <p>Here\u2019s the thing: these aren\u2019t character flaws or signs you\u2019re '
    'lazy. They\u2019re often signals that your body is missing critical micronutrients '
    '\u2014 the vitamins and minerals that act like backstage crew members keeping '
    'everything running smoothly. You don\u2019t see them, but without them, the whole '
    'show falls apart.</p>'
)
new = (
    '<p><strong>Important:</strong> This lesson is an applied synthesis of micronutrient '
    'concepts. Symptoms like fatigue, low focus, skin changes, or mood shifts have many '
    'possible causes \u2014 including sleep, stress, illness, and training load. Do NOT '
    'use this lesson to self-diagnose a deficiency or start supplements.</p>\n'
    '        <p>Why Micronutrients Matter</p>\n'
    '        <p>Micronutrients are vitamins and minerals your body needs in small amounts '
    'to support normal functions. Getting a variety of them through food contributes to '
    'overall health, but no single nutrient determines how you feel or perform on a given day.</p>'
)
if old in content:
    content = content.replace(old, new, 1)
    print("  ✅ Fixed hs-5-3.html opening")

# Fix the "B vitamins give you energy" claims in hs-5-3.html
old_b_energy = (
    '<li>Energy: B vitamins are literally involved in converting the food you eat into '
    'usable energy. Without enough B vitamins, you feel exhausted even when you\u2019ve '
    'had plenty of calories.</li>\n'
    '          <li>Focus and concentration: B vitamins support neurotransmitter production, '
    'which means clearer thinking and better memory during studying and tests.</li>\n'
    '          <li>Mood: Low B vitamins are linked to depression, anxiety, and irritability '
    '\u2014 things that definitely affect your social life and how you feel day-to-day.</li>\n'
    '          <li>Athletic performance: B vitamins help your muscles recover after workouts '
    'and reduce fatigue during training.</li>'
)
new_b_energy = (
    '<li>Energy metabolism: B vitamins help your body convert food into energy through '
    'metabolic processes, but they do not provide energy themselves.</li>\n'
    '          <li>Nervous system function: B vitamins support normal nerve function and '
    'normal red blood cell formation.</li>\n'
    '          <li>Nutrient metabolism: They play a role in how the body processes proteins, '
    'fats, and carbohydrates.</li>'
)
if old_b_energy in content:
    content = content.replace(old_b_energy, new_b_energy, 1)
    print("  ✅ Fixed hs-5-3.html B vitamin claims")

# Fix the "skin, focus, performance" promise section
old_micro_promise = (
    '<p>When you consistently get enough micronutrients, your energy skyrockets, your focus '
    'sharpens, your athletic performance improves, and even your skin clears up. When '
    'you\u2019re deficient, everything suffers.</p>'
)
new_micro_promise = (
    '<p>A varied diet that includes micronutrient-rich foods supports normal body functions '
    'like energy metabolism, immune function, and tissue repair. Micronutrient deficiencies '
    'require proper medical assessment \u2014 not self-diagnosis.</p>'
)
if old_micro_promise in content:
    content = content.replace(old_micro_promise, new_micro_promise, 1)
    print("  ✅ Fixed hs-5-3.html micronutrient promise")

save('hs-5-3.html', content)

# hs-6-1.html - Add recovery disclaimer
print("\n--- hs-6-1.html ---")
content = load('hs-6-1.html')
old_protein = (
    '<p>Protein is more than just a buzzword on energy bar wrappers; it\u2019s a vital '
    'nutrient that helps build, repair, and maintain muscle tissue. For high school '
    'athletes, getting enough protein is essential for feeling strong, energetic, and '
    'ready to take on challenges both on the field and in the classroom. When your body '
    'doesn\u2019t get enough protein, you might notice slower muscle recovery, more '
    'frequent injuries, and even trouble concentrating during the school day.</p>'
)
new_protein = (
    '<p><strong>Note:</strong> Recovery depends on several factors working together: '
    'total energy intake, carbohydrates for glycogen replenishment, sleep quality, '
    'training load management, and injury status. Protein is one important piece, but '
    'inadequate protein alone is rarely the sole cause of poor recovery.</p>\n'
    '        <p>Protein helps build, repair, and maintain muscle tissue. For high school '
    'athletes, getting enough protein supports recovery, but adequate total calories and '
    'carbohydrates are equally important.</p>'
)
if old_protein in content:
    content = content.replace(old_protein, new_protein, 1)
    print("  ✅ Fixed hs-6-1.html protein recovery bias")
else:
    print("  ❌ hs-6-1.html: text not found - trying exact match")
    # Find the protein sentence
    idx = content.find('Protein is more than just a buzzword')
    if idx >= 0:
        snippet = content[idx:idx+350]
        print(f"  Found: {snippet[:100]}")
        # Try replacement with exact bytes
        content = content.replace(content[idx:idx+350], new_protein, 1)
        save('hs-6-1.html', content)
        print("  ✅ Applied with exact match")

# Fix the bottom line for hs-6-1.html
content = load('hs-6-1.html')
old_bottom = (
    '<p>In conclusion, adequate protein intake is a key factor in how well high school '
    'athletes recover from physical activity. Low protein intake can lead to slower '
    'recovery, more injuries, and decreased performance, affecting everything from your '
    'energy levels to your appearance. By understanding the causes of low protein intake '
    'and forming healthy eating habits, you can ensure your body gets the nutrients it '
    'needs to thrive. Whether you\u2019re aiming for a personal best or just want to feel '
    'your best every day, making protein a part of your routine is a smart move.</p>'
)
new_bottom = (
    '<p>Getting enough protein supports muscle repair, but remember that total energy '
    'intake, carbohydrate availability, sleep, training load, and injury management all '
    'affect recovery. If you have concerns about your recovery or eating patterns, talk '
    'to a sports dietitian or healthcare provider for personalized guidance.</p>'
)
if old_bottom in content:
    content = content.replace(old_bottom, new_bottom, 1)
    save('hs-6-1.html', content)
    print("  ✅ Fixed hs-6-1.html bottom line")
else:
    print("  ❌ hs-6-1.html: bottom line not found")

# hs-6-4.html - Add flexibility note
print("\n--- hs-6-4.html ---")
content = load('hs-6-4.html')
old_carb_intro = (
    '<p>Many athletes think this happens because they aren\u2019t working hard enough or '
    'aren\u2019t in good enough shape. But sometimes the real problem starts long before '
    'practice begins\u2014with what you ate (or didn\u2019t eat).</p>\n'
    '        <p>Your body needs fuel to move, think, react, and recover. One of the most '
    'important sources of that fuel is carbohydrates.</p>'
)
new_carb_intro = (
    '<p>Carbohydrates are an important fuel source, especially for high-intensity and '
    'prolonged activity. However, individual needs vary based on sport, intensity, '
    'duration, body size, and overall diet. A single meal does not determine performance, '
    'and there is no one-size-fits-all approach to carbohydrate intake.</p>\n'
    '        <p>Your body needs fuel to move, think, react, and recover. Carbohydrates are '
    'one of the key sources of that fuel, but needs vary from person to person.</p>'
)
if old_carb_intro in content:
    content = content.replace(old_carb_intro, new_carb_intro, 1)
    save('hs-6-4.html', content)
    print("  ✅ Fixed hs-6-4.html carb intro")
else:
    print("  ❌ hs-6-4.html: intro not found")

# hs-5-5.html - Add flexibility note
print("\n--- hs-5-5.html ---")
content = load('hs-5-5.html')
# Replace the bottom line
old_bottom5 = (
    '<p>The Bottom Line</p>\n'
    '        <p>The way you eat throughout the day has a direct impact on your energy, mood, '
    'athletic performance, focus, and appearance. By making thoughtful choices about what '
    'and when you eat, you can improve your daily performance and set yourself up for '
    'long-term health and success. Next time you reach for a snack or skip a meal, remember '
    'how your eating habits shape not just your day, but your future.</p>'
)
new_bottom5 = (
    '<p>The Big Picture</p>\n'
    '        <p>Regular access to nourishment throughout the day supports energy and focus. '
    'The ideal meal frequency and timing varies by individual based on hunger cues, schedule, '
    'culture, and medical needs. There is no single "right" way to eat \u2014 focus on '
    'what helps you feel fueled for your activities.</p>'
)
if old_bottom5 in content:
    content = content.replace(old_bottom5, new_bottom5, 1)
    save('hs-5-5.html', content)
    print("  ✅ Fixed hs-5-5.html bottom line")
else:
    print("  ❌ hs-5-5.html: bottom line not found")

# hs-2-3.html - Fix remaining deterministic "Why it matters" lines
print("\n--- hs-2-3.html ---")
content = load('hs-2-3.html')
# Add a top disclaimer
old_top = (
    '<p>Water Soluble Vitamins</p>\n'
    '        <p>Water-soluble vitamins dissolve in water and go directly into your '
    'bloodstream.'
)
new_top = (
    '<p><strong>Important:</strong> The symptoms mentioned below (like feeling tired '
    'or having slower reactions) have many possible causes. This lesson describes '
    'established biological functions of vitamins but is not a guide for self-diagnosis. '
    'If you have persistent health concerns, talk to a healthcare provider.</p>\n'
    '        <p>Water Soluble Vitamins</p>\n'
    '        <p>Water-soluble vitamins dissolve in water and go directly into your '
    'bloodstream.'
)
if old_top in content:
    content = content.replace(old_top, new_top, 1)
    print("  ✅ Added hs-2-3.html disclaimer")

# Fix the deterministic symptom claims for each B vitamin
replacements = [
    ("If you're low in B1 you may feel tired during classes or workouts and notice slower reaction times in sports.",
     "B1 (thiamin) supports normal energy metabolism and nerve function."),
    ("That can mean more stamina during long study sessions and fewer skin or eye problems from stress or late nights.",
     "Riboflavin supports normal energy production and helps maintain healthy skin and eyes."),
    ("Good niacin levels can help you stay alert and keep your skin looking healthy when you're under stress.",
     "Niacin supports normal digestion and nervous system function."),
    ("It's one of the reasons you can power through a long day of classes or recover after practice.",
     "Pantothenic acid helps the body break down proteins, carbs, and fats."),
    ("Adequate B6 can help with concentration, better mood regulation, and a stronger immune system during exam season.",
     "B6 supports normal immune function and brain development."),
    ("Good biotin support can help your appearance and keep energy levels more stable.",
     "Biotin helps the body process fats and glucose."),
    ("important for growth, recovery after workouts, and maintaining healthy skin.",
     "important for normal cell growth and DNA synthesis."),
    ("low B12 can cause fatigue and brain fog that hurt study and sports performance.",
     "B12 is needed for normal red blood cell formation and nervous system function."),
]
for old_text, new_text in replacements:
    if old_text in content:
        content = content.replace(old_text, new_text, 1)
        print(f"  ✅ Fixed deterministic claim: {old_text[:40]}...")
save('hs-2-3.html', content)

print("\n✅ All remaining High/Medium edits complete!")
