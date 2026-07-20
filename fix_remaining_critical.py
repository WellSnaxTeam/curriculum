#!/usr/bin/env python3
"""Fix remaining failed Critical edits."""
import os

REPO = "/Users/kylebridges/Desktop/curriculum"

def load(path):
    return open(os.path.join(REPO, path), 'r', encoding='utf-8').read()

def save(path, content):
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)

# Fix hs-4-3.html
print("--- hs-4-3.html ---")
content = load('hs-4-3.html')
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
if old_meta in content:
    content = content.replace(old_meta, new_meta, 1)
    save('hs-4-3.html', content)
    print("  ✅ Fixed metabolism/personal calorie claims")
else:
    print("  ❌ metabolism section not found - checking...")
    # Check for the text
    idx = content.find('Activity Level: An athlete')
    if idx >= 0:
        print(f"  Found at pos {idx}: {repr(content[idx:idx+50])}")
    # Try with em-dash
    idx2 = content.find('Activity Level:')
    if idx2 >= 0:
        print(f"  'Activity Level:' found at {idx2}")

# Fix hs-4-6.html - add disclaimer
print("\n--- hs-4-6.html ---")
content = load('hs-4-6.html')
# Add disclaimer after reading section header
old_start = (
    '<h2><span class="badge badge-reading">Reading</span> '
    'Special Diets and Health Conditions <span class="module-time">20 min</span></h2>\n'
    '                <p>Ever notice how you crash hard after eating a huge sugary lunch'
)
new_start = (
    '<h2><span class="badge badge-reading">Reading</span> '
    'Special Diets and Health Conditions <span class="module-time">20 min</span></h2>\n'
    '                <p><strong>Important:</strong> This lesson discusses diets and '
    'health conditions for educational purposes only. Do NOT self-diagnose or start a '
    'therapeutic diet without clinician guidance. If you have health concerns, talk to '
    'a parent, school nurse, or healthcare provider.</p>\n'
    '                <p>Ever notice how you crash hard after eating a huge sugary lunch'
)
if old_start in content:
    content = content.replace(old_start, new_start, 1)
    save('hs-4-6.html', content)
    print("  ✅ Added clinical disclaimer")
else:
    print("  ❌ start text not found")

# Fix hs-5-1.html
print("\n--- hs-5-1.html ---")
content = load('hs-5-1.html')

old_energy = (
    '<p>Imagine waking up for school feeling groggy and sluggish, barely able to keep '
    'your eyes open during first period. Or maybe you remember the last time you tried '
    'to play basketball after skipping lunch, and your legs felt heavy and slow. These '
    'moments are all connected to how your body uses energy, and that energy comes from '
    'the calories in the food you eat. Understanding the relationship between energy and '
    'calories can help you make choices that improve your mood, athletic performance, focus, '
    'and even your appearance.</p>'
)
new_energy = (
    '<p>Energy from food supports everything your body does \u2014 growing, learning, '
    'moving, and maintaining organ function. Calories are a measure of that energy. '
    'This lesson uses general examples only; students should not calculate personal '
    'calorie needs or set weight-related goals as part of this course.</p>'
)
if old_energy in content:
    content = content.replace(old_energy, new_energy, 1)
    save('hs-5-1.html', content)
    print("  ✅ Fixed energy opening")
else:
    print("  ❌ energy opening not found")

# Now fix the rest of hs-5-1.html
content = load('hs-5-1.html')
old_cal = (
    '<p>Calories are units of energy. They are also referred to as kilocalories or kcals. '
    'When you eat food, your body breaks it down and converts it into energy that fuels '
    'everything you do\u2014from running laps in gym class to thinking through a tough math '
    'problem. If you don\u2019t get enough calories, you might feel tired, irritable, or '
    'unable to concentrate. On the other hand, getting too many calories without enough '
    'activity can lead to excess weight, which can affect your confidence and health. The '
    'key is finding the right balance so your body has the energy it needs to perform at '
    'its best. Your body is always burning calories even during rest and sleep to keep '
    'organs functioning.</p>'
)
new_cal = (
    '<p>Calories (kilocalories) are a way to measure the energy in food. Your body uses '
    'energy from food to support growth, organ function, physical activity, and recovery. '
    'Energy needs vary widely based on age, growth rate, body size, activity level, and '
    'genetics.</p>'
)
if old_cal in content:
    content = content.replace(old_cal, new_cal, 1)
    print("  ✅ Fixed calorie definition")

old_why = (
    '<p>The foods you choose matter as much as the number of calories you consume. For '
    'example, eating a donut and drinking soda might give you a quick burst of energy, '
    'but it won\u2019t last long. You might crash and feel sleepy or cranky soon after. '
    'In contrast, eating a balanced meal with whole grains, lean proteins, fruits, and '
    'vegetables provides steady energy throughout the day. This helps you stay alert in '
    'class, perform better in sports, and maintain a positive mood.</p>'
)
new_why = (
    '<p>The foods you choose provide not just energy but also the nutrients your body '
    'needs. A balanced eating pattern that includes a variety of foods supports your '
    'energy, focus, and overall health. Individual snack or meal choices don\u2019t '
    'determine health on their own \u2014 it\u2019s your overall pattern over time that '
    'matters most.</p>'
)
if old_why in content:
    content = content.replace(old_why, new_why, 1)
    print("  ✅ Fixed why calories matter")
    save('hs-5-1.html', content)

# Fix hs-6-3.html
print("\n--- hs-6-3.html ---")
content = load('hs-6-3.html')
old_over = (
    '<p>On the flip side, overhydration\u2014drinking too much water\u2014can also be '
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
    '        <p>On the flip side, overhydration\u2014drinking too much water\u2014can '
    'also be dangerous. Overhydration dilutes the sodium in your blood, which can lead '
    'to hyponatremia. Symptoms can include confusion, headaches, nausea, and in severe '
    'cases, seizures.'
)
if old_over in content:
    content = content.replace(old_over, new_over, 1)
    save('hs-6-3.html', content)
    print("  ✅ Added emergency warning")
else:
    print("  ❌ overhydration text not found")
    idx = content.find('overhydration')
    if idx >= 0:
        print(f"  Found at {idx}: {repr(content[idx:idx+100])}")

# Fix hs-6-5.html
print("\n--- hs-6-5.html ---")
content = load('hs-6-5.html')
old_micro = (
    '<p>Each micronutrient plays a specific role that directly connects to how you '
    'perform in sports and daily life. Iron helps carry oxygen through your blood, '
    'which affects how long you can run before feeling tired. When iron is low, you '
    'may feel unusually exhausted, get winded faster, and struggle to keep up with '
    'teammates even when you\u2019re trying your hardest. Calcium and vitamin D support '
    'strong bones and muscle contractions. Without enough of them, you might feel weaker '
    'during movements, be more prone to injury, or notice slower recovery after practice. '
    'B vitamins help your body turn food into usable energy. When they are lacking, your '
    'energy levels can drop, making you feel sluggish, mentally foggy, or unmotivated '
    'during workouts. Electrolytes like sodium and potassium help control hydration and '
    'muscle function. When they are low, you might experience cramps, dizziness, or a '
    'sudden loss of coordination during performance.</p>'
)
new_micro = (
    '<p><strong>\u26a0 Important:</strong> Symptoms discussed in this lesson \u2014 '
    'like fatigue, slower recovery, or concentration difficulty \u2014 have many possible '
    'causes including sleep, stress, training load, and overall nutrition patterns. Do NOT '
    'use this lesson to self-diagnose a micronutrient deficiency or start supplements. If '
    'you\u2019re concerned about your energy, performance, or health, speak with a trusted '
    'adult, school nurse, or healthcare provider.</p>\n'
    '        <p>Micronutrients play important roles in the body. Iron is needed for oxygen '
    'transport in the blood. Calcium and vitamin D support bone health. B vitamins help '
    'the body use energy from food. Electrolytes like sodium and potassium help with '
    'hydration and muscle function.</p>'
)
if old_micro in content:
    content = content.replace(old_micro, new_micro, 1)
    save('hs-6-5.html', content)
    print("  ✅ Added self-diagnosis disclaimer")
else:
    print("  ❌ micronutrient text not found")

# Fix performance conclusion
content = load('hs-6-5.html')
old_perf = (
    '<p>Your performance isn\u2019t just built in practice\u2014it\u2019s also built '
    'in what you consistently give your body every day. When micronutrients are balanced, '
    'your body can keep up with your effort. When they\u2019re not, your body sends '
    'signals through fatigue, focus loss, and slower performance that are easy to miss '
    'until they start affecting your game.</p>'
)
new_perf = (
    '<p>Your performance is influenced by many factors \u2014 training, sleep, stress, '
    'hydration, and overall nutrition pattern. A varied eating pattern that includes '
    'micronutrient-rich foods supports normal body functions. If you notice persistent '
    'changes in your energy or performance, talk to a healthcare provider or sports '
    'dietitian rather than assuming a deficiency.</p>'
)
if old_perf in content:
    content = content.replace(old_perf, new_perf, 1)
    save('hs-6-5.html', content)
    print("  ✅ Fixed performance conclusion")
else:
    print("  ❌ performance conclusion not found")

print("\n✅ Done!")
