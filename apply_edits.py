#!/usr/bin/env python3
"""
Apply audit revisions to WellSnax curriculum HTML files.
Processes all items in audit.csv, applying the recommended solutions.
"""
import csv
import os
import re
import sys

REPO = "/Users/kylebridges/Desktop/curriculum"

def read_file(path):
    with open(os.path.join(REPO, path), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(os.path.join(REPO, path), 'w', encoding='utf-8') as f:
        f.write(content)

def edit_file(path, old_text, new_text):
    """Replace exact old_text with new_text in file. Returns True if changed."""
    content = read_file(path)
    if old_text not in content:
        print(f"  ⚠️  WARNING: old text not found in {path}")
        print(f"   Looking for: {old_text[:80]}...")
        return False
    content = content.replace(old_text, new_text, 1)
    write_file(path, content)
    print(f"  ✅ Applied edit in {path}")
    return True

def modify_content(path, modifications):
    """Apply multiple modifications to a file. Returns True if any changed."""
    content = read_file(path)
    changed = False
    for old_text, new_text in modifications:
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            changed = True
        else:
            print(f"  ⚠️  Warning: text not found for edit in {path}: {old_text[:60]}...")
    if changed:
        write_file(path, content)
        print(f"  ✅ Applied {len(modifications)} edits to {path}")
    return changed

# ===================== CRITICAL ITEMS =====================

def apply_critical_edits():
    # --- 1. lesson-1-7: Quiz Q3 cereal comparison ---
    old_q3 = """<div class="quiz-question">
          <p class="q">3. Two packaged cereals have the same calories per serving. One has 3 g of fiber and 8 g of added sugars; the other has 1 g of fiber and 2 g of added sugars. Which is the better choice?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> The cereal with 1 g fiber and 2 g added sugars</li>
            <li class="correct"><span class="letter">B.</span> The cereal with 3 g fiber and 8 g added sugars <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">C.</span> Both are equally healthy because calories are the same</li>
            <li class=""><span class="letter">D.</span> Neither — calories are the only important factor</li>
          </ul>
        </div>"""
    new_q3 = """<div class="quiz-question">
          <p class="q">3. Two packaged cereals have the same calories per serving. Cereal A has 5 g of fiber and 2 g of added sugars; Cereal B has 1 g of fiber and 8 g of added sugars. Which cereal is clearly the better choice based on fiber and added sugar?</p>
          <ul class="options">
            <li class="correct"><span class="letter">A.</span> Cereal A (5 g fiber, 2 g added sugars) is higher in fiber and lower in added sugars <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">B.</span> Cereal B (1 g fiber, 8 g added sugars)</li>
            <li class=""><span class="letter">C.</span> Both are equally healthy because calories are the same</li>
            <li class=""><span class="letter">D.</span> Neither — calories are the only important factor</li>
          </ul>
          <p style="font-size:.85rem;color:#64748b;margin-top:.5rem;">Note: When a clear choice exists, compare fiber and added sugar together. When tradeoffs exist, consider the overall context of your eating pattern.</p>
        </div>"""
    edit_file('lesson-1-7.html', old_q3, new_q3)

    # --- 2. lesson-1-11: Special Dietary Needs ---
    # Fix the reading - allergy statement about epinephrine
    old_allergy = """<li>Food allergies (immune system reacts strongly) — requires epinephrine (Epi-Pen)</li>"""
    new_allergy = """<li>Food allergies (immune system reacts strongly) — epinephrine is the first-line emergency treatment for suspected anaphylaxis; always follow your medical plan</li>"""
    edit_file('lesson-1-11.html', old_allergy, new_allergy)

    # Fix diabetes statement in reading
    old_diabetes = """<li><strong>Diabetes:</strong> Monitor carbohydrate intake, choose whole grains, lean proteins, healthy fats</li>"""
    new_diabetes = """<li><strong>Diabetes:</strong> Follow a clinician-directed plan for managing carbohydrate intake and blood sugar</li>"""
    edit_file('lesson-1-11.html', old_diabetes, new_diabetes)

    # Fix the practical tips to add school emergency plan language
    old_tips = """<p><strong>Practical tips:</strong></p>
        <ul>
          <li>Always tell an adult if you have a food allergy</li>
          <li>Read ingredient labels</li>
          <li>Respect classmates' dietary needs</li>
          <li>In case of severe allergic reaction, get an adult and call emergency help immediately</li>
        </ul>"""
    new_tips = """<p><strong>Practical tips:</strong></p>
        <ul>
          <li>Always tell an adult if you have a food allergy</li>
          <li>Read ingredient labels</li>
          <li>Respect classmates' dietary needs</li>
          <li>In case of suspected anaphylaxis, epinephrine is the first-line emergency treatment; get an adult and call emergency help immediately</li>
          <li>Follow your school health plan and clinician-directed dietary recommendations</li>
        </ul>"""
    edit_file('lesson-1-11.html', old_tips, new_tips)

    # Fix Quiz Q6 - lactose intolerance (avoid implying avoid milk entirely)
    old_q6 = """<div class="quiz-question">
          <p class="q">6. A student has lactose intolerance. Which lunch choice is most appropriate?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Yogurt parfait with regular milk and granola</li>
            <li class=""><span class="letter">B.</span> Cheese pizza with extra cheese</li>
            <li class="correct"><span class="letter">C.</span> Sandwich with lean turkey and a fruit cup (no milk) <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">D.</span> Milkshake and fries</li>
          </ul>
        </div>"""
    new_q6 = """<div class="quiz-question">
          <p class="q">6. A student has lactose intolerance. Which lunch choice is most appropriate?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Yogurt parfait with regular milk and granola</li>
            <li class=""><span class="letter">B.</span> Cheese pizza with extra cheese</li>
            <li class="correct"><span class="letter">C.</span> Sandwich with lean turkey, a fruit cup, and lactose-free milk or a fortified alternative <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">D.</span> Milkshake and fries</li>
          </ul>
        </div>"""
    edit_file('lesson-1-11.html', old_q6, new_q6)

    # --- 3. lesson-2-2: Daily Hydration Guidelines ---
    # Fix 6-8 cups as universal
    old_hydration_target = """<p>It is recommended that 11-14 year olds consume about 6-8 cups or about 48 to 64 ounces of water each day.</p>"""
    new_hydration_target = """<p>Total water needs vary by age, sex, activity level, and climate. General ranges exist (for example, about 7-10 cups total water per day for most 11-14 year olds, including water from beverages and food), but individual needs differ. Pay attention to thirst, activity, and weather.</p>"""
    edit_file('lesson-2-2.html', old_hydration_target, new_hydration_target)

    # Remove coffee from recommended beverages
    old_beverages = """<ul>
          <li>Water</li>
          <li>Milk</li>
          <li>100% fruit and vegetable juices</li>
          <li>Tea</li>
          <li>Coffee</li>
        </ul>"""
    new_beverages = """<ul>
          <li>Water</li>
          <li>Milk or fortified alternatives</li>
          <li>100% fruit and vegetable juices (in modest portions)</li>
          <li>Herbal or non-caffeinated tea</li>
        </ul>"""
    edit_file('lesson-2-2.html', old_beverages, new_beverages)

    # Fix activity calculator - remove personal data
    old_activity = """<p>Using the online hydration calculator, calculate how much water you should drink in a day based on your age, gender, height, weight, activity level, climate, and additional water sources.</p>"""
    new_activity = """<p>Using the classroom example provided by your teacher, practice estimating total water needs. Discuss how age, activity level, and climate affect individual hydration needs without entering personal data.</p>"""
    edit_file('lesson-2-2.html', old_activity, new_activity)

    # Fix Quiz Q1 to remove the fixed 6-8 cups as universal
    old_q1 = """<p class="q">1. How much water should most kids your age drink each day?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> 2-3 cups</li>
            <li class="correct"><span class="letter">B.</span> 6-8 cups <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">C.</span> 10-12 cups</li>
            <li class=""><span class="letter">D.</span> 15+ cups</li>
          </ul>"""
    new_q1 = """<p class="q">1. Which statement best describes daily water needs for 11-14 year olds?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Every person needs exactly 8 cups of water, no exceptions</li>
            <li class="correct"><span class="letter">B.</span> Needs vary based on age, activity level, climate, and individual differences, with general ranges as a starting point <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">C.</span> Water needs are the same for everyone regardless of activity</li>
            <li class=""><span class="letter">D.</span> Only athletes need to think about water intake</li>
          </ul>"""
    edit_file('lesson-2-2.html', old_q1, new_q1)

    # --- 4. lesson-2-4: Dehydration and its Effects ---
    # Fix urine color chart
    old_urine = """<p><strong>The best way to tell how hydrated you are:</strong> Look at the color of your urine.</p>
        <ul>
          <li>Transparent/Clear = Overhydrated (cut back)</li>
          <li>Pale Yellow = Healthy and hydrated</li>
          <li>Dark Yellow = Mild dehydration (drink water)</li>
          <li>Amber = Dehydrated (drink water soon)</li>
          <li>Dark Brown = Severe dehydration (see a doctor)</li>
        </ul>"""
    new_urine = """<p><strong>Urine color as a rough screening tool:</strong> Urine color can be affected by medicines, foods, and illness, so use it as one clue among several.</p>
        <ul>
          <li>Pale Yellow = Generally well-hydrated</li>
          <li>Dark Yellow = May be a sign to drink water soon</li>
          <li>Clear = Could mean you've had plenty, but can also happen from other factors</li>
          <li>Dark Brown, red, or unusual colors = Could be a sign of a medical issue; tell an adult</li>
        </ul>
        <p><strong>Important:</strong> Confusion, chest pain, or inability to keep fluids down require immediate adult/medical help — do not just "stop and drink."</p>"""
    edit_file('lesson-2-4.html', old_urine, new_urine)

    # Fix Quiz Q7 - chest pain grouped with simply drinking
    old_q7_2 = """<p class="q">7. Which sign means you should stop exercising and drink water immediately?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Feeling a little tired</li>
            <li class=""><span class="letter">B.</span> Sweating normally</li>
            <li class="correct"><span class="letter">C.</span> Severe dizziness, confusion, or chest pain <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">D.</span> Having slightly dry lips</li>
          </ul>"""
    new_q7_2 = """<p class="q">7. Which signs mean you should stop activity and get adult/medical help immediately?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Slightly dry lips</li>
            <li class=""><span class="letter">B.</span> Normal sweating</li>
            <li class="correct"><span class="letter">C.</span> Confusion, chest pain, or inability to keep fluids down <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">D.</span> Feeling a little tired</li>
          </ul>"""
    edit_file('lesson-2-4.html', old_q7_2, new_q7_2)

    # Fix Q10 - remove "most affected system"
    old_q10 = """<div class="quiz-question">
          <p class="q">10. Which body system is most affected by severe dehydration?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> The skeletal system (bones)</li>
            <li class="correct"><span class="letter">B.</span> The circulatory system (heart and blood) <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">C.</span> The nervous system (brain and nerves)</li>
            <li class=""><span class="letter">D.</span> The digestive system (stomach and intestines)</li>
          </ul>
        </div>"""
    new_q10 = """<div class="quiz-question">
          <p class="q">10. Severe dehydration can affect multiple body systems. Which of these is a possible consequence of severe dehydration?</p>
          <ul class="options">
            <li class=""><span class="letter">A.</span> Only mild thirst</li>
            <li class=""><span class="letter">B.</span> Improved athletic performance</li>
            <li class="correct"><span class="letter">C.</span> Reduced blood volume, kidney stress, and heat-related illness <span class="correct-badge">Correct</span></li>
            <li class=""><span class="letter">D.</span> Stronger bones</li>
          </ul>
        </div>"""
    edit_file('lesson-2-4.html', old_q10, new_q10)

    # --- 5. lesson-2-8: Hydration and Health Conditions ---
    # Replace the reading with medical/clinical disclaimer language
    old_health_reading = """<p><strong>Why it matters:</strong> Hydration plays a role in nearly the entire body. Some health conditions can throw off the balance of fluids.</p>
        <p><strong>Health conditions made worse by dehydration:</strong></p>
        <ul>
          <li>ADHD, Anxiety, Asthma, Celiac disease, Diabetes, UTIs, Sickle cell disease</li>
        </ul>
        <p><strong>Conditions that cause fluid loss:</strong></p>
        <ul>
          <li>Celiac and IBS, Cystic Fibrosis, Diabetes, Kidney disease</li>
        </ul>
        <p><strong>Dehydration affects these conditions by causing:</strong></p>
        <ul>
          <li>Fatigue, headaches, weakness, difficulty concentrating, mood changes</li>
        </ul>
        <p>When the body is properly hydrated, it can function as it is supposed to, even with health conditions. This can lead to a minimization of symptoms and better overall health.</p>"""
    new_health_reading = """<p><strong>Why it matters:</strong> Hydration plays a role in nearly the entire body. Some health conditions can affect fluid balance, which is why individual hydration needs can vary.</p>
        <p><strong>Important:</strong> Students with fluid restrictions or health conditions that affect hydration must follow their clinician's guidance and school health plan. This lesson discusses general principles — it does not replace medical advice.</p>
        <p><strong>Things that can affect hydration needs:</strong></p>
        <ul>
          <li>Some medical conditions may change how the body handles fluids</li>
          <li>Certain medications can affect fluid or electrolyte balance</li>
          <li>Illness with fever, vomiting, or diarrhea increases fluid needs</li>
        </ul>
        <p><strong>Key takeaway:</strong> Hydration needs are personal. What works for one person may not work for another, especially for those with health conditions. Always follow your clinician and school health plan.</p>"""
    edit_file('lesson-2-8.html', old_health_reading, new_health_reading)

    # --- 6. lesson-3-2: Snack Nutrients ---
    # Fix "6 main nutrients" - replace fiber with water
    old_nutrients = """<p>There are 6 main nutrients that the body uses: carbohydrates, protein, fats, vitamins, minerals, and fiber.</p>"""
    new_nutrients = """<p>There are 6 essential nutrient categories the body needs: carbohydrates, protein, fats, vitamins, minerals, and water. Fiber is a type of carbohydrate that supports digestion.</p>"""
    edit_file('lesson-3-2.html', old_nutrients, new_nutrients)

    # Fix balanced snack formula
    old_snack_formula = """<p>A balanced snack includes: a carbohydrate, protein, fruit or vegetable, healthy fats, and limited added sugar.</p>"""
    new_snack_formula = """<p>A balanced snack can include flexible pairings — for example, a carbohydrate plus protein, or adding a fruit or vegetable. The right combination depends on hunger level, timing, and activity needs.</p>"""
    edit_file('lesson-3-2.html', old_snack_formula, new_snack_formula)

    # --- 7. lesson-3-5: Impact of Snack Choices ---
    # Replace the deterministic reading
    old_snack_impact = """<p><strong>Sugary Snacks</strong> (candy, cookies, ice cream)</p>
        <ul>
          <li>Immediate: Energy rushes and crashes, increased cravings, brain fog</li>
          <li>Long-term: Weight gain, tooth decay, Type 2 diabetes</li>
        </ul>
        <p><strong>Salty, Fried Snacks</strong> (chips, crackers, french fries)</p>
        <ul>
          <li>Immediate: Water retention, bloating</li>
          <li>Long-term: High blood pressure, heart disease, inflammation</li>
        </ul>
        <p><strong>Healthy Snacks</strong> (veggies and hummus, fruit and peanut butter, nuts)</p>
        <ul>
          <li>Immediate: Boosts energy, balanced blood sugar, sharper focus</li>
          <li>Long-term: Reduces risk of chronic illness, better weight management, improved heart and gut health</li>
        </ul>
        <p><strong>Why your snack choices matter now:</strong> Your body is transitioning to adulthood. Healthy muscle and bone development, brain development, mood, athletic performance, and metabolism all depend on good nutrition.</p>"""
    new_snack_impact = """<p><strong>Snack choices and your body: the bigger picture</strong></p>
        <p>No single snack determines your health. What matters most is your overall eating pattern over time.</p>
        <p><strong>Frequent high-added-sugar intake</strong> — Having snacks with lots of added sugar on a regular basis can increase the risk of tooth decay and may contribute to energy ups and downs. Your body can handle occasional treats; the pattern overall is what matters.</p>
        <p><strong>Frequent high-sodium intake</strong> — Regularly eating foods high in sodium can contribute to higher blood pressure over time. Enjoying salty snacks sometimes is fine, but making them a daily habit may have long-term effects.</p>
        <p><strong>Snacks with fiber, protein, and nutrients</strong> — Snacks like fruits, vegetables, nuts, yogurt, or whole grains can help provide steady energy, support fullness, and contribute to overall nutrient needs across your day.</p>
        <p><strong>Why your overall pattern matters:</strong> Your body is growing and developing. A pattern that includes a variety of nutrient-dense foods supports energy, focus, dental health, and healthy development. One snack won't make or break your health — it's your consistent choices that count.</p>"""
    edit_file('lesson-3-5.html', old_snack_impact, new_snack_impact)

    # --- 8. lesson-3-8: Food Allergies ---
    # Fix reading about severe reactions
    old_severe_reaction = """<p><strong>For severe reactions:</strong> Epinephrine (Epi-Pen) and call 911.</p>"""
    new_severe_reaction = """<p><strong>For suspected anaphylaxis:</strong> Epinephrine is the first-line emergency treatment. Emergency services and adults must be contacted immediately. Follow the school emergency plan.</p>"""
    edit_file('lesson-3-8.html', old_severe_reaction, new_severe_reaction)

    # Fix the "How to keep people safe" section
    old_safety = """<p><strong>How to keep people safe:</strong></p>
        <ul>
          <li>Ask about allergies</li>
          <li>Check ingredient lists</li>
          <li>Avoid cross-contamination</li>
          <li>Keep allergy-free food separate</li>
        </ul>"""
    new_safety = """<p><strong>School safety practices:</strong></p>
        <ul>
          <li>Know and follow the school emergency plan for allergic reactions</li>
          <li>Check ingredient lists and allergen statements on every package</li>
          <li>Avoid food-sharing to prevent cross-contact</li>
          <li>Keep allergy-free foods separate from potential allergens</li>
          <li>Know the difference between intolerance, allergy, and anaphylaxis</li>
        </ul>"""
    edit_file('lesson-3-8.html', old_safety, new_safety)

    # --- 9. hs-1-1: Macronutrients (HS) ---
    # Replace the opening paragraphs
    old_hs_opening = """<p>Close your eyes for a second. How do you feel at this exact moment? Energized? Sluggish? Focused? Scattered?</p>
        <p>Here's the thing: what you ate today is literally the reason. Not tomorrow. Not next week. Today. Your breakfast, your snack, that energy drink—they're all affecting how your brain works, how fast you can move, and how you handle stress right now.</p>
        <p>The nutrients you eat are your body's operating system. And we're going to show you exactly how.</p>
        <p>What Are Macronutrients?</p>"""
    new_hs_opening = """<p>Have you ever noticed that your energy and focus can vary throughout the day? What you eat plays a role, along with sleep, stress, hydration, and activity level.</p>
        <p>Macronutrients — carbohydrates, protein, and fat — are the nutrients your body needs in the largest amounts. They provide energy, support growth, and help your body function. Let's look at how they work.</p>
        <p>What Are Macronutrients?</p>"""
    edit_file('hs-1-1.html', old_hs_opening, new_hs_opening)

    # Fix the "Your Habit" table - remove causal/metabolism claims
    old_habit_table = """<p>Your Habit</p>
        <p>What Happens TODAY</p>
        <p>What Happens Over Time</p>
        <p>Eating carbs before class</p>
        <p>Brain fog lifts, focus sharpens</p>
        <p>Stable energy levels, better grades</p>
        <p>Skipping breakfast</p>
        <p>Low energy, hard to concentrate</p>
        <p>Slower metabolism, weight gain, fatigue</p>
        <p>Eating protein with meals</p>
        <p>Feel full longer, less snacking</p>
        <p>Stronger muscles, faster recovery, better mood</p>
        <p>Choosing mostly processed foods</p>
        <p>Energy crash after 1-2 hours</p>
        <p>Increased risk of diabetes, heart disease, obesity</p>
        <p>Including healthy fats</p>
        <p>Better concentration, healthier skin</p>
        <p>Reduced inflammation, better brain function, heart health</p>
        <p>Drinking lots of water with meals</p>
        <p>Better digestion, clearer skin</p>
        <p>Improved kidney function, better hydration</p>
        <hr style="margin:1rem 0;border:none;border-top:1px solid #e2e8f0;">"""
    new_habit_table = """<p>How eating patterns can influence how you feel:</p>
        <ul>
          <li><strong>Eating carbohydrates before class</strong> — can help provide energy for your brain and body; may be associated with steady focus</li>
          <li><strong>Skipping breakfast</strong> — some students find it harder to concentrate when hungry; energy and focus vary by individual</li>
          <li><strong>Eating protein with meals</strong> — can support fullness between meals and provide amino acids your body needs</li>
          <li><strong>Choosing mostly processed foods</strong> — a pattern high in ultra-processed foods is associated with higher risk of some health conditions over time</li>
          <li><strong>Including unsaturated fats</strong> — supports normal body functions like nutrient absorption and cell health</li>
          <li><strong>Drinking water with meals</strong> — supports digestion and overall hydration</li>
        </ul>
        <hr style="margin:1rem 0;border:none;border-top:1px solid #e2e8f0;">"""
    edit_file('hs-1-1.html', old_habit_table, new_habit_table)

    # Fix "The Bottom Line" - remove fear-based language
    old_bottom_line = """<p>The Bottom Line</p>
        <p>Without these nutrients, your body goes into "preservation mode"—organ systems slow down, and your body starts breaking down its own tissue for energy. That's not just uncomfortable; it's dangerous.</p>
        <p>You get to choose every single meal, whether you're fueling up or breaking down. Now you know what each macronutrient does. What will you choose today?</p>"""
    new_bottom_line = """<p>The Big Picture</p>
        <p>Macronutrients provide the energy and building blocks your body needs to grow, learn, and stay active. Eating a variety of foods with carbohydrates, protein, and fat helps support your overall health. No single meal determines your health — it's your overall eating pattern that matters.</p>"""
    edit_file('hs-1-1.html', old_bottom_line, new_bottom_line)

    # --- 10. hs-1-6: Macronutrients and Physical Activity ---
    # Add statement about medical conditions and sports dietitian
    old_hs6_reading_end = """<p>Carbohydrates: Your Quick Energy Powerhouse</p>"""
    # Add a disclaimer before the reading content
    old_hs6_opening = """<p>Picture this: You're halfway through your soccer game, basketball practice, or workout. You started strong, felt great in the first half, but now? Your legs feel heavy. Your mind is foggy. You can't quite push as hard as you want to, and you're frustrated because you know you have more in you. What's happening? It's not a lack of willpower—it's likely a fuel problem.</p>
        <p>The truth is, what you eat before, during, and after physical activity directly impacts how you perform, how quickly you recover, and even how you feel for the rest of the day. Macronutrients—carbohydrates, proteins, and fats—are the building blocks that keep your body energized, rebuild muscle, and keep your hormones balanced. When you time them right, you'll notice the difference immediately: more energy, sharper focus, better recovery, and stronger athletic performance.</p>
        <p>Carbohydrates: Your Quick Energy Powerhouse</p>"""
    new_hs6_opening = """<p>What you eat before, during, and after physical activity can influence how you perform and recover. This lesson covers general fueling principles organized by activity duration, intensity, and time available before exercise.</p>
        <p><strong>Important note:</strong> Athletes with medical conditions or high training loads should follow guidance from a sports dietitian or medical team. These are general principles, not personalized prescriptions.</p>
        <p>Carbohydrates: Your Quick Energy Powerhouse</p>"""
    edit_file('hs-1-6.html', old_hs6_opening, new_hs6_opening)

    # --- 11. hs-1-7: Counting Macronutrients ---
    # Rename the lesson title and replace the entire reading section
    # The reading section contains BMR calculations, personal targets, etc.
    # We need to preserve the structure but change the content
    
    # First, rename the lesson title
    old_title_hs1_7 = "<h1>Counting Macronutrients</h1>"
    new_title_hs1_7 = "<h1>Estimating and Balancing Macronutrient Sources</h1>"
    edit_file('hs-1-7.html', old_title_hs1_7, new_title_hs1_7)
    
    old_page_title = "<title>Lesson 7: Counting Macronutrients — WellSnax Curriculum</title>"
    new_page_title = "<title>Lesson 7: Estimating and Balancing Macronutrient Sources — WellSnax Curriculum</title>"
    edit_file('hs-1-7.html', old_page_title, new_page_title)

    # Replace the reading section that has BMR/TDEE calculations
    # Need to find the exact text to replace
    old_reading_hs17_start = """<p>Understanding Your Macronutrients</p>
        <p>You know that feeling around 2 p.m. when you hit a wall? Your eyes get heavy, your focus disappears, and you can barely get through your last class or practice. Or maybe you're an athlete who feels completely drained halfway through a game, even though you "ate breakfast." Or perhaps you're trying to build muscle, feel confident in your body, or just want to stop the energy roller coaster that's been messing with your mood and performance.</p>
        <p>Here's what most people don't realize: the food you eat isn't just about calories—it's about the specific mix of nutrients your body needs to actually work the way you want it to. This mix is called your macronutrients, and learning to balance them could be the difference between crushing your day and barely getting through it.</p>
        <p>Why Tracking Macronutrients Actually Matters to You</p>
        <p>You'll finally understand what's really in your food. Most people have no idea what they're eating or how it impacts their energy, mood, and performance. When you start tracking, you realize that a candy bar and a chicken breast might have similar calories, but they affect your body completely differently. One leaves you crashed and tired; the other keeps you steady and focused.</p>
        <p>You'll build habits that last. Learning to read food labels and manage portion sizes now means you'll never feel confused about nutrition again. This knowledge stays with you for life—and it's way more powerful than any diet.</p>
        <p>You'll stop the energy crashes. The right balance of macronutrients keeps your blood sugar stable throughout the day. No more 3 p.m. crash. No more feeling shaky or irritable. Just consistent energy when you need it most.</p>
        <p>You'll recover better and perform stronger. If you're an athlete or active person, macronutrients are everything. The right fuel before activity powers your performance. The right recovery nutrition afterward rebuilds your muscles so you actually get stronger. Without it, you're just going through the motions.</p>
        <p>You'll feel more satisfied. Eating the right macronutrient balance keeps you full longer and prevents those constant cravings that derail your goals. You'll actually feel good, not deprived.</p>
        <p>How to Calculate Your Personal Macronutrient Targets</p>
        <p>Step 1: Find Your Basal Metabolic Rate (BMR)</p>
        <p>Your BMR is how many calories your body burns just existing—breathing, thinking, keeping your heart beating. It's your baseline. Here's the formula based on your sex:</p>
        <p>Males:</p>
        <p>(10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5 = BMR</p>
        <p>Females:</p>
        <p>(10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161 = BMR</p>
        <p>Why this matters: This is the starting point. It tells you your body's baseline demand for energy. Knowing this helps you understand how much fuel you actually need—not what diet culture tells you to eat, but what your body requires.</p>
        <p>Step 2: Multiply by Your Activity Level to Get Your TDEE (Total Daily Energy Expenditure)</p>
        <p>Your activity level is how much you move around. Multiply your BMR by the factor that matches your lifestyle:</p>
        <ul>
          <li>Sedentary (mostly sitting): BMR × 1.2</li>
          <li>Lightly Active (light exercise 1-3 days/week): BMR × 1.375</li>
          <li>Moderately Active (exercise 3-5 days/week): BMR × 1.55</li>
          <li>Very Active (exercise 6-7 days/week or intense sports): BMR × 1.725</li>
          <li>Super Active (intense daily training or physical job): BMR × 1.9</li>
        </ul>
        <p>The result is your TDEE—how many calories you actually burn in a day.</p>
        <p>Why this matters: This is where your personal goals come in. Your TDEE tells you exactly how much energy your body needs based on what you actually do. An athlete training hard needs way more fuel than someone who sits in class all day. Honoring that difference means you have the energy to perform and recover—or, if you're trying to lose fat, you know how much you can safely reduce without tanking your performance and mood.</p>
        <p>Step 3: Adjust for Your Goal</p>
        <p>Now you customize based on what you want:</p>
        <ul>
          <li>Building Muscle: TDEE + 250–500 calories</li>
          <li>Losing Fat: TDEE − 250–500 calories</li>
          <li>Maintaining Weight: TDEE stays the same</li>
        </ul>
        <p>Why this matters: This is crucial. If you want to build muscle or lose fat, you can't just eat random amounts. You need a specific target. But notice the range—you're not doing anything extreme. Small, sustainable adjustments are what actually work and keep you healthy.</p>
        <p>Step 4: Calculate Protein</p>
        <p>Protein is your muscle-building, recovery, and satiety superpower.</p>
        <p>Formula: Target weight in lbs × (1.25–1.5g) = grams of protein per day</p>
        <p>Then convert to calories: Protein grams × 4 = calories from protein</p>
        <p>Why this matters: Protein is non-negotiable if you want to feel full, build or maintain muscle, and recover from activity. It's also the most satiating macronutrient, meaning it keeps you feeling satisfied longer. This is why you don't feel as hungry after eating chicken compared to eating bread—even if they have similar calories. Prioritize protein and you'll naturally make better choices throughout the day.</p>
        <p>Step 5: Calculate Fats</p>
        <p>Fats support hormone production, brain function, and nutrient absorption. Don't skip them.</p>
        <p>Formula: Adjusted total calories × 0.25 = fat calories</p>
        <p>Then convert to grams: Fat calories ÷ 9 = grams of fat per day</p>
        <p>Why this matters: Fats are essential for your hormones, mood, and brain power. Cutting them out leaves you feeling foggy, irritable, and unmotivated. The right amount of fat supports focus, stable mood, and energy.</p>
        <p>Step 6: Calculate Carbohydrates</p>
        <p>Carbs are your energy source—especially important if you're active or an athlete.</p>
        <p>Formula: Adjusted total calories − (protein calories + fat calories) = carbohydrate calories</p>
        <p>Then convert to grams: Carbohydrate calories ÷ 4 = grams of carbs per day</p>
        <p>Why this matters: Carbs fuel your brain and muscles. They're what gives you energy during workouts, focus in class, and the stamina to get through your day. If you cut carbs too low, you'll feel sluggish, unfocused, and your athletic performance will suffer. The right amount of carbs is what keeps you performing at your best.</p>
        <p>The General Macronutrient Balance</p>
        <p>A solid baseline to aim for is:</p>
        <ul>
          <li>50% Carbohydrates (fuel and brain power)</li>
          <li>25% Protein (muscle, recovery, and satiety)</li>
          <li>25% Fats (hormones, mood, and absorption)</li>
        </ul>
        <p>This balance works for most high schoolers and supports both brain power and physical activity.</p>
        <p>Important Reminders</p>
        <p>Track macronutrients with adult supervision. Always do this under the guidance of a parent, doctor, or registered dietician. They can make sure you're doing it safely and that your targets are appropriate for your age and development.</p>
        <p>Never drop your calories too low. Restricting calories too much will actually harm your physical development into adulthood and tank your athletic performance. You need enough fuel to grow, learn, and perform. Slow, sustainable changes are what work.</p>
        <p>Use tracking tools to make it easier. Apps like Cronometer or MacrosFirst make tracking simple and convenient. You don't have to do math in your head—let the app do it.</p>
        <p>Track consistently for at least 2 weeks. You need time to see what's actually working. After 2 weeks, look at the results—are you gaining or losing weight at a reasonable pace? If things are moving too fast or too slow, adjust your calorie intake slightly and try again.</p>
        <p>Remember: counting macros isn't required to be healthy. If tracking stresses you out or makes eating feel like a chore, stop. You don't have to count every gram to be healthy. Instead, focus on eating whole foods with a priority on protein, and practice mindful eating—listen to your hunger and fullness cues. Your body often knows what it needs.</p>"""
    new_reading_hs17 = """<p>Estimating and Balancing Macronutrient Sources</p>
        <p>Understanding macronutrients in the foods you eat is a useful skill. Rather than tracking exact grams or personal targets, this lesson focuses on label literacy, meal-building examples, and learning to recognize macronutrient sources.</p>
        <p><strong>A note on safety:</strong> This lesson uses general examples only. Students should not set personal macronutrient targets, log their own food intake for counting purposes, or weigh foods without a medical or clinical need. If you have concerns about your eating patterns, energy, or growth, talk to a trusted adult, school counselor, or healthcare provider.</p>
        <p>Using Food Labels to Identify Macronutrients</p>
        <ul>
          <li><strong>Carbohydrates</strong> are listed as "Total Carbohydrate" on the Nutrition Facts label, with subcategories for dietary fiber and added sugars.</li>
          <li><strong>Protein</strong> is listed as "Protein" on the label.</li>
          <li><strong>Fat</strong> is listed as "Total Fat," with subcategories for saturated fat and trans fat.</li>
        </ul>
        <p>Being able to find these on a label helps you understand what's in packaged foods without needing to track daily targets.</p>
        <p>Building Balanced Meals: Examples for Different Schedules</p>
        <ul>
          <li><strong>Busy school morning:</strong> Oatmeal with berries and milk, or whole-grain toast with peanut butter and a banana</li>
          <li><strong>Lunch from the cafeteria:</strong> A sandwich, piece of fruit, and a carton of milk or water</li>
          <li><strong>After-school snack:</strong> Yogurt with granola, or apple slices with cheese</li>
          <li><strong>Post-practice:</strong> A turkey wrap, fruit, and water</li>
        </ul>
        <p>Discussion Questions (for class use, not personal tracking)</p>
        <ol>
          <li>Using the food label from a sample packaged meal, identify the grams of carbohydrate, protein, and fat per serving. How might these change if someone ate two servings?</li>
          <li>Look at two different types of crackers. How do their carbohydrate, protein, and fat amounts compare? Does one have more fiber or less added sugar?</li>
          <li>Build a sample meal for a student who has soccer practice after school. What would you include and why?</li>
        </ol>
        <p><strong>Key takeaway:</strong> Understanding macronutrient sources helps you make informed choices — but you don't need to count or track them to eat well. If you have specific health, performance, or body concerns, reach out to a qualified professional rather than self-prescribing a diet.</p>"""
    edit_file('hs-1-7.html', old_reading_hs17_start, new_reading_hs17)

    print("\n✅ All Critical edits applied!")
    return True

if __name__ == "__main__":
    os.chdir(REPO)
    print("Starting Critical edits...")
    apply_critical_edits()
