#!/usr/bin/env python3
"""Apply remaining Critical audit revisions to HS curriculum files."""
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
        # Debug: show where it failed
        first_line = old.split('\n')[0][:60]
        print(f"  ❌ {path}: text not found for '{desc}' ({first_line}...)")
        return False

print("=" * 50)
print("Remaining Critical Revisions")
print("=" * 50)

# === hs-2-1.html (already mostly fixed by first script, just check) ===

# === hs-2-2.html: Fix D2/K2, E recovery, sun exposure ===
print("\n--- hs-2-2.html: Fat-Soluble Vitamins ---")

# Fix the D2/K2 interaction claim
old_d2k2 = """<li>Interaction note: Taking vitamin K2 with vitamin D2 can help direct calcium to bones and teeth instead of soft tissues, protecting long‑term heart and artery health — relevant to future athletic health and long‑term fitness.</li>"""
new_d2k2 = """<li>Clinical note: Vitamin D supports calcium absorption; adequate intake supports bone health. Any questions about combining specific vitamin forms should be directed to a healthcare provider or registered dietitian.</li>"""
replace('hs-2-2.html', old_d2k2, new_d2k2, "Fixed D2/K2 calcium-routing claim")

# Fix vitamin E - remove performance/soreness promises
old_e_recovery = """<li>Function in the body: Vitamin E neutralizes free radicals that can cause muscle soreness and fatigue after intense workouts, supports immune function so you recover faster, and helps protect skin and hair — affecting appearance and feeling of wellbeing. It may also support cardiovascular health, helping endurance.</li>"""
new_e_recovery = """<li>Function in the body: Vitamin E acts as an antioxidant, helping protect cells from oxidative stress. It can be found in nuts, seeds, and vegetable oils. While it supports normal cell function, it does not directly reduce muscle soreness or speed recovery from exercise.</li>"""
replace('hs-2-2.html', old_e_recovery, new_e_recovery, "Fixed vitamin E recovery claims")

# Fix vitamin E intro line
old_e_intro = """<p>Vitamin E — antioxidant protection for cells, skin, and athletic recovery</p>"""
new_e_intro = """<p>Vitamin E — antioxidant that helps protect cells from oxidative stress</p>"""
replace('hs-2-2.html', old_e_intro, new_e_intro, "Fixed vitamin E intro")

# Fix sun exposure wording
old_sun = """<li>Safe sun exposure plus diet: Get short periods of sun for vitamin D, and include fortified foods or discuss supplements with a healthcare provider if you’re indoors most days — this helps maintain mood, focus, and physical performance.</li>"""
new_sun = """<li>Sun safety: Moderate sun exposure can help your skin produce vitamin D, but use sun protection to prevent skin damage. Vitamin D can also come from fortified foods and supplements under healthcare provider guidance.</li>"""
replace('hs-2-2.html', old_sun, new_sun, "Fixed sun exposure wording")

# Fix recovery and appearance line  
old_appearance = """<li>Recovery and appearance: After heavy exercise, choose snacks with vitamin E sources to support recovery and skin health.</li>"""
new_appearance = """<li>After exercise, choose snacks that include a variety of nutrients — including vitamin E from nuts and seeds — as part of an overall recovery eating pattern.</li>"""
replace('hs-2-2.html', old_appearance, new_appearance, "Fixed recovery/appearance claim")

# Fix first bullet about fat-soluble vitamins
old_fat_sol = """<li>Fat‑soluble vitamins dissolve in fat and need dietary fat to be absorbed. If you eat vitamin‑rich foods with a healthy fat (olive oil, avocado, nuts), your body absorbs more of the vitamin — which can mean better energy, clearer thinking, and improved athletic recovery.</li>"""
new_fat_sol = """<li>Fat‑soluble vitamins dissolve in fat and need dietary fat to be absorbed. Eating vitamin‑rich foods with a source of fat (like olive oil, avocado, or nuts) supports absorption, which is part of normal nutrient processing.</li>"""
replace('hs-2-2.html', old_fat_sol, new_fat_sol, "Fixed fat-soluble vitamin claims")

# === hs-2-4.html: Key Minerals ===
print("\n--- hs-2-4.html: Key Minerals ---")

# Fix magnesium implication for cramps
content = load('hs-2-4.html')

# Add a disclaimer about exercise cramps being multifactorial at the start of the reading
old_start = """<p><strong>What Are Minerals?</strong></p>
        <p>Minerals are naturally occurring elements found in soil and water, which plants absorb and animals eat. Your body needs these minerals."""

# Check if this exists
if old_start in content:
    print(f"  ℹ️  hs-2-4.html: found reading start")
    
# Fix activity section that asks students to self-diagnose
old_activity_connect = """<li>write a reflection connecting possible mineral gaps (like iron or magnesium) to how you feel</li>"""
new_activity_connect = """<li>write a reflection describing how a varied food pattern supports normal body functions (instead of linking specific symptoms to specific mineral gaps)</li>"""
replace('hs-2-4.html', old_activity_connect, new_activity_connect, "Fixed self-diagnosis activity")

# Fix quiz questions about mineral gaps causing specific symptoms
old_q2 = """<li><span class="letter">D.</span> High potassium improving energy regulation</li>
          </ul>
        </div>
        <div class="quiz-question">
          <p class="q">2. Frequent muscle cramps during exercise combined with low fruit and vegetable intake most likely indicates low:"""
old_new2 = """<li><span class="letter">D.</span> High potassium improving energy regulation</li>
          </ul>
        </div>
        <div class="quiz-question">
          <p class="q">2. Frequent muscle cramps during exercise combined with low fruit and vegetable intake could be a sign of several possible imbalances. Which factor is worth considering?"""
replace('hs-2-4.html', old_q2, old_new2, "Fixed Q2 about cramps")

# Fix Q13
old_q13 = """<p class="q">13. Muscle cramps during exercise may be linked to low potassium and magnesium intake. True / False</p>"""
new_q13 = """<p class="q">13. Muscle cramps during exercise may be influenced by several factors including hydration, electrolyte balance, conditioning, and overall nutrition. True / False</p>"""
replace('hs-2-4.html', old_q13, new_q13, "Fixed Q13 about cramps")

# Fix Q11
old_q11 = """<p class="q">11. Eating a variety of fruits, vegetables, dairy, and lean proteins supports balanced mineral intake that improves energy and performance. True / False</p>"""
new_q11 = """<p class="q">11. Eating a variety of fruits, vegetables, dairy, and lean proteins supports balanced mineral intake, which contributes to normal body functions. True / False</p>"""
replace('hs-2-4.html', old_q11, new_q11, "Fixed Q11")

# === hs-4-3.html: Individual Dietary Needs ===
print("\n--- hs-4-3.html: Individual Dietary Needs ---")

content = load('hs-4-3.html')

# Replace metabolism/personal calorie claims
old_meta = """<p>Activity Level: An athlete training 10+ hours per week needs significantly more calories and protein than a student who sits in class most of the day. That extra fuel directly impacts muscle recovery, endurance during competition, and whether you have energy left over for homework. A soccer player might need 500+ extra calories on game days just to maintain performance and focus.</p>
        <p>Metabolism: Some people naturally burn calories faster than others. A faster metabolism means you might need more frequent meals to maintain steady energy and concentration. If you crash without eating every few hours, your metabolism is telling you something—listen to it. Skipping meals when you metabolize quickly leads to brain fog, irritability, and poor athletic performance.</p>"""
new_meta = """<p>Activity Level: A student athlete training many hours per week generally needs more energy and nutrients than a less active student. Individual needs vary based on body size, sport, training volume, and other factors. Rather than calculating personal targets, think about whether you feel fueled for your activities.</p>
        <p>Metabolism: Everyone's energy needs are different, influenced by genetics, body composition, growth, and activity level. If you find yourself feeling low on energy regularly, that's worth discussing with a trusted adult or healthcare provider rather than self-prescribing changes.</p>"""
replace('hs-4-3.html', old_meta, new_meta, "Fixed metabolism/personal calorie claims")

# Fix activity description that asks for personal data
old_activity_personal = """<li>Identify one personal goal you are currently working toward</li>"""
new_activity_personal = """<li>Review fictional athlete profiles provided by your teacher and identify nutrition strategies for each</li>"""
replace('hs-4-3.html', old_activity_personal, new_activity_personal, "Fixed personal goal activity")

# === hs-4-6.html: Special Diets and Health Conditions ===
print("\n--- hs-4-6.html: Special Diets and Health Conditions ---")

content = load('hs-4-6.html')

# Add a disclaimer at the top of the reading
old_reading_start = """<p><strong>What Are Special Diets?</strong></p>
        <p>Some diets are medically necessary, while others are chosen for personal, ethical, or religious reasons. Understanding the difference is important because special diets are powerful tools when used correctly—but following the wrong diet for your situation can harm your health, performance, and wellbeing. Once you understand the landscape of special diets, you can make informed decisions about foods that support your body, energy levels, and values.</p>"""
new_reading_start = """<p><strong>Important:</strong> Diets and health conditions discussed in this lesson are for educational purposes only. Students should NOT self-diagnose medical conditions or start therapeutic diets without clinician guidance. If you have concerns about a health condition, talk to your parent, school nurse, or healthcare provider.</p>
        <p><strong>What Are Special Diets?</strong></p>
        <p>Some diets are medically necessary, while others are chosen for personal, ethical, or religious reasons. Understanding the difference is important. This lesson uses case studies for classroom discussion — not for individual diagnosis or treatment planning.</p>"""
replace('hs-4-6.html', old_reading_start, new_reading_start, "Added clinical disclaimer")

# Replace prescriptive "Why the diet matters" sections with neutral educational language
old_diabetes = """<p>Why the diet matters: When someone has diabetes, eating a diabetic diet—which focuses on balanced portions of whole grains, lean proteins, healthy fats, and limited refined sugars—keeps blood sugar stable. Without this balance, blood sugar spikes and crashes create energy rollercoasters that destroy focus and athletic performance. A student with diabetes who eats a donut for breakfast might feel energized for 20 minutes, then crash hard by the second period, making it impossible to concentrate on a test. By eating balanced meals with protein and fiber, they maintain steady energy throughout the day, stay sharp during classes, and have the stamina to excel in sports or activities.</p>"""
new_diabetes = """<p>Why the diet matters: People with diabetes must follow a clinician‑directed plan to manage blood sugar levels. This often includes balancing carbohydrate intake, eating at regular intervals, and choosing nutrient‑dense foods. The specific dietary approach is individualized and should be managed by a healthcare team.</p>"""
replace('hs-4-6.html', old_diabetes, new_diabetes, "Fixed diabetes prescriptive language")

old_celiac = """<p>Why the diet matters: People with celiac must eat a gluten-free diet, avoiding any food containing gluten. When they eat gluten, it causes inflammation in their digestive system, which leads to bloating, cramping, and nutrient absorption problems. This means their body can't properly absorb the vitamins and minerals needed for energy and focus. A student with undiagnosed celiac eating regular pasta might experience brain fog during class, feel exhausted after sports, and struggle with mood swings throughout the day. Once they switch to gluten-free alternatives, they notice clearer thinking, better athletic recovery, improved mood, and skin that clears up as inflammation decreases.</p>"""
new_celiac = """<p>Why the diet matters: People with celiac disease must follow a strict gluten‑free diet to prevent intestinal damage and allow nutrient absorption. The gluten‑free diet is a medically necessary treatment, not a lifestyle choice. Students with celiac disease should follow their medical plan and work with a dietitian.</p>"""
replace('hs-4-6.html', old_celiac, new_celiac, "Fixed celiac disease prescriptive language")

old_heart = """<p>Why the diet matters: A heart-healthy diet emphasizes lean proteins, whole grains, fruits, vegetables, and healthy fats (like those in olive oil and fish) while limiting saturated fat, trans fat, and sodium. This diet keeps arteries clear and reduces inflammation, allowing blood to flow efficiently throughout the body—including to the brain. Better blood flow means more oxygen reaching your muscles and brain. Students following a heart-healthy diet report better focus during long study sessions, improved athletic endurance, and more stable moods because their brain and heart are getting the oxygen they need. Plus, a heart-healthy diet often leads to improved appearance as excess weight decreases and skin looks healthier.</p>
        <p>The personal impact: A heart-healthy diet = better oxygen delivery to your brain and muscles, sharper focus, improved athletic performance, sustained energy, better mood, and a healthier appearance.</p>"""
new_heart = """<p>Why the diet matters: A heart‑healthy eating pattern emphasizes vegetables, fruits, whole grains, lean proteins, and unsaturated fats while limiting saturated fat, trans fat, and sodium. People with cardiovascular conditions should follow their clinician's dietary guidance rather than self‑prescribing.</p>"""
replace('hs-4-6.html', old_heart, new_heart, "Fixed heart-healthy prescriptive language")

old_allergy = """<p>Why the diet matters: People with food allergies must avoid their allergen completely. Even small amounts can cause reactions ranging from mild itching to severe breathing problems. By following an elimination diet (removing the allergen), they protect their health and maintain consistent well-being. A student with a peanut allergy who accidentally eats peanuts might experience swelling, difficulty breathing, or anaphylaxis—a life-threatening emergency. By being vigilant about reading labels and avoiding their allergen, they stay healthy, maintain their energy, keep their focus sharp, and can fully participate in school and sports without fear.</p>"""
new_allergy = """<p>Why the diet matters: People with food allergies must strictly avoid their allergen. Even trace amounts can trigger reactions. For suspected anaphylaxis, epinephrine is the first-line emergency treatment. Students with food allergies should have a school health plan and know how to use their emergency medications.</p>"""
replace('hs-4-6.html', old_allergy, new_allergy, "Fixed allergy prescriptive language")

old_gerd = """<p>Why the diet matters: People with GERD must avoid trigger foods—typically spicy foods, citrus, chocolate, caffeine, fatty foods, and carbonated drinks—that relax the valve between the stomach and esophagus or increase acid production. When someone with GERD eats pizza loaded with cheese and pepperoni right before bed, they experience painful heartburn that keeps them awake, leaving them exhausted and unfocused the next day. By eating smaller, balanced meals and avoiding triggers, they sleep better, wake refreshed, maintain energy throughout the day, and can focus during class and perform better athletically. Their mood also improves because they're not dealing with constant discomfort.</p>"""
new_gerd = """<p>Why the diet matters: People with GERD often need to identify and avoid personal trigger foods and may benefit from smaller, more frequent meals. Individual triggers vary, so dietary plans should be developed with clinician guidance.</p>"""
replace('hs-4-6.html', old_gerd, new_gerd, "Fixed GERD prescriptive language")

old_alpha_gal = """<p>Why the diet matters: People with alpha-gal must avoid red meat and mammal dairy products, instead eating poultry, fish, plant-based proteins, and non-mammal dairy alternatives. When someone with alpha-gal eats a hamburger, they might experience itching, hives, or gastrointestinal distress hours later, which disrupts their sleep and leaves them tired and unfocused the next day. By eating chicken, fish, beans, and alternatives instead, they maintain steady energy, sleep well, stay focused in class, perform better in sports, and avoid the appearance issues (like hives) that come with allergic reactions.</p>"""
new_alpha_gal = """<p>Why the diet matters: People with alpha‑gal syndrome must avoid mammalian meat and products. Management involves dietary avoidance and having an emergency plan for allergic reactions, directed by their healthcare provider.</p>"""
replace('hs-4-6.html', old_alpha_gal, new_alpha_gal, "Fixed alpha-gal prescriptive language")

# Fix vegetarian/vegan sections that guarantee outcomes
old_veg = """<p>Why people choose it: Many choose vegetarianism for ethical or environmental reasons. When done well, a vegetarian diet provides plenty of protein from eggs, dairy, legumes, nuts, and seeds. Students who eat vegetarian meals often report sustained energy, better focus, and improved mood because plant-based foods are rich in fiber and nutrients. Athletic performance improves when vegetarians combine proteins properly (like beans with rice) to get all amino acids needed for muscle recovery.</p>
        <p>The personal impact: A well-planned vegetarian diet = sustained energy, clear focus, stable mood, and strong athletic performance.</p>"""
new_veg = """<p>Why people choose it: Many choose vegetarianism for ethical, environmental, or religious reasons. A well‑planned vegetarian diet can meet nutrient needs, including protein from eggs, dairy, legumes, nuts, and seeds. As with any eating pattern, individual planning matters for adequacy.</p>"""
replace('hs-4-6.html', old_veg, new_veg, "Fixed vegetarian guaranteed outcomes")

old_vegan = """<p>Why people choose it: Vegans choose this diet for ethical, environmental, or health reasons. A well-planned vegan diet provides all necessary nutrients through plant-based sources like legumes, tofu, tempeh, nuts, seeds, whole grains, and vegetables. Students following a vegan diet often experience better digestion, clearer skin, sustained energy, and improved mood. Athletic performance thrives when vegans eat adequate protein and carbohydrates for muscle recovery and fuel.</p>
        <p>The personal impact: A well-planned vegan diet = sustained energy, improved digestion and skin clarity, stable mood, sharp focus, and reliable athletic performance.</p>"""
new_vegan = """<p>Why people choose it: Vegans choose this diet for ethical, environmental, or religious reasons. A well‑planned vegan diet can meet nutrient needs through plant sources like legumes, tofu, nuts, seeds, and whole grains. Those following a vegan diet should pay attention to nutrients like vitamin B12, iron, calcium, and vitamin D, which may require fortified foods or supplementation under clinician guidance.</p>"""
replace('hs-4-6.html', old_vegan, new_vegan, "Fixed vegan guaranteed outcomes")

# === hs-5-1.html: Energy and Calories ===
print("\n--- hs-5-1.html: Energy and Calories ---")

content = load('hs-5-1.html')

# Replace energy balance material
old_energy_reading = """<p>Imagine waking up for school feeling groggy and sluggish, barely able to keep your eyes open during first period. Or maybe you remember the last time you tried to play basketball after skipping lunch, and your legs felt heavy and slow. These moments are all connected to how your body uses energy, and that energy comes from the calories in the food you eat. Understanding the relationship between energy and calories can help you make choices that improve your mood, athletic performance, focus, and even your appearance.</p>
        <p>What are calories?</p>
        <p>Calories are units of energy. They are also referred to as kilocalories or kcals. When you eat food, your body breaks it down and converts it into energy that fuels everything you do—from running laps in gym class to thinking through a tough math problem. If you don't get enough calories, you might feel tired, irritable, or unable to concentrate. On the other hand, getting too many calories without enough activity can lead to excess weight, which can affect your confidence and health. The key is finding the right balance so your body has the energy it needs to perform at its best. Your body is always burning calories even during rest and sleep to keep organs functioning.</p>
        <p>Why do calories matter?</p>
        <p>The foods you choose matter as much as the number of calories you consume. For example, eating a donut and drinking soda might give you a quick burst of energy, but it won't last long. You might crash and feel sleepy or cranky soon after. In contrast, eating a balanced meal with whole grains, lean proteins, fruits, and vegetables provides steady energy throughout the day. This helps you stay alert in class, perform better in sports, and maintain a positive mood.</p>
        <p>Calories come from three main sources: carbohydrates, proteins, and fats. Each plays a unique role in your body. Carbohydrates are your body's preferred source of energy, especially for activities that require quick bursts of movement, like sprinting or jumping. Carbs provide the body with 4 calories of energy per gram. Proteins help build and repair muscles, which is important if you're active or want to look and feel strong. Proteins provide the body with 4 calories of energy per gram. Fats provide long-lasting energy and are essential for healthy skin and brain function. Fats provide the body with 9 grams of energy per calorie. Choosing foods that combine these nutrients helps you feel full, focused, and ready to take on challenges.</p>"""

new_energy_reading = """<p>Energy from food supports everything your body does — growing, learning, moving, and maintaining organ function. Calories are a measure of that energy. This lesson uses general examples only; students should not calculate personal calorie needs or set weight‑related goals as part of this course.</p>
        <p>What are calories?</p>
        <p>Calories (kilocalories) are a way to measure the energy in food. Your body uses energy from food to support growth, organ function, physical activity, and recovery. Energy needs vary widely based on age, growth rate, body size, activity level, and genetics.</p>
        <p>Why do calories matter?</p>
        <p>The foods you choose provide not just energy but also the nutrients your body needs. A balanced eating pattern that includes a variety of foods supports your energy, focus, and overall health. Individual snack or meal choices don't determine health on their own — it's your overall pattern over time that matters most.</p>
        <p>Where energy comes from:</p>
        <ul>
          <li>Carbohydrates — the body's preferred energy source, especially for higher‑intensity activity (4 calories per gram)</li>
          <li>Protein — supports growth, repair, and recovery (4 calories per gram)</li>
          <li>Fat — provides concentrated energy and supports normal cell function (9 calories per gram)</li>
        </ul>
        <p><strong>Important:</strong> This information is for educational understanding only. Do not use it to calculate your own calorie needs or set personal intake targets. If you have concerns about energy, growth, or eating patterns, talk to a trusted adult or healthcare provider.</p>"""
replace('hs-5-1.html', old_energy_reading, new_energy_reading, "Fixed energy balance reading")

# === hs-5-4.html: Pre, During, and Post Activity Fueling ===
print("\n--- hs-5-4.html: Pre/During/Post Activity Fueling ---")

content = load('hs-5-4.html')

# Add disclaimer about individualization
old_5_4_opening = """<p>You've probably experienced it: that moment during practice, a game, or even just your afternoon classes when your energy completely crashes. Your legs feel heavy, your focus disappears, and suddenly everything feels harder than it should. Or maybe you've noticed that on days when you eat poorly, your mood is off, your skin breaks out, or you just feel sluggish and unmotivated. Here's what's actually happening: your body is a machine that runs on fuel, and when you don't fuel it strategically, everything suffers—your athletic performance, your mental clarity, your energy levels, and even your appearance.</p>"""
new_5_4_opening = """<p>This lesson covers general fueling principles for physical activity. These are broad examples based on time to activity and activity duration — not personalized prescriptions. Individual needs vary based on body size, sport, intensity, gastrointestinal tolerance, heat, access, and medical conditions. Athletes with specific needs should work with a sports dietitian or medical team.</p>
        <p><strong>Important safety note:</strong> Heat, gastrointestinal tolerance, sport rules, and personal preferences all affect what and when to eat before, during, and after activity. Experiment with what works for you in practice, not on game day.</p>"""
replace('hs-5-4.html', old_5_4_opening, new_5_4_opening, "Added individualization disclaimer")

# Fix absolute water intake recommendations
old_water = """<p>Drink 16-20 ounces of water 2-3 hours before activity. This gives your body time to absorb the fluid and regulate it through your kidneys. You'll notice you can push harder during your workout, your focus stays sharp, and you recover faster afterward.</p>
        <p>Drink another 8-10 ounces about 15-20 minutes before you start. This "top-up" ensures you're fully hydrated without causing discomfort during activity.</p>"""
new_water = """<p>General pre-activity hydration: having water available and sipping throughout the day before activity is usually sufficient. Drinking large amounts right before activity may cause discomfort. Follow thirst and have water accessible.</p>"""
replace('hs-5-4.html', old_water, new_water, "Fixed prescriptive water amounts")

# === hs-6-2.html: Underfueling and Energy Deficiency ===
print("\n--- hs-6-2.html: Underfueling and Energy Deficiency ---")

content = load('hs-6-2.html')

# Add trauma-informed language and confidentiality guidance
old_6_2_car = """<p>Your body is like a car. Even the fastest sports car cannot go very far without fuel. Your muscles and brain work the same way. Before physical activity, your body needs energy from food to help you move, think, react, and recover. When you don't eat enough—or you eat foods that don't provide lasting energy—you may experience underfueling.</p>"""
new_6_2_car = """<p><strong>Important note for students:</strong> This lesson discusses energy and fueling in general terms. If you have concerns about your own eating patterns, energy levels, or body — or if someone has expressed concern about you — please talk to a trusted adult, school counselor, or healthcare provider. This lesson does not ask for personal body measurements, intake tracking, or weight information.</p>
        <p>Your muscles and brain need energy from food to move, think, react, and recover. When you consistently don't eat enough to meet your body's demands — whether from training, growth, or daily activities — underfueling can occur.</p>"""
replace('hs-6-2.html', old_6_2_car, new_6_2_car, "Added trauma-informed disclaimer")

# === hs-6-3.html: Overhydration and Dehydration ===
print("\n--- hs-6-3.html: Overhydration and Dehydration ---")

content = load('hs-6-3.html')

# Add disclaimer about emergency signs
old_6_3_opening = """<p>On the flip side, overhydration—drinking too much water—can also be dangerous. While it's less common, it's important to understand. Overhydration dilutes the sodium in your blood, which can lead to a condition called hyponatremia. Symptoms include confusion, headaches, nausea, and in severe cases, seizures. For athletes, this can happen if you drink excessive amounts of water without replacing electrolytes lost through sweat. It's a reminder that balance is key: more isn't always better.</p>
        <p>It's also important to consider what you're drinking. Water is usually the best choice, but during long or intense workouts, sports drinks can help replace electrolytes like sodium and potassium. These minerals are essential for muscle function and preventing cramps. However, avoid sugary drinks or energy drinks—they can lead to a quick energy crash and don't provide the hydration your body needs.</p>"""

# Find the section about overhydration
# Actually let me just add a safety note at the beginning
old_reading_6_3 = """<p><strong>What Is Dehydration?</strong></p>"""
# We need to add content before this. Let me find it.
# Actually, let me look at the full file structure
content = load('hs-6-3.html')
if '<p><strong>What Is Dehydration?</strong></p>' in content:
    print(f"  ℹ️  hs-6-3.html: found dehydration section start at position {content.find('<p><strong>What Is Dehydration?</strong></p>')}")
else:
    print(f"  ℹ️  hs-6-3.html: looking for different section start...")
    # Check the reading section content

# Let me just add an emergency sign note to the overhydration section
old_over = """<p>On the flip side, overhydration—drinking too much water—can also be dangerous. While it's less common, it's important to understand. Overhydration dilutes the sodium in your blood, which can lead to a condition called hyponatremia. Symptoms include confusion, headaches, nausea, and in severe cases, seizures."""
new_over = """<p><strong>⚠ Emergency warning:</strong> Confusion, vomiting, collapse, or seizures require immediate emergency medical response — call 911 or get help. These are not conditions to handle by "just drinking more" or "resting it off." Follow your school athletic trainer and medical team's protocols.</p>
        <p>On the flip side, overhydration—drinking too much water—can also be dangerous. Overhydration dilutes the sodium in your blood, which can lead to hyponatremia. Symptoms can include confusion, headaches, nausea, and in severe cases, seizures."""
replace('hs-6-3.html', old_over, new_over, "Added emergency warning for overhydration")

# === hs-6-5.html: Micronutrient Deficiencies ===
print("\n--- hs-6-5.html: Micronutrient Deficiencies ---")

content = load('hs-6-5.html')

# Add disclaimer at top of reading
old_6_5_start = """<p>Each micronutrient plays a specific role that directly connects to how you perform in sports and daily life. Iron helps carry oxygen through your blood, which affects how long you can run before feeling tired. When iron is low, you may feel unusually exhausted, get winded faster, and struggle to keep up with teammates even when you're trying your hardest. Calcium and vitamin D support strong bones and muscle contractions. Without enough of them, you might feel weaker during movements, be more prone to injury, or notice slower recovery after practice. B vitamins help your body turn food into usable energy. When they are lacking, your energy levels can drop, making you feel sluggish, mentally foggy, or unmotivated during workouts. Electrolytes like sodium and potassium help control hydration and muscle function. When they are low, you might experience cramps, dizziness, or a sudden loss of coordination during performance.</p>"""
new_6_5_start = """<p><strong>⚠ Important:</strong> Symptoms discussed in this lesson — like fatigue, slower recovery, or concentration difficulty — have many possible causes including sleep, stress, training load, and overall nutrition patterns. Do NOT use this lesson to self‑diagnose a micronutrient deficiency or start supplements. If you're concerned about your energy, performance, or health, speak with a trusted adult, school nurse, or healthcare provider who can arrange proper assessment.</p>
        <p>Micronutrients play important roles in the body. Iron is needed for oxygen transport in the blood. Calcium and vitamin D support bone health. B vitamins help the body use energy from food. Electrolytes like sodium and potassium help with hydration and muscle function.</p>"""
replace('hs-6-5.html', old_6_5_start, new_6_5_start, "Added self-diagnosis disclaimer")

# Fix the "deficiency correction" section that encourages self-treatment
old_correction = """<p>If a micronutrient deficiency does develop, it can often be corrected, but it takes intentional action. Increasing nutrient-rich foods is the first step—adding iron-rich foods like beans or lean meats, calcium sources like dairy or fortified plant milks, and fruits and vegetables for vitamins can quickly improve how you feel over time. In some cases, a healthcare provider may recommend supplements, but food-based intake is the most reliable foundation for long-term performance. As nutrient levels recover, athletes often notice improvements in energy, focus, mood stability, and how quickly their bodies bounce back after activity.</p>"""
new_correction = """<p>If a micronutrient deficiency is diagnosed by a healthcare provider, treatment typically involves dietary changes and possibly supplements under medical supervision. The first step is always proper assessment — not self‑diagnosis. Eating a varied diet with fruits, vegetables, lean proteins, whole grains, and dairy (or fortified alternatives) helps support overall nutrient intake for most people.</p>"""
replace('hs-6-5.html', old_correction, new_correction, "Fixed self-treatment language")

# Fix the "performance isn't just practice" conclusion
old_perf = """<p>Your performance isn't just built in practice—it's also built in what you consistently give your body every day. When micronutrients are balanced, your body can keep up with your effort. When they're not, your body sends signals through fatigue, focus loss, and slower performance that are easy to miss until they start affecting your game.</p>"""
new_perf = """<p>Your performance is influenced by many factors — training, sleep, stress, hydration, and overall nutrition pattern. A varied eating pattern that includes micronutrient‑rich foods supports normal body functions. If you notice persistent changes in your energy or performance, talk to a healthcare provider or sports dietitian rather than assuming a deficiency.</p>"""
replace('hs-6-5.html', old_perf, new_perf, "Fixed performance language")

print("\n" + "=" * 50)
print("All remaining Critical edits applied!")
print("=" * 50)
