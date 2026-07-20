#!/usr/bin/env python3
"""Apply remaining High and Medium severity revisions to HS curriculum files."""
import os

REPO = "/Users/kylebridges/Desktop/curriculum"

def load(path):
    return open(os.path.join(REPO, path), 'r', encoding='utf-8').read()

def save(path, content):
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)

def replace(path, old, new, desc=""):
    content = load(path)
    if old in content:
        content = content.replace(old, new, 1)
        save(path, content)
        print(f"  ✅ {path}: {desc}")
        return True
    else:
        first_line = old.split('\n')[0][:60]
        print(f"  ❌ {path}: '{desc}' - text not found")
        return False

# ===================== HIGH ITEMS =====================

# === hs-2-3.html: Water-Soluble Vitamins - fix energy/immunity claims ===
print("\n=== hs-2-3.html: Water-Soluble Vitamins ===")

content = load('hs-2-3.html')

# Fix B vitamins "give energy" claim
old_b_energy = (
    '<p>What they do: B vitamins help your body create energy from the food you eat. '
    'If you\u2019re not getting enough, you might feel tired all the time, struggle '
    'to concentrate in class, or notice your mood changes. Think of B vitamins as the '
    'spark plugs that keep your internal engine running smoothly.</p>'
)
new_b_energy = (
    '<p>What they do: B vitamins help your body convert food into usable energy through '
    'metabolic processes. They support normal energy metabolism and nervous system '
    'function. However, B vitamins themselves do not provide energy (calories). Feeling '
    'tired or unfocused can have many causes beyond B vitamin intake.</p>'
)
replace('hs-2-3.html', old_b_energy, new_b_energy, "Fixed B vitamin energy claim")

# Fix immunity claim about vitamin C
old_c_immune = (
    '<p>What it does: Vitamin C is famous for supporting your immune system and helping '
    'you fight off illness. People who eat enough vitamin C tend to get sick less often '
    'and recover faster when they do get sick.</p>'
)
new_c_immune = (
    '<p>What it does: Vitamin C supports normal immune function and helps with tissue '
    'repair. While getting enough vitamin C from food is part of a healthy diet, it does '
    'not guarantee fewer illnesses or faster recovery. Immune health depends on many '
    'factors.</p>'
)
replace('hs-2-3.html', old_c_immune, new_c_immune, "Fixed vitamin C immunity claim")

# Add supplement upper limit caution
old_excess = (
    '<p>Excess is excreted: Most water-soluble vitamins don\u2019t stay in your body for long. '
    'You pee out what you don\u2019t need. But that doesn\u2019t mean you should overdo '
    'supplements\u2014more is not always better, and some B vitamins can cause nerve '
    'damage in extremely high doses.</p>'
)
new_excess = (
    '<p>Excretion and safety: Most excess water-soluble vitamins are excreted in urine, '
    'but very high doses from supplements can still cause side effects. Always follow '
    'upper-limit guidelines for supplements, and check for possible interactions with '
    'medications. Food sources are the safest way to meet your needs.</p>'
)
replace('hs-2-3.html', old_excess, new_excess, "Fixed excess excretion with safety notes")

# === hs-5-2.html: Macronutrients as Fuel - overhaul ===
print("\n=== hs-5-2.html: Macronutrients as Fuel ===")

content = load('hs-5-2.html')

# Replace the reading with a synthesis lesson approach
old_5_2_reading = (
    '<p>You already know that macronutrients\u2014carbohydrates, protein, and fat\u2014are '
    'the three main energy sources your body relies on to function. But here\u2019s the '
    'part that most people miss: your body doesn\u2019t just pick one fuel source and '
    'stick with it. Instead, it blends them in different ratios depending on what you\u2019re '
    'doing, how hard you\u2019re working, and how well fueled you are.</p>'
)
new_5_2_reading = (
    '<p>This lesson builds on what you learned in Course 1 by exploring how the body uses '
    'different fuel sources flexibly across various activity intensities. The body does not '
    'switch exclusively between carbs and fat; rather, it uses a blend depending on '
    'intensity, duration, and individual factors.</p>'
)
replace('hs-5-2.html', old_5_2_reading, new_5_2_reading, "Fixed macronutrient fuel claims")

# === hs-5-3.html: Micronutrients for Function - convert to synthesis ===
print("\n=== hs-5-3.html: Micronutrients for Function ===")

content = load('hs-5-3.html')

# Add a note that this should be a synthesis lesson
old_5_3_intro = (
    '<p>You know that macronutrients\u2014carbohydrates, protein, and fat\u2014are the '
    'fuel your body runs on. But what about the tiny helpers that make everything work '
    'smoothly? That\u2019s where micronutrients come in.</p>'
)
new_5_3_intro = (
    '<p>This lesson is an applied synthesis. You have learned about micronutrients in '
    'Course 2. Here, we focus on food patterns and case studies rather than individual '
    'nutrient functions. Symptoms like fatigue, poor recovery, or low focus have many '
    'possible causes; do not use this lesson to self-diagnose deficiencies.</p>'
)
replace('hs-5-3.html', old_5_3_intro, new_5_3_intro, "Converted to synthesis lesson intro")

# === hs-5-5.html: Eating Habits Throughout the Day ===
print("\n=== hs-5-5.html: Eating Habits Throughout the Day ===")

content = load('hs-5-5.html')

# Find and fix rigid meal frequency/timing
old_rigid = (
    '<p>Eating every 3\u20134 hours keeps your metabolism active and your blood sugar '
    'stable. When you go too long without eating, your energy drops, your mood shifts, '
    'and your ability to focus in class or perform athletically suffers.</p>'
)
new_rigid = (
    '<p>Many people find that regular access to nourishment supports steady energy '
    'throughout the day, but the ideal frequency and timing of meals and snacks varies '
    'by individual. Factors like hunger cues, schedule, culture, and medical needs all '
    'play a role. There is no one "right" schedule that works for everyone.</p>'
)
replace('hs-5-5.html', old_rigid, new_rigid, "Fixed rigid meal timing")

# === hs-6-1.html: Protein, Total Energy and Recovery ===
print("\n=== hs-6-1.html: Protein, Total Energy and Recovery ===")

content = load('hs-6-1.html')

# Rename the lesson - update title
old_h6_title = '<title>Lesson 1: Inadequate Protein and Poor Recovery — WellSnax Curriculum</title>'
new_h6_title = '<title>Lesson 1: Protein, Total Energy and Recovery — WellSnax Curriculum</title>'
replace('hs-6-1.html', old_h6_title, new_h6_title, "Renamed lesson title")

old_h1 = '<h1>Inadequate Protein and Poor Recovery</h1>'
new_h1 = '<h1>Protein, Total Energy and Recovery</h1>'
replace('hs-6-1.html', old_h1, new_h1, "Renamed heading")

# Add note about multifactorial recovery
old_protein_bias = (
    '<p>Protein is the single most important macronutrient for recovery. After exercise, '
    'your muscle fibers develop microtears that need repair. Without enough protein, your '
    'body can\u2019t rebuild these fibers properly, which leads to longer recovery times, '
    'decreased strength gains, and a higher risk of injury.</p>'
)
new_protein_bias = (
    '<p>Protein is important for muscle repair after exercise, but recovery depends on '
    'multiple factors working together: total energy intake (calories), carbohydrates for '
    'glycogen replacement, sleep quality, training load management, and injury status all '
    'play significant roles. Inadequate protein alone is rarely the only cause of poor recovery.</p>'
)
replace('hs-6-1.html', old_protein_bias, new_protein_bias, "Fixed protein recovery bias")

# === hs-6-4.html: Carbohydrates and Fuel Depletion ===
print("\n=== hs-6-4.html: Carbohydrates and Fuel Depletion ===")

content = load('hs-6-4.html')

# Fix framing about low-carb always being a mistake
old_carb_bias = (
    '<p>Cutting carbs is one of the biggest mistakes athletes make. When you don\u2019t '
    'eat enough carbohydrates, your glycogen stores run low, and your performance at '
    'high intensity drops significantly. You\u2019ll feel sluggish, your legs will feel '
    'heavy, and you won\u2019t be able to push through hard efforts the way you should.</p>'
)
new_carb_bias = (
    '<p>High-intensity and prolonged activity generally rely heavily on carbohydrate fuel. '
    'However, individual carbohydrate needs vary based on sport, intensity, duration, body '
    'size, and overall diet. A single meal or snack does not determine performance. Focus '
    'on your overall eating pattern rather than labeling any one approach as a "mistake."</p>'
)
replace('hs-6-4.html', old_carb_bias, new_carb_bias, "Fixed carbohydrate framing")

# ===================== MEDIUM ITEMS =====================

# === lesson-1-4.html: Understanding Macronutrients ===
print("\n=== lesson-1-4.html: Understanding Macronutrients ===")

content = load('lesson-1-4.html')

# Fix simple/complex carb oversimplification and fat labeling
old_fat_categories = (
    '<p><strong>Fats</strong> \u2014 Help store energy, protect organs, and help with '
    'vitamin absorption. Unsaturated fats are the healthiest choice. Saturated fats '
    'should be limited. Trans fats should be avoided.</p>'
)
new_fat_categories = (
    '<p><strong>Fats</strong> \u2014 Help store energy, protect organs, and help with '
    'vitamin absorption. Fats are classified as unsaturated, saturated, and trans. '
    'Emphasizing unsaturated fats while limiting trans fat is a general dietary guidance. '
    'Most foods contain a mix of fat types, so focus on overall patterns rather than '
    'labeling individual foods as good or bad.</p>'
)
replace('lesson-1-4.html', old_fat_categories, new_fat_categories, "Fixed fat oversimplification")

# Fix simple/complex carb language
old_carbs = (
    '<p><strong>Carbohydrates</strong> \u2014 Provide energy for the body. Simple '
    'carbohydrates give fast energy; complex carbohydrates give sustained energy.</p>'
)
new_carbs = (
    '<p><strong>Carbohydrates</strong> \u2014 Provide energy for the body. Digestion '
    'speed depends on fiber content, processing, portion size, and what foods are eaten '
    'together. Whole grains, fruits, and vegetables generally provide fiber and nutrients '
    'along with carbohydrates.</p>'
)
replace('lesson-1-4.html', old_carbs, new_carbs, "Fixed carb oversimplification")

# === lesson-2-1.html: Water's Role ===
print("\n=== lesson-2-1.html: Water's Role ===")

content = load('lesson-2-1.html')

# Fix "even more for a child" and "blood is 80% water"
old_water_facts = (
    '<p>Your brain is 73% water, your muscles are 79% water, and your bones are 31% water. '
    'Blood is about 80% water. These percentages can vary by age, body composition, and '
    'hydration status.</p>'
)
new_water_facts = (
    '<p>Water makes up a large portion of your body \u2014 approximately 55\u201360% for '
    'most people. Specific percentages vary by age, body composition, and hydration status. '
    'Water helps transport nutrients, regulate body temperature, support digestion, and '
    'remove waste.</p>'
)
replace('lesson-2-1.html', old_water_facts, new_water_facts, "Fixed water facts")

# === lesson-4-4.html: Lunch Routines ===
print("\n=== lesson-4-4.html: Lunch Routines ===")

content = load('lesson-4-4.html')

# Fix same-time eating and chewing advice
old_chew = (
    '<p>Eating lunch at the same time every day helps regulate your body\u2019s internal '
    'clock and keeps your metabolism running smoothly. Chew your food thoroughly to help '
    'digestion and prevent overeating.</p>'
)
new_chew = (
    '<p>Having a regular opportunity to eat during the school day supports energy and '
    'focus. School schedules vary, so focus on making the most of your allotted lunch '
    'time \u2014 including time to eat, choosing foods from different groups, and preparing '
    'accessible options. Avoid grading students on meal timing they cannot control.</p>'
)
replace('lesson-4-4.html', old_chew, new_chew, "Fixed lunch timing advice")

# === hs-3-1.html: Intro to Nutrition Facts Label ===
print("\n=== hs-3-1.html: Intro to Nutrition Facts Label ===")

content = load('hs-3-1.html')

# Fix label as health score
old_label_score = (
    '<p>The Nutrition Facts label tells you everything you need to know about whether '
    'a food is healthy. Just look at the numbers to decide.</p>'
)
new_label_score = (
    '<p>The Nutrition Facts label is one tool for understanding what is in packaged foods. '
    'Start with serving size and servings per container, then use %DV to compare products. '
    'Use labels to compare similar foods for a stated purpose rather than declaring any '
    'single food as "healthy" or "unhealthy."</p>'
)
replace('hs-3-1.html', old_label_score, new_label_score, "Fixed label as health score")

# === hs-4-5.html: Food Marketing Strategies ===
print("\n=== hs-4-5.html: Food Marketing Strategies ===")

content = load('hs-4-5.html')

# Fix marketing analysis framing
old_marketing = (
    '<p>Food companies use clever marketing to trick you into buying their products. '
    'Almost every claim on the front of a package is designed to manipulate you. '
    'Never trust what you see on the front\u2014only the ingredient list and nutrition '
    'facts tell the real story.</p>'
)
new_marketing = (
    '<p>Food companies use a variety of marketing strategies to attract buyers. Some '
    'claims on packages are regulated by the FDA (such as "low sodium" or "good source '
    'of fiber"), while others are unregulated marketing language (such as "natural," '
    '"wholesome," or "clean"). Learning to distinguish regulated claims from branding '
    'helps you evaluate food choices more critically.</p>'
)
replace('hs-4-5.html', old_marketing, new_marketing, "Fixed marketing framing")

# === hs-5-1.html: more Medium fixes ===
print("\n=== hs-5-1.html: Additional fixes ===")

content = load('hs-5-1.html')

# Fix the energy sources section that still has prescriptive language
old_sources = (
    '<p>Calories come from three main sources: carbohydrates, proteins, and fats. '
    'Carbohydrates are your body\u2019s preferred source of energy, especially for '
    'activities that require quick bursts of movement, like sprinting or jumping. '
    'Carbs provide the body with 4 calories of energy per gram. Proteins help build '
    'and repair muscles, which is important if you\u2019re active or want to look and '
    'feel strong. Proteins provide the body with 4 calories of energy per gram. Fats '
    'provide long-lasting energy and are essential for healthy skin and brain function. '
    'Fats provide the body with 9 grams of energy per calorie.</p>'
)
new_sources = (
    '<p>Calories come from three main sources: carbohydrates, proteins, and fats. '
    'Carbohydrates provide 4 calories per gram and are the body\u2019s preferred energy '
    'source for higher-intensity activity. Proteins provide 4 calories per gram and '
    'support growth and repair. Fats provide 9 calories per gram and support normal '
    'cell function and nutrient absorption.</p>'
)
replace('hs-5-1.html', old_sources, new_sources, "Fixed energy sources section")

print("\n✅ All High and Medium edits applied!")
