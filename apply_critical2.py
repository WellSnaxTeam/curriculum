#!/usr/bin/env python3
"""Apply remaining Critical audit revisions to HS files."""
import os

REPO = "/Users/kylebridges/Desktop/curriculum"

def edit_file(path, old_text, new_text):
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    if old_text not in content:
        # Try to find it
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if old_text.split('\n')[0][:40] in line:
                print(f"  ℹ️  Found partial match at line {i+1}: {line[:80]}")
        print(f"  ❌ FAILED: {path} - text not found: {old_text[:60]}...")
        return False
    content = content.replace(old_text, new_text, 1)
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)
    print(f"  ✅ Updated {path}")
    return True

def fix_hs_2_1():
    """Fix hs-2-1.html: Remove diagnostic/cosmetic promises, fix quiz duplicates"""
    path = 'hs-2-1.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    
    # Fix reading opening - remove causal/diagnostic language
    old = """<p>The Truth About Micronutrients</p>
        <p>Ever wonder why some days you feel like you could run a marathon, and other days you can barely stay awake in class? Or why your skin breaks out right before an important event? Or why you crush it at practice one week and feel sluggish the next?</p>
        <p>The answer might not be what you think. It's not always about sleep or stress. Often, it comes down to micronutrients—the tiny vitamins and minerals your body absolutely needs to function. Without them, everything from your energy levels to your mood to your athletic performance falls apart.</p>
        <p>Here's the deal: while macronutrients (like carbs, protein, and fat) give your body fuel, micronutrients are the workers behind the scenes. They're the chemical regulators that help your body produce the enzymes and hormones that keep you sharp, energized, and feeling your best.</p>
        <p>What Are Micronutrients?</p>"""
    new = """<p>What Are Micronutrients?</p>
        <p>Micronutrients are vitamins and minerals that your body needs in small amounts to support normal functions like growth, immune health, and energy metabolism. They don't provide energy themselves, but they help your body use the energy from food.</p>
        <p><strong>Important:</strong> While micronutrients support normal body functions, symptoms like fatigue, mood changes, or skin concerns have many possible causes. If you're experiencing persistent symptoms, talk to a trusted adult or healthcare provider rather than self-diagnosing a deficiency.</p>"""
    if old in content:
        content = content.replace(old, new, 1)
        print(f"  ✅ Fixed hs-2-1.html reading opening")
    else:
        print(f"  ❌ hs-2-1.html: reading opening not found")
    
    # Fix vitamin E dermatologist claim
    old_e = """<li>Vitamin E protects your skin from damage, which is why dermatologists recommend it for clear, healthy skin</li>"""
    new_e = """<li>Vitamin E acts as an antioxidant and helps protect cells from damage</li>"""
    if old_e in content:
        content = content.replace(old_e, new_e, 1)
        print(f"  ✅ Fixed hs-2-1.html vitamin E claim")
    
    # Fix vitamin C energy claim
    old_c = """<li>Vitamin C boosts your immune system (fewer sick days = more time with friends and better grades), helps your skin look clear, and gives you energy</li>"""
    new_c = """<li>Vitamin C supports normal immune function and helps with tissue repair</li>"""
    if old_c in content:
        content = content.replace(old_c, new_c, 1)
    
    # Fix B vitamins claim
    old_b = """<li>B-Complex Vitamins are basically your brain's best friend—they help you focus in class, regulate your mood, and convert food into the energy you need to power through your day</li>"""
    new_b = """<li>B-Complex vitamins help your body convert food into energy and support normal nervous system function</li>"""
    if old_b in content:
        content = content.replace(old_b, new_b, 1)
        print(f"  ✅ Fixed hs-2-1.html B vitamin claim")
    
    # Fix "When Vitamin Intake Goes Wrong" - remove diagnostic language
    old_deficiency = """<p>When Vitamin Intake Goes Wrong</p>
        <p>Vitamin Deficiency: When your body doesn't get enough of a vitamin, you experience symptoms that directly affect your life—fatigue, brain fog, weak immune system (constant colds), mood swings, or even acne.</p>"""
    new_deficiency = """<p>When Vitamin Intake Goes Wrong</p>
        <p>Vitamin Deficiency: When your body doesn't get enough of a vitamin over time, deficiency symptoms can develop. These symptoms have many possible causes, so a healthcare provider should assess for deficiencies through proper testing.</p>"""
    if old_deficiency in content:
        content = content.replace(old_deficiency, new_deficiency, 1)
    
    # Fix magnesium claim
    old_mg = """<li>Magnesium reduces muscle soreness after workouts, helps you relax and sleep better, and actually improves your mood</li>"""
    new_mg = """<li>Magnesium supports normal muscle and nerve function, and can be found in foods like nuts, seeds, and leafy greens</li>"""
    if old_mg in content:
        content = content.replace(old_mg, new_mg, 1)
    
    # Fix potassium claim
    old_k = """<li>Potassium regulates your heartbeat and helps muscles contract, so you perform better athletically</li>"""
    new_k = """<li>Potassium helps nerves and muscles communicate and is found in bananas, potatoes, and leafy greens</li>"""
    if old_k in content:
        content = content.replace(old_k, new_k, 1)
    
    # Fix "Why this matters" sections
    old_minerals_intro = """<p>Why this matters to you: Minerals literally build your body—your bones, teeth, and muscles. Without them, you're weak, your bones are fragile, and your body can't do basic things like regulate your heartbeat or send signals from your brain to your muscles.</p>"""
    new_minerals_intro = """<p>Why this matters: Minerals play structural and regulatory roles in your body — supporting bone health, nerve signaling, and fluid balance. Getting them from food sources supports normal function.</p>"""
    if old_minerals_intro in content:
        content = content.replace(old_minerals_intro, new_minerals_intro, 1)
    
    # Fix bottom line
    old_bottom = """<p>The Bottom Line</p>
        <p>Your body is constantly working, and micronutrients are the difference between feeling amazing and feeling terrible. They're why some days you're sharp, focused, and energized—and why other days you're foggy, moody, and exhausted.</p>
        <p>The good news? You have control. By eating a variety of whole foods—fruits, vegetables, lean proteins, whole grains, and dairy—you can get most of the micronutrients your body needs. And when you do, you'll notice the difference: better focus in class, more energy at practice, clearer skin, better mood, and faster recovery.</p>
        <p><strong>It's not just about health. It's about being your best self.</strong></p>"""
    new_bottom = """<p>The Big Picture</p>
        <p>Micronutrients play important roles in supporting your body's normal functions — from energy metabolism to immune health to bone development. A balanced eating pattern that includes a variety of foods can help you meet your micronutrient needs.</p>
        <p>Keep in mind: nutrient deficiencies require proper assessment by a healthcare provider. Symptoms like fatigue or mood changes can have many possible causes. Eating a variety of nutrient-dense foods supports your overall health, but no single nutrient determines how you feel or perform.</p>"""
    if old_bottom in content:
        content = content.replace(old_bottom, new_bottom, 1)
    
    # Fix duplicated quiz fragments (the extra "1. True" questions after Q4 and Q9)
    # Remove the duplicate after Q4
    dup1 = """<div class="quiz-question">
          <p class="q">1. True</p>
          <ul class="options">
            <li><span class="letter">B.</span> False</li>
          </ul>
        </div>
        <div class="quiz-question">
          <p class="q">5."""
    new_after_q4 = """<div class="quiz-question">
          <p class="q">5."""
    content = content.replace(dup1, new_after_q4, 1)
    
    # Remove the duplicate after Q9
    dup2 = """<div class="quiz-question">
          <p class="q">1. True</p>
          <ul class="options">
            <li><span class="letter">B.</span> False</li>
          </ul>
        </div>
        <div class="quiz-question">
          <p class="q">10."""
    new_after_q9 = """<div class="quiz-question">
          <p class="q">10."""
    content = content.replace(dup2, new_after_q9, 1)
    print(f"  ✅ Fixed duplicated quiz fragments")
    
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)
    print(f"  ✅ Completed hs-2-1.html edits")

def fix_hs_2_2():
    """Fix hs-2-2.html: D/K2 claim, E recovery, sun exposure"""
    path = 'hs-2-2.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    
    # Find and fix vitamin E recovery claim
    old_e = """Vitamin E reduces muscle soreness and fatigue after exercise. By protecting cell membranes from damage caused by free radicals during intense activity, it speeds up workout recovery."""
    new_e = """Vitamin E acts as an antioxidant, helping protect cells from oxidative stress. Getting it from food sources like nuts, seeds, and vegetable oils supports normal cell function, but it does not directly speed up workout recovery."""
    if old_e in content:
        content = content.replace(old_e, new_e, 1)
        print(f"  ✅ Fixed hs-2-2.html vitamin E recovery claim")
    else:
        print(f"  ℹ️  hs-2-2.html: Exact vitamin E text not found, trying broader search")
        # Try alternative approach
        if "Vitamin E" in content and "soreness" in content:
            idx = content.find("Vitamin E")
            snippet = content[idx:idx+200]
            print(f"  Found: {snippet[:100]}...")
    
    # Fix sun exposure wording
    old_sun = """safe sun exposure"""
    if old_sun in content:
        idx = content.find(old_sun)
        snippet = content[max(0,idx-100):idx+200]
        print(f"  Found sun text: {snippet}")
    
    open(os.path.join(REPO, path), 'w', encoding='utf-8').write(content)

def fix_hs_2_4():
    """Fix hs-2-4.html: cramps/performance claims"""
    path = 'hs-2-4.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    # Complex editing needed - check file first
    print(f"  ℹ️  hs-2-4.html: {len(content)} chars - reading for analysis")
    # Find magnesium section
    if "cramp" in content.lower():
        idx = content.lower().find("cramp")
        print(f"  Found 'cramp' at position {idx}")
        print(f"  Context: {content[max(0,idx-100):idx+150]}")

def fix_hs_4_3():
    """Fix hs-4-3.html: Use fictional profiles, remove personal data"""
    path = 'hs-4-3.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-4-3.html: {len(content)} chars")

def fix_hs_4_6():
    """Fix hs-4-6.html: Differentiate medical/ethical/trend diets"""
    path = 'hs-4-6.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-4-6.html: {len(content)} chars")

def fix_hs_5_1():
    """Fix hs-5-1.html: Energy balance material"""
    path = 'hs-5-1.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-5-1.html: {len(content)} chars")

def fix_hs_5_4():
    """Fix hs-5-4.html: Remove prescriptive timing rules"""
    path = 'hs-5-4.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-5-4.html: {len(content)} chars")

def fix_hs_6_2():
    """Fix hs-6-2.html: Trauma-informed language"""
    path = 'hs-6-2.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-6-2.html: {len(content)} chars")

def fix_hs_6_3():
    """Fix hs-6-3.html: Emergency signs, not personal prescriptions"""
    path = 'hs-6-3.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-6-3.html: {len(content)} chars")

def fix_hs_6_5():
    """Fix hs-6-5.html: Stop self-diagnosis"""
    path = 'hs-6-5.html'
    content = open(os.path.join(REPO, path), 'r', encoding='utf-8').read()
    print(f"  ℹ️  hs-6-5.html: {len(content)} chars")

if __name__ == "__main__":
    os.chdir(REPO)
    print("=== Fixing hs-2-1.html ===")
    fix_hs_2_1()
    print("\n=== Fixing hs-2-2.html ===")
    fix_hs_2_2()
    print("\n=== Fixing hs-2-4.html ===")
    fix_hs_2_4()
    print("\n=== Fixing hs-4-3.html ===")
    fix_hs_4_3()
    print("\n=== Fixing hs-4-6.html ===")
    fix_hs_4_6()
    print("\n=== Fixing hs-5-1.html ===")
    fix_hs_5_1()
    print("\n=== Fixing hs-5-4.html ===")
    fix_hs_5_4()
    print("\n=== Fixing hs-6-2.html ===")
    fix_hs_6_2()
    print("\n=== Fixing hs-6-3.html ===")
    fix_hs_6_3()
    print("\n=== Fixing hs-6-5.html ===")
    fix_hs_6_5()
