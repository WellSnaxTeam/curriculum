#!/usr/bin/env python3
"""Final soft-launch pass (Oct 2026).

Applies the Final Punch List (37 items), the companion edits from the
cross-check doc, and Devon's four approval tweaks. Every replacement must
match exactly once, so a rerun or a drifted page fails loudly instead of
silently doing nothing.

Record of decisions: "Final Punch List: Cross-Check Against the Live
Curriculum" (Claude Doc), approved by Devon with four tweaks.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
_cache = {}
log = []


def load(f):
    if f not in _cache:
        _cache[f] = open(os.path.join(REPO, f), encoding='utf-8').read()
    return _cache[f]


def rep(f, old, new, item):
    s = load(f)
    n = s.count(old)
    if n != 1:
        sys.exit(f'[{item}] {f}: expected 1 match, found {n}: {old[:80]!r}')
    _cache[f] = s.replace(old, new)
    log.append(f'[{item}] {f}: {old[:70].strip()!r}')


def _qblock(s, num):
    m = re.search(r'(<div class="quiz-question">\s*<p class="q">%d\. .*?</ul>\s*</div>)' % num, s, re.S)
    return m


def quiz(f, num, stem, options, correct, item):
    """Replace quiz question `num` whole. options: list of option texts (A, B, ...)."""
    s = load(f)
    m = _qblock(s, num)
    if not m:
        sys.exit(f'[{item}] {f}: Q{num} not found')
    old = m.group(1)
    empty = ' class=""' if '<li class="">' in old else ''
    lines = []
    for i, text in enumerate(options):
        L = 'ABCDEFG'[i]
        if L == correct:
            lines.append(f'<li class="correct"><span class="letter">{L}.</span> {text} <span class="correct-badge">Correct</span></li>')
        else:
            lines.append(f'<li{empty}><span class="letter">{L}.</span> {text}</li>')
    ind = '            '
    new = ('<div class="quiz-question">\n'
           f'          <p class="q">{num}. {stem}</p>\n'
           '          <ul class="options">\n'
           + ''.join(f'{ind}{l}\n' for l in lines) +
           '          </ul>\n'
           '        </div>')
    _cache[f] = s.replace(old, new)
    log.append(f'[{item}] {f}: Q{num} rewritten (key {correct})')


def q_stem(f, num, old_stem, new_stem, item):
    rep(f, f'<p class="q">{num}. {old_stem}</p>', f'<p class="q">{num}. {new_stem}</p>', item)


def opt(f, num, letter, old_text, new_text, item):
    """Reword one option of question `num`, keeping its correct/incorrect state."""
    s = load(f)
    m = _qblock(s, num)
    if not m:
        sys.exit(f'[{item}] {f}: Q{num} not found')
    blk = m.group(1)
    pat = re.compile(r'(<span class="letter">%s\.</span> )%s( <span class="correct-badge">|</li>)' % (letter, re.escape(old_text)))
    if len(pat.findall(blk)) != 1:
        sys.exit(f'[{item}] {f}: Q{num} option {letter} text not found: {old_text[:60]!r}')
    _cache[f] = s.replace(blk, pat.sub(lambda mm: mm.group(1) + new_text + mm.group(2), blk))
    log.append(f'[{item}] {f}: Q{num} option {letter} reworded')


def between(f, start, end, new, item):
    """Replace from `start` (inclusive) up to `end` (exclusive); both must be unique."""
    s = load(f)
    if s.count(start) != 1 or s.count(end) != 1:
        sys.exit(f'[{item}] {f}: markers not unique: {start[:50]!r} / {end[:50]!r}')
    i, j = s.index(start), s.index(end)
    if j <= i:
        sys.exit(f'[{item}] {f}: end marker before start')
    _cache[f] = s[:i] + new + s[j:]
    log.append(f'[{item}] {f}: replaced block starting {start[:60].strip()!r}')


def save_all():
    for f, s in _cache.items():
        open(os.path.join(REPO, f), 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- middle school

# Item 2: lesson-1-2 food-morality wording
rep('lesson-1-2.html',
    '<li>Dark green vegetables = extra healthy (spinach, broccoli, kale)</li>',
    '<li>Dark green vegetables provide nutrients such as folate, vitamin K and carotenoids (spinach, broccoli, kale)</li>', 2)
rep('lesson-1-2.html',
    '          <li>Lean proteins = healthier (chicken, fish, beans)</li>\n'
    '          <li>High-fat proteins = eat less often (fatty beef, processed meats)</li>\n'
    '          <li>Plant-based proteins = great options (beans, lentils, nuts, tofu)</li>\n',
    '          <li>Protein foods vary in fat type, iron, fiber and other nutrients.</li>\n'
    '          <li>Include a variety of animal and plant sources (chicken, fish, eggs, beef, beans, lentils, nuts, tofu).</li>\n', 2)

# Item 4: lesson-1-2 core activity + optional extension
rep('lesson-1-2.html',
    '<h2><span class="badge badge-activity">Activity</span> Food Group Investigation <span class="module-time">90 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p><strong>There are 5 food group stations to investigate.</strong>',
    '<h2><span class="badge badge-activity">Activity</span> Food Group Sort <span class="module-time">25 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p><strong>Core Activity (25 min):</strong> Your teacher will provide 12 foods or food pictures. Sort each one into its food group. Then compare two Nutrition Facts labels from the same group (for example, two cereals or two yogurts) and note one difference in fiber, added sugar or protein.</p>\n'
    '        </div>\n'
    '        <div class="activity-box">\n'
    '        <p><strong>Optional Extension (up to 90 min): Food Group Investigation.</strong> <strong>There are 5 food group stations to investigate.</strong>', 4)

# Item 3: lesson-1-2 Q10
quiz('lesson-1-2.html', 10, 'Which statement about fruit forms is most accurate?',
     ['Only fresh fruit contains vitamins and fiber',
      'Fresh, frozen and canned fruit can all be nutritious. Compare labels for added sugar or syrup.',
      'Canned fruit has no nutrients left',
      'Frozen fruit always has added sugar'], 'B', 3)

# Item 5: lesson-1-3 flexible plate
rep('lesson-1-3.html',
    '<li>Grains — Choose whole grains most of the time. Examples:',
    '<li>Grains — Whole grains usually provide more fiber than refined grains. Examples:', 5)
rep('lesson-1-3.html',
    '<li>Vegetables — Fill half your plate with vegetables when possible. Examples:',
    '<li>Vegetables — Vegetables provide fiber, vitamins and minerals. Examples:', 5)
rep('lesson-1-3.html',
    '<li>A balanced plate often has vegetables and fruit as the largest share, with protein foods and grains filling out the rest. Dairy or a fortified alternative can be included here or elsewhere in the day. These are starting points, not exact rules, and the right amounts depend on your size, growth and activity.</li>',
    '<li>A balanced meal can include carbohydrate-rich foods, protein-rich foods, fruits and/or vegetables, and other foods that help meet nutrient needs. Exact portions vary with hunger, growth, activity, culture and the rest of the day. There is no single plate shape that is right for every student or every meal. Dairy or a fortified alternative can be included here or elsewhere in the day.</li>', 5)
rep('lesson-1-3.html',
    'steamed broccoli and carrots (vegetables), an apple (fruit), and a cup of whole milk (dairy).</p>\n',
    'steamed broccoli and carrots (vegetables), an apple (fruit), and a cup of whole milk (dairy).</p>\n'
    '        <p><strong>Athletes and highly active students:</strong> On long or hard training days, many athletes need more carbohydrate-rich foods, so grains and starchy foods may take up more of the plate. On lighter days the plate may look more like an everyday meal.</p>\n', 5)
quiz('lesson-1-3.html', 2, 'Which statement about a balanced meal is most accurate?',
     ['Every meal must be half vegetables',
      'A balanced meal usually includes foods from several groups, and portions can change with hunger, activity and culture',
      'Protein should always be the largest portion',
      'A meal is only balanced if it includes dairy'], 'B', 5)
q_stem('lesson-1-3.html', 5, 'Which grain choice is healthiest for including on a balanced plate most often?',
       'Which grain choice usually provides the most fiber?', 5)
q_stem('lesson-1-3.html', 6, 'If a student fills half their plate with vegetables and fruits, which rationale is most accurate?',
       'Why is it useful to include vegetables and fruits in meals?', 5)

# Item 6: lesson-1-5 neutral physiology wording
rep('lesson-1-5.html', '<li>Boosting immune system function</li>', '<li>Supporting normal immune function</li>', 6)
rep('lesson-1-5.html', '<li>Converting food into energy</li>', '<li>Helping the body use energy from food</li>', 6)
rep('lesson-1-5.html', '<li>Vitamin D: Calcium absorption, bone health, mood regulation — ',
    '<li>Vitamin D: Supports calcium absorption and bone health — ', 6)

# Item 7: lesson-1-6 Q5 tests only fiber and added sugar
opt('lesson-1-6.html', 5, 'B', 'Low saturated fat, high fiber, low % Daily Value for sodium',
    'Higher fiber, lower added sugar', 7)

# Item 8: lesson-2-3 no universal target, fictional scenarios
rep('lesson-2-3.html',
    '<p>In the previous lesson, we discussed how it is recommended that 12-14 year olds drink at least 6-8 cups of water each day.</p>',
    '<p>Fluid needs vary with age, body size, food intake, activity, weather, illness and health, so there is no single number that fits every student. Water is generally the everyday default, and food and other drinks also provide fluid. On active days, drink before activity and take regular fluid breaks.</p>', 8)
rep('lesson-2-3.html',
    '<h2><span class="badge badge-activity">Activity</span> Building a Hydration Plan <span class="module-time">45 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p>Create a hydration habits plan to help you set a goal to be more hydrated.</p>\n'
    '        <p><strong>Step 1: Goal Setting</strong> — What\'s your daily water goal?</p>\n'
    '        <p><strong>Step 2: Identify Barriers</strong> — What makes it hard to drink enough water?</p>\n'
    '        <p><strong>Step 3: Choose Your Strategy</strong> — Pick 2-3 strategies that will work for you.</p>\n'
    '        <p><strong>Step 4: Daily Hydration Schedule</strong> — Fill in 6-8 times when you will drink water.</p>\n'
    '        <p><strong>Step 5: Motivation</strong> — Why do YOU want to build this habit?</p>\n'
    '        <p>After filling out the form, write 3-5 sentences on how you will use this plan to consume more water each day.</p>\n',
    '<h2><span class="badge badge-activity">Activity</span> Hydration Plans for Three Students <span class="module-time">25 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p>Read about three students. For each one: (1) name one thing that makes it harder for them to drink enough, (2) pick two strategies that would help, and (3) describe when during the day they could drink and what drink fits.</p>\n'
    '        <p><strong>Maya</strong> has a regular school day. Her water bottle usually stays in her locker.</p>\n'
    '        <p><strong>Jordan</strong> has a 90 minute soccer practice after school on a hot afternoon.</p>\n'
    '        <p><strong>Sam</strong> is home sick with a fever and does not feel like drinking.</p>\n'
    '        <p>Finish by explaining in 2 to 3 sentences why the plans are different for each student.</p>\n'
    '        <p><em>Optional, private, not graded:</em> jot down one hydration idea you might try yourself.</p>\n', 8)
quiz('lesson-2-3.html', 1, 'Which statement about how much fluid a teen needs is most accurate?',
     ['Every teen needs exactly 8 cups a day',
      'Fluid needs vary with body size, activity, weather and health',
      'Teens only need fluid when they exercise',
      'Food never provides any water'], 'B', 8)
quiz('lesson-2-3.html', 8, 'Jordan has a 90 minute soccer practice on a hot afternoon. Which plan makes the most sense?',
     ['Skip drinking so he does not feel full',
      'Drink before practice and take regular fluid breaks during it',
      'Wait until he feels dizzy to drink',
      'Drink only after practice is over'], 'B', 8)
opt('lesson-2-3.html', 9, 'B', 'Plain water is the best and healthiest choice for hydration',
    'Water is a good everyday default for hydration', 8)
# Item 8 companion: lesson-2-7 Q5 (lesson-2-2 ranges already say "general targets" and "needs depend", so no change there)
quiz('lesson-2-7.html', 5, 'Which statement about daily water needs is most accurate?',
     ['Everyone needs exactly 2 to 3 cups',
      'Needs vary with body size, activity, weather and health',
      'Kids should drink as much as possible',
      'Only athletes need to think about water'], 'B', '8 companion')

# Item 9: lesson-2-6 flexible scenario guidance
rep('lesson-2-6.html',
    'Drink water throughout the day — aim for 5–8 cups total, including water from food and other drinks.',
    'Drink water throughout the day, such as at meals and between classes. Food and other drinks also provide fluid.', 9)
rep('lesson-2-6.html',
    '<p><strong>Short Practice / PE Class (under 60 minutes)</strong><br>\n'
    '        Drink water before you start. Take water breaks during activity (every 15–20 minutes, about ½ cup). Drink after you finish. Water is all you need.</p>',
    '<p><strong>Short Practice / PE Class</strong><br>\n'
    '        Drink before activity and take regular water breaks. Drink after you finish. For most PE classes and short practices, water is enough.</p>', 9)
rep('lesson-2-6.html',
    '<p><strong>Long or Hot Practice / Game (60+ minutes in heat)</strong><br>\n'
    '        Pre-hydrate: drink water in the hour before practice. During activity, drink water or a sports drink with electrolytes every 15–20 minutes.',
    '<p><strong>Long, Intense or Hot Practice / Game</strong><br>\n'
    '        Pre-hydrate: drink water in the hour before practice. Take regular fluid breaks. Water is appropriate for many activities. Prolonged, intense, hot or high-sweat activity may call for additional carbohydrate and electrolyte support, such as a sports drink.', 9)
rep('lesson-2-6.html',
    'Try to sip water or an oral rehydration solution often, even if you don\'t feel thirsty. Avoid sugary or caffeinated drinks — they can make dehydration worse. If you can\'t keep fluids down or feel much worse, tell a parent or guardian.',
    'Sip fluids often in small amounts, even if you don\'t feel thirsty. An oral rehydration solution may be appropriate. Tell a parent or guardian, and seek medical guidance if fluids cannot be kept down or you feel much worse.', 9)
opt('lesson-2-6.html', 5, 'B', 'A normal amount of water throughout the day (6-8 cups)', 'Drink water throughout the day as usual', '9 companion')
opt('lesson-2-6.html', 5, 'C', 'Only drink if you feel thirsty', 'Only drink on hot days', '9 companion')
quiz('lesson-2-6.html', 9, 'You have PE class right after lunch. Which drink is a good everyday choice with lunch?',
     ['A large energy drink', 'Nothing at all', 'Water', 'Soda only'], 'C', '9 companion')
opt('lesson-2-6.html', 10, 'B', "Stop every 20-30 minutes to drink water, even if you don't feel thirsty",
    "Take regular water breaks, even if you don't feel thirsty yet", '9 companion')
opt('lesson-2-4.html', 6, 'B', 'Water, or a sports drink after prolonged or intense activity (60+ minutes)',
    'Water, or a sports drink after long, intense or very sweaty activity', '9 companion')

# Item 28 companions in middle school: coconut water and weighing
quiz('lesson-2-5.html', 10, 'Why is coconut water not a direct substitute for a sports drink when the goal is replacing sodium?',
     ['It has much less sodium than a sports drink',
      'It contains no fluid',
      'It has more caffeine than energy drinks',
      'It contains no potassium'], 'A', '28 companion')
opt('lesson-2-7.html', 7, 'C', 'Weighing yourself before and after exercise', 'Noticing whether you feel thirsty', '28 companion')

# Item 10: lesson-3-5 nutrient/function language
rep('lesson-3-5.html',
    '<li>Over time: Frequent high added-sugar intake can contribute to tooth decay and can be a factor in long-term health patterns when it replaces other foods.</li>',
    '<li>Over time: Frequent high added-sugar intake can crowd out more nutrient-dense foods and can contribute to tooth decay.</li>', 10)
rep('lesson-3-5.html',
    'Create a poster showing how various snacks (sugary, salty, and healthy) affect that body system.</p>',
    'Create a poster showing which nutrients from snacks support that body system (for example, calcium for bones, fiber for digestion, protein for muscles). Then show what a pattern high in added sugar or sodium can do to that system over time. Use words like "can" and "over time" rather than promises.</p>', 10)
q_stem('lesson-3-5.html', 1, 'Which of the following is a healthy snack choice?',
       'Which snack provides fiber, protein and unsaturated fat?', 10)
quiz('lesson-3-5.html', 2, 'Which statement about eating a lot of added sugar is most accurate?',
     ['It keeps energy steady all day',
      'Frequent high added sugar intake can crowd out more nutrient-dense foods and affect dental health',
      'It has no effect on the body',
      'It helps build muscle'], 'B', 10)
opt('lesson-3-5.html', 4, 'B', 'They can increase thirst and raise blood pressure',
    'A pattern high in sodium can contribute to higher blood pressure over time in some people', 10)
opt('lesson-3-5.html', 7, 'B', 'They often contain added sugars, sodium, and unhealthy fats',
    'Many are higher in added sugar, sodium or saturated fat, so checking the label helps', 10)
quiz('lesson-3-5.html', 8, 'Regular meals and snacks can be one of many things that support focus at school.',
     ['True', 'False'], 'A', 10)
quiz('lesson-3-5.html', 10, 'Reading nutrition labels can help you compare snacks for fiber, added sugar and sodium.',
     ['True', 'False'], 'A', 10)

# ---------------------------------------------------------------- high school

# Item 1: homepage title + hs-1-7 quiz framing
rep('index.html', '<a href="hs-1-7.html">Counting Macronutrients</a>',
    '<a href="hs-1-7.html">Estimating and Balancing Macronutrient Sources</a>', 1)
rep('hs-1-7.html', 'Counting Macronutrients Quiz <span class="module-time">', 'Lesson 7 Quiz <span class="module-time">', '1 companion')
q_stem('hs-1-7.html', 5, 'Samantha is tracking her macronutrients and notices that her lunch of grilled chicken and broccoli is high in which macronutrient?',
       "Samantha's lunch is grilled chicken and broccoli. Which macronutrient is it highest in?", '1 companion')
q_stem('hs-1-7.html', 10, 'If you are counting macronutrients and your breakfast is oatmeal with berries, which macronutrient is likely to be highest?',
       'Your breakfast is oatmeal with berries. Which macronutrient is likely highest?', '1 companion')
q_stem('hs-1-7.html', 15, 'If you are counting macronutrients and your lunch includes cheese, which macronutrient are you likely increasing?',
       'Your lunch includes cheese. Which macronutrient are you likely adding the most of?', '1 companion')
opt('hs-1-7.html', 15, 'B', 'Protein', 'Fiber', '1 companion')

# Item 11: hs-1-1 activity -> fictional students
rep('hs-1-1.html', 'Activity</span> Macronutrients Reflection <span class="module-time">45 min</span>',
    'Activity</span> Macronutrients in Three Students <span class="module-time">45 min</span>', 11)
between('hs-1-1.html', '<p>Daily Life Reflection</p>', '<p>Part 3: Case Study Analysis</p>',
    '<p>Part 1: Three Students (15 min)</p>\n'
    '        <p><strong>Ava</strong>, 10th grade, does not play a sport. She catches the bus at 6:50, usually skips breakfast, and has lunch at 12:45. After school she snacks on chips.</p>\n'
    '        <p><strong>Marcus</strong>, 11th grade, has football practice from 3:30 to 5:30. He eats a sandwich at 11:00 and nothing else until dinner at 7:00.</p>\n'
    '        <p><strong>Lena</strong>, 9th grade, is in marching band and works weekend shifts. She has cereal for breakfast, pasta at lunch, and fast food between band and work.</p>\n'
    '        <p>Part 2: Analyze (15 min)</p>\n'
    '        <p>For each student: (1) name what carbohydrate, protein and fat are doing for them across the day, (2) find one timing issue, and (3) suggest one practical change that fits their schedule and budget.</p>\n'
    '        ', 11)
rep('hs-1-1.html', '<li>Which athlete will likely perform better in school and sports?</li>',
    '<li>What is the most realistic first change Athlete A could make, and why?</li>', 11)
rep('hs-1-1.html', "<li>How might Athlete A's habits affect energy, focus, recovery, and performance?</li>",
    "<li>How could Athlete A's habits affect energy during practice?</li>", 11)
between('hs-1-1.html', '<p>Part 4: Action Plan for Change</p>', '        </div>\n      </div>\n\n      <!-- QUIZ SECTION -->',
    '<p><em>Optional, private, not graded:</em> note one idea from this lesson you might try.</p>\n', 11)

# Item 12: hs-1-1 Q1 (Derek correction)
opt('hs-1-1.html', 1, 'B',
    'Their carbohydrate intake increased available blood glucose and muscle glycogen for high-intensity activity.',
    'The carbohydrate provided readily available glucose for high-intensity activity.', 12)

# Item 13: hs-1-1 Q6, Q7, Q13, Q14 -> general physiology
quiz('hs-1-1.html', 6, 'A student eats chicken and rice after a resistance-training session. What role does the protein in that meal play?',
     ['It is the main fuel for sprinting.',
      'It supplies amino acids that support muscle repair as part of total daily intake.',
      'It converts to glycogen to refill the muscles.',
      'It increases fiber absorption.'], 'B', 13)
opt('hs-1-1.html', 7, 'A',
    'Simple sugars from the drink provide quick energy, but without other nutrients, energy and focus may not stay steady over time.',
    'The sugar provided quick energy, but several factors could play a role later, such as what else they ate, hydration, sleep and pacing.', 13)
opt('hs-1-1.html', 13, 'A',
    "The candy bar's simple sugars caused a quick blood glucose rise and insulin response, giving short-term energy followed by a rapid drop.",
    'Simple sugars can raise blood glucose quickly, but a candy bar alone may not provide enough fuel for a full interval workout; pacing and earlier meals also matter.', 13)
quiz('hs-1-1.html', 14, 'A student eats very little protein across the day for several weeks while strength training. Which explanation is most likely?',
     ['Low protein intake over time can limit muscle repair and recovery.',
      'Lack of fat prevents glycogen storage.',
      'Low protein increases carbohydrate storage, causing weakness.',
      'Protein only affects flexibility, not strength.'], 'A', 13)

# Item 14: hs-2-4 "Why you need it" -> neutral physiological functions
MINERALS = {
    'Calcium': ['Builds and maintains bones and teeth',
                'Needed for muscle contraction and nerve signaling',
                'Helps blood clot'],
    'Phosphorus': ['Works with calcium to build bones and teeth',
                   'Part of cell membranes, DNA and ATP, the molecule cells use to carry energy'],
    'Sodium': ['Helps maintain fluid balance',
               'Needed for nerve impulses and muscle contraction',
               'Most people in the United States get more than they need. It is lost in sweat, so students who sweat heavily during long or hot activity may need to replace more'],
    'Potassium': ['Works with sodium to maintain fluid balance',
                  'Supports normal heart rhythm, nerve signaling and muscle contraction'],
    'Chloride': ['Helps maintain fluid and pH balance',
                 'Part of stomach acid, which helps digest food',
                 'Helps red blood cells carry carbon dioxide out of the body'],
    'Sulfur': ['Part of some amino acids, so it is found in proteins throughout the body, including muscle, skin and connective tissue',
               'Most people get enough from protein foods'],
    'Iron': ['Part of hemoglobin, which carries oxygen in the blood, and myoglobin, which holds oxygen in muscle',
             'Needed for enzymes that help the body use energy',
             'Supports normal immune function'],
    'Zinc': ['Needed for many enzyme reactions',
             'Supports normal immune function and wound healing',
             'Supports growth and taste'],
    'Iodine': ['Needed to make thyroid hormones, which help regulate metabolism',
               'Supports normal growth and nervous system development'],
    'Fluoride': ['Helps make tooth enamel more resistant to acid and helps prevent cavities',
                 'Also found in bones'],
    'Selenium': ['Needed for normal thyroid hormone function',
                 'Part of enzymes that help protect cells from damage',
                 'Supports normal immune function'],
    'Copper': ['Helps the body use iron and make red blood cells',
               'Needed for enzymes involved in energy production, connective tissue and the nervous system'],
    'Manganese': ['Part of enzymes involved in metabolism and protecting cells from damage',
                  'Helps form bone and cartilage'],
    'Chromium': ['May help insulin work normally',
                 'Involved in how the body processes carbohydrate, fat and protein'],
    'Molybdenum': ['Part of enzymes that break down sulfites and certain amino acids',
                   'Helps the body process some waste products'],
}
_s = load('hs-2-4.html')
for name, bullets in MINERALS.items():
    pat = re.compile(r'(<p>%s</p>.*?<p>Why you need it:</p>\s*<ul>\n)(.*?)(        </ul>)' % name, re.S)
    if len(pat.findall(_s)) < 1 or _s.count('<p>%s</p>' % name) != 1:
        sys.exit(f'[14] hs-2-4.html: mineral block {name} not found uniquely')
    body = ''.join(f'          <li>{b}</li>\n' for b in bullets)
    _s = pat.sub(lambda m: m.group(1) + body + m.group(3), _s, count=1)
    log.append(f'[14] hs-2-4.html: {name} bullets rewritten')
_cache['hs-2-4.html'] = _s

# Item 15: hs-2-4 activity ending + Q5-Q9 test function and sources
rep('hs-2-4.html',
    '<li>reflecting on how you think your energy, focus, or recovery might change</li>',
    '<li>identifying which minerals the meal plan provides well, and one food that could add a mineral it is low in</li>', 15)
rep('hs-2-4.html', '          <li></li>\n          <li></li>\n', '', '15 (empty bullets)')
quiz('hs-2-4.html', 5, 'Which two minerals work together to maintain fluid balance?',
     ['Calcium and phosphorus', 'Iron and zinc', 'Sodium and potassium', 'Iodine and fluoride'], 'C', 15)
quiz('hs-2-4.html', 6, 'Which mineral supports normal muscle and nerve function and is found in nuts, seeds and whole grains?',
     ['Sodium', 'Magnesium', 'Calcium', 'Iron'], 'B', 15)
quiz('hs-2-4.html', 7, 'Which mineral supports normal immune function and wound healing?',
     ['Calcium', 'Zinc', 'Potassium', 'Sodium'], 'B', 15)
quiz('hs-2-4.html', 8, 'Which mineral is needed to make thyroid hormones?',
     ['Magnesium', 'Iodine', 'Iron', 'Calcium'], 'B', 15)
quiz('hs-2-4.html', 9, 'Which mineral helps make tooth enamel more resistant to acid?',
     ['Zinc', 'Sodium', 'Fluoride', 'Iron'], 'C', 15)

# Item 16 (+ Devon tweak 3): hs-2-4 Q14 and Q15
quiz('hs-2-4.html', 14, 'Most people in the United States get more sodium than they need.', ['True', 'False'], 'A', 16)
quiz('hs-2-4.html', 15, 'Fatigue has many possible causes, so it cannot be blamed on one mineral without appropriate evaluation by a healthcare professional.',
     ['True', 'False'], 'A', '16 + Devon tweak 3')

# Item 17: hs-3-1 "Personal consequence" -> objective label interpretation
rep('hs-3-1.html',
    'What you ate — and how much — directly affected your energy, focus, mood, and athletic performance. Learning to read the Nutrition Facts label helps you compare foods and choose options that keep your brain sharp, your mood steady, and your body ready to perform.</p>',
    'How you feel depends on many things, including sleep, stress, hydration and what you ate. Learning to read the Nutrition Facts label helps you compare foods for a stated purpose, such as a filling snack or fuel before practice.</p>', 17)
WHY = [
    'Why it matters when comparing foods: All numbers on the label are for one serving. If you eat two servings, you get twice the calories and nutrients listed.',
    'Why it matters when comparing foods: A package may hold more than one serving. Multiply to see what the whole package provides.',
    'Why it matters when comparing foods: Calories show how much energy a serving provides. Needs vary with age, body size, growth and activity.',
    'Why it matters when comparing foods: Use the 5/20 rule to see quickly whether a serving has a little or a lot of a nutrient.',
    'Why it matters when comparing foods: Replacing saturated fat with unsaturated fat is linked with better heart health over time. The label lists saturated and trans fat so you can compare.',
    'Why it matters when comparing foods: Higher fiber can support fullness and digestive health. The added sugars line shows sugar put in during processing.',
    'Why it matters when comparing foods: Protein supports growth and repair as part of total daily intake. Compare grams per serving when protein is your purpose.',
    'Why it matters when comparing foods: Use %DV to find foods that provide more vitamin D, calcium, iron and potassium.',
    'Why it matters when comparing foods: Use the ingredient list to find allergens, added sugar sources and whole grains.',
]
_s = load('hs-3-1.html')
_hits = re.findall(r'<li>Personal consequence: [^<]*</li>', _s)
if len(_hits) != len(WHY):
    sys.exit(f'[17] hs-3-1.html: expected {len(WHY)} Personal consequence lines, found {len(_hits)}')
for old, new in zip(_hits, WHY):
    _s = _s.replace(old, f'<li>{new}</li>', 1)
_cache['hs-3-1.html'] = _s
log.append('[17] hs-3-1.html: 9 "Personal consequence" lines replaced')
rep('hs-3-1.html', '(example: yogurt with fruit and nuts). This supports sustained focus and steady mood.</li>',
    '(example: yogurt with fruit and nuts).</li>', 17)
rep('hs-3-1.html', 'A small bag may contain 2-3 servings; eating the whole bag could cause sugar spikes and crash your focus.</li>',
    'A small bag may contain 2-3 servings, so multiply the numbers if you eat the whole bag.</li>', 17)
rep('hs-3-1.html', '<li>Scan sugar and fiber: low added sugar + higher fiber = steadier energy.</li>',
    '<li>Scan added sugar and fiber per serving.</li>', 17)
# Item 17 companions: Q3, Q5, Q11 test label reading, not outcomes
quiz('hs-3-1.html', 3, 'A product is labeled "low fat." What else should a student check on the label?',
     ['Nothing, low fat means it is low in everything',
      'Only the product name',
      'The added sugars line, since some lower fat products have more added sugar',
      'Only the color of the packaging'], 'C', '17 companion')
quiz('hs-3-1.html', 5, 'A student is choosing between a candy bar and a granola bar for breakfast before a test. Which label lines are most useful for comparing them?',
     ['Only the calories', 'Added sugars, fiber and protein per serving', 'The brand name', 'The package size only'], 'B', '17 companion')
quiz('hs-3-1.html', 11, 'A student compares the labels on whole-grain bread and white bread. What will the whole-grain label most likely show?',
     ['No carbohydrates', 'More fiber per serving', 'More added sugar', 'Fewer nutrients of every kind'], 'B', '17 companion')

# Item 18: hs-3-1 activity -> fictional label comparison
between('hs-3-1.html', '<h2><span class="badge badge-activity">Activity</span> Energy Timeline <span class="module-time">45 min</span></h2>',
        '        </div>\n      </div>\n\n      <!-- QUIZ SECTION -->',
    '<h2><span class="badge badge-activity">Activity</span> Snack Label Comparison <span class="module-time">25 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p>Your teacher will provide 3 or 4 Nutrition Facts labels. Three students each want a snack for a different purpose:</p>\n'
    '        <ul>\n'
    '          <li><strong>Priya</strong> wants something filling to hold her until a late dinner.</li>\n'
    '          <li><strong>Tyler</strong> needs a light snack about 30 minutes before basketball practice.</li>\n'
    '          <li><strong>Rosa</strong> wants a snack that is lower in sodium.</li>\n'
    '        </ul>\n'
    '        <p>For each student: (1) compare serving size, fiber, added sugar, sodium and protein per serving, (2) choose the label that best fits their purpose, and (3) explain your choice using two numbers from the label. Finish with one sentence on why the best choice was different for each student.</p>\n', 18)

# Item 19: hs-3-2 reading -> objective macro/calorie functions (+ Devon tweak 1 energy-balance line)
between('hs-3-2.html', '<p><strong>How Macronutrients and Calories Power Your Day</strong></p>', '      </div>\n\n      <!-- ACTIVITY SECTION -->',
    '<p><strong>How Macronutrients and Calories Fit Into Your Day</strong></p>\n'
    '        <p>What Calories Are</p>\n'
    '        <p>Calories are units of energy. Your body uses energy for everything, including breathing, thinking, growing and moving. The Nutrition Facts label shows calories per serving, so pair the calorie number with the serving size. Energy needs vary with age, body size, growth and activity.</p>\n'
    '        <p>Carbohydrate, protein and fat all provide calories. Carbohydrate and protein each provide about 4 calories per gram, and fat provides about 9 calories per gram.</p>\n'
    '        <p>Carbohydrates</p>\n'
    '        <p>Carbohydrate is a main fuel for the brain and muscles. Your body breaks carbohydrates down into glucose, a quick source of energy. Complex carbohydrates such as oatmeal, brown rice, whole grains and beans are digested more slowly and also provide fiber.</p>\n'
    '        <p>Protein</p>\n'
    '        <p>Protein supports growth and repair of tissues, including muscle after exercise, as part of total daily intake. Protein also helps you feel full. Sources include chicken, fish, eggs, tofu, Greek yogurt and legumes.</p>\n'
    '        <p>Fats</p>\n'
    '        <p>Fat is a concentrated source of calories. It supports cell structure, helps the body absorb vitamins A, D, E and K, and, along with protein, helps with fullness. Unsaturated fats are found in avocado, nuts, olive oil and fatty fish.</p>\n'
    '        <p>Balancing Macronutrients</p>\n'
    '        <p>Meals that combine carbohydrate, protein and fat can support energy across the day. For example, whole-grain toast, scrambled eggs and sliced avocado provide all three.</p>\n'
    '        <p>Energy Balance</p>\n'
    '        <p>When energy intake is consistently higher than energy needs over time, the body stores some of the extra energy. One meal or one day does not decide this; patterns over time do.</p>\n', 19)
rep('hs-3-2.html', '<li>Your teacher will provide two food labels (or bring in two similar packaged foods).</li>',
    '<li>Your teacher will provide two food labels.</li>', 19)
rep('hs-3-2.html',
    '<p>Brand New Habit:</p>\n        <p>Write one specific habit you will practice next week to improve your energy through balanced food choices.</p>',
    '<p><em>Optional, private, not graded:</em> write one idea you might try.</p>', 19)
q_stem('hs-3-2.html', 5, 'A student is tracking their calorie intake. Which macronutrients contribute to their total calories?',
       'A student reads a Nutrition Facts label. Which macronutrients contribute to the total calories?', 19)
# Item 20 (optional softening): hs-3-2 Q10
quiz('hs-3-2.html', 10, 'True or False: Balanced meals can support energy across the day.', ['True', 'False'], 'A', 20)
# Devon tweak 1: hs-3-2 Q12
opt('hs-3-2.html', 12, 'C', 'The student is likely consuming more calories than needed, which can lead to weight gain.',
    'When energy intake consistently exceeds energy needs over time, the body may store some of that energy.', 'Devon tweak 1')

# Item 21: hs-3-4 reading -> what ingredient lists actually tell students
rep('hs-3-4.html',
    "That choice can change how you feel in the next hour - sharper, slower, or crash-and-burn. Small snack choices add up and directly affect your energy, focus, mood, and how well you perform on the field or in the classroom.</p>",
    "The ingredient list tells you what a food is made of, which helps you compare options for your purpose.</p>", 21)
rep('hs-3-4.html',
    "If sugar or corn syrup is listed first or second, that snack will likely give you a quick energy spike followed by a crash - which hurts concentration and athletic endurance. When whole foods like oats, nuts, or fruit are listed first, the snack delivers more stable energy and better focus throughout practice or study.</p>",
    "If sugar or a syrup is listed first or second, sugar makes up a large share of the product by weight. If whole foods like oats, nuts or fruit are listed first, they make up most of the product.</p>", 21)
rep('hs-3-4.html',
    "These ingredients release energy slowly, helping you sustain attention during long classes and maintain steady athletic performance. Whole foods also support clearer skin and better mood because they provide vitamins and minerals your body needs.</p>",
    "Whole foods often provide fiber, vitamins and minerals.</p>", 21)
rep('hs-3-4.html',
    "give fast but brief energy. That burst often causes irritability and difficulty concentrating afterward. Snacks with limited added sugars keep blood sugar steadier, which supports better focus for tests and less fatigue during workouts.</p>",
    "are sugars put in during processing. Keeping added sugar moderate leaves more room for foods that provide fiber, vitamins and minerals.</p>", 21)
rep('hs-3-4.html',
    '          <li>Read from top to bottom: the first three ingredients matter most for steady energy and focus.</li>\n'
    '          <li>Prefer snacks with whole foods listed first to support sustained concentration and athletic output.</li>\n'
    '          <li>If sugar appears among the top two ingredients, expect a quick energy spike and likely crash - bad for tests or games.</li>\n'
    '          <li>Avoid "partially hydrogenated" on labels to protect long-term stamina and general health.</li>\n'
    '          <li>When in doubt, choose fresh fruit, plain yogurt with nuts, or whole-grain toast with peanut butter for reliable energy and better mood.</li>\n',
    '          <li>Read from top to bottom: because ingredients are listed by weight, the first few make up most of the product.</li>\n'
    '          <li>Use the ingredient list to check for allergens, added sugar sources, whole grains and the type of oil (for example, olive or avocado oil).</li>\n'
    '          <li>Use the ingredient list together with the Nutrition Facts panel; neither tells the whole story alone.</li>\n', 21)
rep('hs-3-4.html',
    "<p>Every snack is a small decision that shapes how you think, move, and look all day. Learning to read ingredient lists helps you choose foods that keep your energy steady, sharpen your focus, improve athletic performance, and support a healthy appearance. Next time you reach into your bag, take a few seconds to read - your body and mind will thank you.</p>",
    "<p>Reading ingredient lists takes a few seconds and helps you compare foods for allergens, added sugars, whole grains and oils.</p>", 21)
# Item 21 companion + QA rule (no personal food logs): activity uses teacher-provided products
rep('hs-3-4.html', '<p>Objective: Examine personal eating habits through ingredient lists.</p>',
    '<p>Objective: Practice reading ingredient lists using products your teacher provides.</p>', '21 companion')
rep('hs-3-4.html', '<li>Make a list of 10 foods you eat most often.</li>',
    '<li>Your teacher will provide 10 food products or ingredient lists.</li>', '21 companion')
rep('hs-3-4.html', '<p>5. - Do most of the foods you eat have whole-food ingredients, some processed ingredients, or highly processed ingredients?</p>',
    '<p>5. - Do most of the products have whole-food ingredients, some processed ingredients, or highly processed ingredients?</p>', '21 companion')
rep('hs-3-4.html', '          <li>- Do you choose foods high in added sugars?</li>\n          <li>- Do you choose foods high in calories and trans fats?</li>\n',
    '          <li>- Which products list an added sugar among the first few ingredients?</li>\n          <li>- Which products list a whole grain first?</li>\n', '21 companion')
rep('hs-3-4.html', '<p>8. Calculate how many of your foods have added sugars listed within the first five ingredients.</p>',
    '<p>8. Count how many of the products have added sugars listed among the first few ingredients.</p>', '21 companion')
rep('hs-3-4.html', '          <li>Which foods keep you energized?</li>\n          <li>Which foods leave you tired or hungry soon afterward?</li>\n',
    '          <li>Which product would you choose for a filling snack, and which ingredients support that choice?</li>\n', '21 companion')
rep('hs-3-4.html',
    '<p>Healthy Habit Commitment</p>\n        <p>Create a simple goal to make one healthy change this week to form a new habit. Building good habits with small changes at a time can lead to a healthier lifestyle.</p>\n        <p>Example: "I will replace one highly processed snack with a whole-food option this week."</p>',
    '<p><em>Optional, private, not graded:</em> note one thing you might check on an ingredient list next time you choose a snack.</p>', '21 companion')

# Item 22: hs-3-4 Q9
quiz('hs-3-4.html', 9, 'Which is the best use of an ingredient list?',
     ['Choosing the product with the longest list',
      'Checking for allergens and seeing which ingredients are present in the greatest amounts',
      'Avoiding any ingredient you cannot pronounce',
      'Picking the most colorful packaging'], 'B', 22)

# Item 23 (+ Devon tweak 2): hs-4-1 food groups -> functions and patterns
rep('hs-4-1.html',
    "<p>These are packed with vitamins, minerals, and fiber. What they do for you: They stabilize your energy so you don't crash mid-afternoon, keep your skin clear and glowing, and help your brain stay sharp during long study sessions. The fiber also keeps your digestion running smoothly so you feel lighter and more comfortable.</p>",
    "<p>Fruits and vegetables provide fiber, vitamins such as A and C, minerals such as potassium, and water. Fiber supports normal digestion.</p>", 23)
rep('hs-4-1.html',
    "<p>Real talk: Aim for variety-different colors mean different nutrients. A colorful plate isn't just Instagram-worthy; it's actually better for you.</p>",
    "<p>Real talk: Eating a variety of colors helps cover a wider range of nutrients.</p>", 23)
rep('hs-4-1.html',
    "<p>Whole grains like oatmeal, brown rice, and whole wheat bread contain fiber and B vitamins. What they do for you: They provide sustained energy so you don't hit the wall during practice or a big game. They also improve focus and concentration-crucial when you're cramming for finals or trying to stay alert in class.</p>",
    "<p>Grains provide carbohydrate, a main fuel for the brain and muscles. Whole grains like oatmeal, brown rice and whole wheat bread keep the bran and germ, so they usually have more fiber, B vitamins and minerals than refined grains.</p>", 23)
rep('hs-4-1.html',
    "<p>Real talk: At least half your grains should be whole grains. Refined grains (white bread, sugary cereals) spike your blood sugar, then crash it, leaving you tired and unfocused.</p>",
    "<p>Real talk: Dietary guidelines suggest making at least half your grains whole grains. Many refined grains are enriched with iron and B vitamins, and both can fit in a varied diet.</p>", 23)
rep('hs-4-1.html',
    "<p>Found in meat, fish, eggs, beans, nuts, and dairy. What they do for you: Protein builds and repairs muscle, so if you're athletic or working out, this is non-negotiable. It also keeps you feeling full longer, stabilizes your mood, and supports clear skin. Plus, it helps your body recover after exercise.</p>",
    "<p>Found in meat, poultry, fish, eggs, beans, lentils, tofu, nuts and seeds, and dairy. Protein foods provide amino acids for growth and repair, plus nutrients such as iron and zinc. Protein also helps you feel full.</p>", 23)
rep('hs-4-1.html',
    "<p>Real talk: You need it at every meal, not just dinner. A protein-heavy breakfast will keep you satisfied through the second period.</p>",
    "<p>Real talk: Spreading protein across meals and snacks is one practical way to meet daily needs.</p>", 23)
rep('hs-4-1.html', '<li>Dairy (Or Dairy Alternatives)</li>', '<li>Dairy Foods and Fortified Alternatives</li>', 'Devon tweak 2')
rep('hs-4-1.html',
    "<p>Milk, yogurt, and cheese are rich in calcium and vitamin D. What they do for you: Strong bones now mean fewer fractures and better athletic performance. Calcium also supports muscle function and helps regulate mood. Vitamin D boosts your immune system so you don't get sick as often.</p>",
    "<p>Milk, yogurt, cheese and fortified alternatives can provide calcium, vitamin D, protein and potassium, which support bone growth during the teen years.</p>", 23)
rep('hs-4-1.html',
    "<p>Real talk: If you're lactose intolerant or vegan, fortified plant-based alternatives (soy, almond, oat milk) work too.</p>",
    "<p>Real talk: If you're lactose intolerant or vegan, fortified plant-based alternatives can be an option. Check the label, since not every alternative provides the same calcium, vitamin D and protein.</p>", 'Devon tweak 2')
rep('hs-4-1.html',
    "<p>Found in olive oil, nuts, avocados, and fatty fish. What they do for you: Healthy fats are essential for brain function-they literally help your brain work better, which means better grades and sharper focus. They also support hormone balance, which affects your mood and energy. And they help your body absorb vitamins from other foods.</p>",
    "<p>Found in olive oil, nuts, seeds, avocados and fatty fish. Unsaturated fats support cell structure and help the body absorb vitamins A, D, E and K.</p>", 23)
rep('hs-4-1.html',
    "<p>Real talk: Not all fats are equal. Olive oil and avocado are your friends; trans fats and excess saturated fats are not.</p>",
    "<p>Real talk: Replacing saturated fat with unsaturated fat is linked with better heart health over time.</p>", 23)
# Same page, same claim types (Key Guidelines + closing); sodium line kept as agreed
rep('hs-4-1.html', 'Eating too much of anything-even good stuff-can leave you feeling sluggish and affect how you look and feel.</li>',
    'Portion needs vary with hunger, growth and activity.</li>', 23)
rep('hs-4-1.html', '<li>Hydration is non-negotiable. Water affects everything: your energy, focus, skin clarity, and athletic performance. Dehydration makes you tired, moody, and unfocused. Drink water, not just sugary drinks.</li>',
    '<li>Hydration matters. Water supports temperature regulation and physical function, and dehydration can contribute to fatigue. Water is generally the everyday default.</li>', 23)
rep('hs-4-1.html', '<li>Limit added sugars and sodium. Too much sugar causes energy crashes, mood swings, and affects your skin. Sodium',
    '<li>Limit added sugars and sodium. Keeping added sugar moderate leaves more room for foods that provide fiber, vitamins and minerals. Sodium', 23)
rep('hs-4-1.html', "<li>Don't skip meals. Skipping breakfast or lunch tanks your energy and focus. Eating regular meals keeps your blood sugar stable and your mood steady.</li>",
    "<li>Eat regular meals. Regular meals and snacks help spread energy and nutrients across the day.</li>", 23)
rep('hs-4-1.html', "shape your energy levels, your athletic potential, your skin, your focus, and even your mood. You don't have to be perfect, but you do have to be intentional. Understanding dietary guidelines gives you the power to feel your best, perform your best, and look your best. That's not vanity-that's self-care.</p>",
    "are one part of your overall health, along with sleep, activity and stress. You don't have to be perfect. Understanding dietary guidelines helps you make informed choices that fit your culture, budget and needs.</p>", 23)

# Item 24: hs-4-4 quiz -> variety and tradeoff reasoning
quiz('hs-4-4.html', 2, 'A student prepares a meal with lean beef, whole wheat bread, and carrots but leaves out any sources of fat. Which addition would bring in a source of unsaturated fat?',
     ['Avocado slices', 'More carrots', 'A second slice of bread', 'Extra beef'], 'A', 24)
quiz('hs-4-4.html', 3, 'A student eats a lunch that includes whole grains, lean protein, vegetables, and a small amount of unsaturated fat. Which statement is most accurate?',
     ['It includes several food groups, which supports a varied intake.', 'It is missing every food group.',
      'It contains only protein.', 'It has no carbohydrate.'], 'A', 24)
quiz('hs-4-4.html', 5, 'A student wants a drink with lunch that has no added sugar. Which choice fits?',
     ['Water', 'Soda', 'Sweet tea', 'An energy drink'], 'A', 24)
quiz('hs-4-4.html', 7, 'A student is packing lunch on a tight budget. Which swap keeps the meal varied while lowering the cost?',
     ['Removing every vegetable', 'Using canned beans as the protein instead of deli meat',
      'Packing only chips', 'Skipping lunch'], 'B', 24)
quiz('hs-4-4.html', 8, 'A student eats eggs, whole grain toast, and fruit for breakfast. Which food groups does this breakfast include?',
     ['Only dairy', 'Protein, grains and fruit', 'Only grains', 'Vegetables and dairy'], 'B', 24)
quiz('hs-4-4.html', 9, 'A student adds spinach and tomatoes to her sandwich at lunch. What does this change add to the meal?',
     ['More protein only', 'More added sugar', 'A dairy food', 'Vegetables, which add fiber, vitamins and minerals'], 'D', 24)
quiz('hs-4-4.html', 12, 'True or False: A lunch of only desserts includes foods from several food groups.',
     ['True', 'False'], 'B', 24)

# Item 25: hs-4-6 condition first, then the strategy
quiz('hs-4-6.html', 2, 'A student with diabetes has been taught carbohydrate counting by their care team. Why might they do this?',
     ['To avoid dairy', 'To help manage their blood sugar levels', 'To build muscle mass', 'To prepare for a competition'], 'B', 25)
quiz('hs-4-6.html', 6, 'A student with kidney disease follows a meal plan from their care team that limits protein. Why might this be part of their plan?',
     ['To follow a ketogenic diet', 'Kidneys affected by disease may have a harder time handling waste products from protein',
      'To gain weight', 'To avoid sugar'], 'B', 25)
quiz('hs-4-6.html', 15, 'A student with celiac disease needs to avoid gluten. Which food would they need to check most carefully?',
     ['Plain rice', 'Fresh fruit', 'Wheat bread', 'Plain grilled chicken'], 'C', '25 (key D -> C)')

# Item 26: hs-5-4 pre-activity wording
rep('hs-5-4.html',
    "When you have adequate carbs before exercise, you'll have better endurance, faster reaction time, and improved athletic performance. Without them, you'll feel weak and fatigued.</p>",
    "Carbohydrate availability can support higher intensity activity.</p>", 26)
rep('hs-5-4.html',
    "<p>Protein helps preserve muscle and provides sustained energy. Including some protein in your pre-activity meal prevents muscle breakdown during exercise and helps you feel fuller longer. This means better performance during your workout and less hunger-related mood swings.</p>",
    "<p>Some protein may fit in a meal before activity when there is enough time to digest it. Protein also helps you feel fuller longer.</p>", 26)
rep('hs-5-4.html', '          <li>Nuts and nut butters</li>\n          <li>Protein powder</li>\n',
    '          <li>Nuts and nut butters</li>\n', 26)

# Item 27: hs-5-4 during activity -> no numeric protocol, needs vary
# (keeps the "Choose easily digestible carbs" list and the "Avoid high-fiber..." line that Q8 depends on)
between('hs-5-4.html', '<p>Why Mid-Activity Nutrition Matters</p>', '<p>Choose easily digestible carbs:',
    '<p>Why Mid-Activity Nutrition Matters</p>\n'
    '        <p>For most practices and PE classes, water is enough. For longer, intense, hot or high sweat sessions, such as extended practices, tournaments, long-distance running or back-to-back games, some athletes benefit from carbohydrate, fluid and sodium during activity.</p>\n'
    '        <p>Amounts vary by sport, conditions, body size, sweat rate and tolerance. Individual plans belong with an athletic trainer, registered dietitian or other qualified staff.</p>\n'
    '        <p>Hydration During Activity</p>\n'
    '        <p>Take regular fluid breaks. When fluid and sodium replacement is the goal, examples include sports drinks designed for sweat replacement. Coconut water provides fluid and potassium but is usually lower in sodium than these drinks.</p>\n'
    '        ', '27 + 28')

# Item 28: hs-5-4 post-activity rehydration without body-weight calculations
rep('hs-5-4.html',
    "<p>Drink 16-24 ounces of fluid for every pound of body weight lost during activity. You can estimate this: if you weighed yourself before and after exercise, the difference is your fluid loss. This matters because proper rehydration affects your mood, energy levels, cognitive function, and how quickly you recover for your next workout.</p>",
    "<p>Rehydrate after activity based on thirst, how much you sweated and the weather. Some athletic programs use sweat rate testing to estimate fluid loss. If used, it should be supervised by qualified staff.</p>", 28)
rep('hs-5-4.html',
    "Sports drinks, coconut water, or even chocolate milk work well. The sodium helps your body retain fluid, and the carbs begin the recovery process immediately.</p>",
    "Water with a meal or snack, milk or chocolate milk, or a sports drink can all help with rehydration after activity. Sodium helps your body retain fluid.</p>", 28)

# Same page, same claim types (scenarios still used the 60 minute rule; closing promised appearance changes)
_s = load('hs-5-4.html')
if _s.count('During (if over 60 min)') != 2 or _s.count('During events (if over 60 min)') != 1:
    sys.exit('[27] hs-5-4.html: scenario 60 min lines not as expected')
_cache['hs-5-4.html'] = _s.replace('During (if over 60 min)', 'During (if long, intense or hot)').replace('During events (if over 60 min)', 'During events (if long, intense or hot)')
log.append('[27] hs-5-4.html: 3 scenario lines no longer use the 60 minute rule')
rep('hs-5-4.html', "you can dramatically change how you feel and perform.", "you can better support how you feel during activity.", 27)
rep('hs-5-4.html', "This completes your recovery and ensures you're fully refueled for your next activity. You'll notice improved performance in your next workout, better mood, clearer focus, and faster muscle recovery.</p>",
    "This helps you refuel for your next activity.</p>", 27)
rep('hs-5-4.html',
    "When you fuel strategically—with the right foods at the right times—you'll perform better athletically, think more clearly, feel more energized, maintain a better mood, and even look better as your body composition improves and your skin clears. These aren't complicated changes. They're simple, intentional choices that compound over time. Start with one or two strategies from this guide, notice how you feel, and build from there. Your future self—and your performance—will thank you.</p>",
    "Fueling before, during and after activity can support energy and recovery. These aren't complicated changes. Start with one or two strategies from this guide, and talk with an athletic trainer or registered dietitian for an individual plan.</p>", 27)
# Item 26/27 companions: soften guaranteed-outcome keys
opt('hs-5-4.html', 2, 'A', 'Her blood glucose and sodium levels are better maintained, slowing fatigue and reducing cramp risk',
    'The carbohydrate, fluid and sodium can help maintain blood glucose and fluid balance during long, hot activity', '27 companion')
opt('hs-5-4.html', 12, 'C', 'She will improve recovery and training consistency through better glycogen replenishment and repair',
    'Over time, this can support recovery and training consistency by helping replenish glycogen and repair muscle', '27 companion')

END_ACTIVITY = '        </div>\n      </div>\n\n      <!-- QUIZ SECTION -->'

# Item 29: hs-6-1 activity -> fictional athletes, optional private goal
between('hs-6-1.html', '<h2><span class="badge badge-activity">Activity</span> Recovery Habits Scorecard', END_ACTIVITY,
    '<h2><span class="badge badge-activity">Activity</span> Recovery Case Studies <span class="module-time">30 min</span></h2>\n'
    '        <div class="activity-box">\n'
    '        <p>Read about three fictional athletes. For each one: (1) describe their protein and overall energy pattern across the day, (2) identify the most useful change they could make, and (3) explain why.</p>\n'
    '        <ul>\n'
    '          <li><strong>Jordan</strong>, wrestling: eats a large dinner with chicken and rice, but has only a sports drink for breakfast and often skips lunch.</li>\n'
    '          <li><strong>Maya</strong>, soccer: eats three meals with some protein in each, but rarely eats anything between an after-school practice and a late dinner.</li>\n'
    '          <li><strong>Chris</strong>, track: eats cereal for breakfast, a sandwich at lunch and pasta at dinner, with little protein beyond the sandwich.</li>\n'
    '        </ul>\n'
    '        <p>Finish by explaining why total protein and energy across the day matter for recovery.</p>\n'
    '        <p><em>Optional, private, not graded:</em> note one recovery idea from this lesson you might try.</p>\n', 29)

# Item 30: hs-6-1 Q10 (Derek-reviewed item, reworded toward repair)
quiz('hs-6-1.html', 10, 'True or False: Adequate protein supports muscle repair and recovery after exercise.', ['True', 'False'], 'A', 30)

# Item 31 (+ companion): hs-6-2 Part 1 optional/private, real duration, Part 2 fictional logs
rep('hs-6-2.html', 'Activity</span> Fuel and Energy Patterns <span class="module-time">0 min</span>',
    'Activity</span> Fuel and Energy Patterns <span class="module-time">35 min</span>', '31 companion / 37')
rep('hs-6-2.html', '<p>You will connect nutrition to athletic performance.</p>',
    '<p>Part 1 (<em>Optional, private, not graded</em>): connect habits to how you feel. You do not need to share or turn in this part.</p>', '31 companion')
between('hs-6-2.html', '<p>Part 2: My Energy Pattern</p>', END_ACTIVITY,
    '<p>Part 2: Three Training Day Logs (20 min)</p>\n'
    '        <ul>\n'
    '          <li><strong>Jada</strong>, cross country: skips breakfast, has a light salad at lunch, runs 6 miles at 3:30 and eats dinner at 8:00. She says she feels drained by mile 4 and has felt dizzy after practice twice this week.</li>\n'
    '          <li><strong>Ben</strong>, swimming: practices at 5:30 a.m. and again after school. He eats lunch but often skips breakfast and the after-school snack. He says his last class is hard to focus in and he feels slow to recover.</li>\n'
    '          <li><strong>Sofia</strong>, soccer: eats breakfast and lunch, has a granola bar and water before practice, and eats dinner after. She says her energy feels normal, with one sore day after a weekend tournament.</li>\n'
    '        </ul>\n'
    '        <p>For each athlete: (1) Could their pattern be consistent with underfueling? (2) What else could explain how they feel, such as sleep, stress or illness? (3) What general support could help, such as regular meals and a snack before practice? (4) Who could they talk to? Do not diagnose.</p>\n', 31)

# Item 32: hs-6-2 quiz -> "may be consistent with", qualified referral
opt('hs-6-2.html', 3, 'A', 'They might experience decreased concentration and mood swings.',
    'Under-eating over time may contribute to low energy and difficulty concentrating.', 32)
opt('hs-6-2.html', 4, 'D', 'They may be experiencing symptoms of energy deficiency.',
    'These symptoms may be consistent with energy deficiency, but they have many possible causes and should be checked by a qualified professional.', 32)
quiz('hs-6-2.html', 5, 'A student is concerned they may be underfueling. What is the best next step?',
     ['Talk with a parent or guardian, athletic trainer, registered dietitian, or healthcare professional, and make sure regular meals and snacks are available.',
      'Skip meals to lose weight.',
      'Decrease water intake.',
      'Avoid carbohydrates.'], 'A', 32)
opt('hs-6-2.html', 10, 'B', 'They should talk to a coach or nutritionist about their eating habits.',
    'They should talk with a parent or guardian, athletic trainer, registered dietitian, or healthcare professional.', 32)

# Item 33: hs-6-3 opening -> no appearance or guaranteed mood/focus claims
rep('hs-6-3.html',
    "how much and what you drink can directly impact your energy, mood, focus, and even your appearance. Hydration isn't just about quenching thirst; it's about fueling your body to perform at its best.</p>",
    "hydration supports normal circulation, temperature regulation and physical function. Significant dehydration can contribute to fatigue, dizziness and reduced exercise performance.</p>", 33)
rep('hs-6-3.html', " You might even notice your skin looking dull or dry, since water helps keep your body and appearance healthy.</p>", "</p>", 33)
rep('hs-6-3.html',
    "<p>Proper hydration isn't just about avoiding negative consequences-it's about maximizing your potential. When you're hydrated, you'll notice better focus in school, more energy during workouts, and faster recovery after games. Your skin will look healthier, and your mood will be more stable. Hydration is a simple habit that can give you a real edge, both on and off the field.</p>",
    "<p>Staying hydrated is one of several things, along with sleep, fueling and training, that support how you feel and perform at school and in sports.</p>", 33)

# Item 34 (+ companion): hs-6-3 Part 1 optional/private, Part 2 scenarios, no 1-week commitment
rep('hs-6-3.html', '<p>Think about your most recent practice, workout, or PE class.</p>',
    '<p>Part 1 (<em>Optional, private, not graded</em>): think about your most recent practice, workout, or PE class. You do not need to share or turn in this part.</p>', '34 companion')
between('hs-6-3.html', '<p>Part 2: Build A Personal Hydration Plan</p>', END_ACTIVITY,
    '<p>Part 2: Hydration Plans for Five Scenarios (20 min)</p>\n'
    '        <p>Build a simple plan (before, during and after) for each:</p>\n'
    '        <ul>\n'
    '          <li>A normal school day</li>\n'
    '          <li>A 45 minute PE class</li>\n'
    '          <li>A 2 hour football practice on a hot August afternoon</li>\n'
    '          <li>An all-day volleyball tournament in a gym</li>\n'
    '          <li>A week of outdoor marching band camp in summer</li>\n'
    '        </ul>\n'
    '        <p>For each, explain when water is likely enough and when additional carbohydrate or sodium may help. Name one sign of dehydration and one sign of overhydration to watch for.</p>\n', 34)

# ---------------------------------------------------------------- Devon tweak 4: hs-5-5 and hs-6-4 quiz softening
T4 = 'Devon tweak 4'
opt('hs-5-5.html', 1, 'C', 'Jordan is showing signs of low blood glucose from skipping breakfast.',
    'Skipping breakfast may have left Jordan with low blood glucose, which can contribute to shakiness and trouble concentrating.', T4)
opt('hs-5-5.html', 2, 'A', 'The balanced meal provided sustained energy and nutrients for mental focus.',
    'The balanced meal can support steady energy, which is one of several things that support focus.', T4)
opt('hs-5-5.html', 3, 'D', 'Eating mostly refined carbohydrates and fat delayed muscle recovery and did not replenish fluids or protein.',
    'A snack of mostly refined carbohydrate and fat did not replace fluids or provide much protein to support recovery.', T4)
opt('hs-5-5.html', 4, 'C', 'Repeated sugar spikes and drops are causing energy crashes and headaches.',
    'A pattern high in added sugar and low in protein and fiber may contribute to energy dips; headaches have many possible causes.', T4)
opt('hs-5-5.html', 5, 'A', "The snack's combination of protein and fiber is helping stabilize blood sugar and mood.",
    "The snack's protein and fiber can help with fullness and steadier energy between meals.", T4)
opt('hs-5-5.html', 6, 'B', 'Sleep deprivation combined with missed meals impairs cognitive function and decision-making.',
    'Sleep loss combined with missed meals can make it harder to concentrate and make decisions.', T4)
opt('hs-5-5.html', 7, 'D', 'Switching to water plus protein/fat from nuts reduced a rapid sugar spike and steadied energy.',
    'Switching from soda to water and nuts cut added sugar, and the protein and fat in nuts can support steadier energy.', T4)
opt('hs-5-5.html', 9, 'A', 'Proper hydration and nutrient-dense meals support brain function and stress management.',
    'Hydration and regular, nutrient-dense meals can support brain function and help with managing stress.', T4)
opt('hs-5-5.html', 11, 'A', 'Fiber and protein slow digestion and promote steadier blood glucose and energy.',
    'Fiber and protein slow digestion, which can support steadier blood glucose and energy.', T4)
opt('hs-5-5.html', 13, 'B', 'Skipping snacks leads to greater hunger later, promoting larger meals and possible overeating.',
    'Skipping snacks can lead to greater hunger later, which may lead to larger meals.', T4)
opt('hs-6-4.html', 5, 'C', 'Their brain is receiving less glucose for focus and mood regulation',
    'Their brain may be getting less glucose, which can affect focus and mood', T4)
opt('hs-6-4.html', 12, 'A', 'Their brain is low on glucose needed for focus and cognitive function',
    'Their brain may be low on glucose, which can make it harder to focus', T4)


if __name__ == '__main__':
    save_all()
    print('\n'.join(log))
    print(f'\n{len(log)} edits across {len(_cache)} files')
