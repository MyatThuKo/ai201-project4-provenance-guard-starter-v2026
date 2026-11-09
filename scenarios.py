"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Criterion 1 counts how many of these get "ai". Criterion 2 reuses
        # the same 10 as its human side.
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "I am a computer science graduate, currently working as an iOS engineer at a FinTech Company. I am currently taking a course on AI Engineering from CodePath. I like to play video games such as EAFC27 and League of Legends during my free time. Currently, I am reading AI Engineering by Chip Huyen to learn more about the AI engineering and its applications.",
            "Apple Magic Keyboard is a wireless keyboard that allows a user to connect to their iPad Pro (12.9-inch and 11-inch) and the new iPad Air (4th generation), which was announced on September 15, 2020. The Magic Keyboard has the same physical appearance as a notebook when it is closed or folded, and it is slightly bigger than an iPad in size. It is a two-sided item where on one side, a user will see a keyboard and a built-in trackpad while on the other side, the user will see a leather-coating layer with three tiny circular magnets. The Magic Keyboard will make the user’s life easier when it comes to typing office or school documents, and having a portable, and light device. Using the Magic Keyboard with an iPad will surely reduce the problem of a user not being able to reach certain keys while they are holding the iPad to type on its widescreen. The main parts of this keyboard are its keys with a built-in trackpad, the structure, and the built-in magnets for the connectivity with the iPad.",
            "A lot of New Yorkers love to go shopping at the Whole Foods Market. The one located at the Columbus Circle is said to be the largest supermarket located in New York City and is a flagship store. This large supermarket spreads over a huge acre of spaces with a wide variety of items in it, but this is somewhat a problem for a customer who wants to go in and out of the store. People often find difficulties in searching for the location that the one item they need.",
            "With advanced technologies, people are now starting to use contactless payments such as Apple Pay, Google Pay, and Samsung Pay. Only a few percentages of the world are currently using it and some of the third-world countries are still using paper money. Contactless payment is widely popular and used in developed countries such as the United States of America, and some countries in Europe. By reducing the use of paper money, we will be able to lessen the migration of paper money from one hand to another. The use of contactless payments has a huge advantage over card payments and paper money payments when it comes to having human interactions and contacts.",
            "The use of digital wallets or mobile wallets starts in 2011 where Google and Android announced Google Pay and Android Pay accordingly. Not so long after the two tech giants started their way into digital wallets, Apple initialized their way to it in 2014. Since the start of the digital wallets, it has been growing exponentially and the global usage of the smart card is expected to exceed $65 billion by 2025 (Rolfe, Alex). Not all retail stores accept digital wallets or contactless payments yet. A few other local small businesses such as 99 Cents stores in New York, still use the paper money method. We can encourage the local small business to accept digital payment and encourage the payment system to be more accessible to those local small businesses. Everyone including both the customers and the merchants should take advantage of contactless payments.",
            "In order to have a more streamlined and user-friendly customer experience inside the store, we would like to build our own application featuring three main innovations: a shopping list, an updated inventory report, and an interactive in-store map to navigate and locate goods. The features of the application lend themselves to integration within any sector of the retail marketplace.",
            "This feature functions much like the shopping list from the legacy Whole Foods application, with the added integration mentioned with the Store Map feature. In addition to reducing the necessity for pen and paper to make shopping lists, this list can be accessed by anyone on the user’s account to amend the list in real-time. We envision this feature to streamline shopping trips that have multiple family members “dividing and conquering” the list, or for a member who may still be at work or school to contribute to the weekly grocery shopping.",
            "Year 1 represents the greatest incurred cost as this contains the cost of development, as well as the cost for marketing and IP protection. Years 2-5 will represent the cost of maintenance, marketing, and IP protection. We also make a gross revenue forecast following year 5--the point in which 100% adoption by households that shop at Whole Foods is achieved; this calculation does not take into account the revenue generated during the first 5 years of the application’s life.",
            "The magnetic connection between the iPad and the Magic Keyboard plays a vital role when it comes to connectivity or attachment. There are no extra switches, plugs, or Bluetooth pairing required in order for the two to attach each other. The simple built-in magnetism will do the job for the user. While the iPad is attached magnetically to the keyboard, the user will also experience the floating cantilever design. This floating design allows the user to adjust it smoothly with no lagging to have a better viewing angle while working or using it. In adjusting for a perfect angle, the hinge joint along the line on the leather-coating side works seamlessly with the help of the magnets holding the iPad.",
            "The most realistic way to improve the usage of the contactless payment will be the widespread information and advertisement for it. A lot of people are familiar with the contactless payment but some of them do not have the card in their hands nor are they comfortable using them. People need to start using those as a replacement of the traditional cards, and the cash. There are a lot of advantages of using the contactless payment over the paper money or contact payment.",
        ],
    },
    {
        "name": "AI samples",
        "criterion": 2,
        # The AI side of criterion 2. Compare the average combined score here
        # with the average from "my own writing".
        #
        # Model: Claude Opus 5.5 (claude-opus-5-5), one sample per prompt,
        # no editing. Prompt for every sample:
        #   "Write a short paragraph (about five sentences) about <topic>."
        # Topics, in order: morning routines, the benefits of reading, learning
        # a new language, regular exercise, social media, a rainy day,
        # volunteering, cities and climate change, the first day at a new job,
        # technology in education.
        "texts": [
            "A consistent morning routine can set the tone for the entire day. Starting with a few simple habits, such as drinking a glass of water, stretching, or writing down priorities, helps the mind shift from rest to focus. Many people find that avoiding their phone for the first half hour reduces stress and improves concentration. Over time, these small actions build momentum and create a sense of control. Ultimately, a well-designed morning routine is less about perfection and more about starting each day with intention.",
            "Reading offers benefits that extend far beyond entertainment. It strengthens vocabulary, improves concentration, and exposes readers to perspectives they might never encounter otherwise. Fiction in particular can build empathy by allowing people to experience the world through someone else's eyes. Regular reading has also been linked to reduced stress and better sleep when it replaces screen time before bed. Whether it is a novel, a biography, or a short article, every page contributes to a sharper and more curious mind.",
            "Learning a new language is a challenging but deeply rewarding experience. At first, unfamiliar sounds and grammar rules can feel overwhelming, but steady practice gradually turns confusion into understanding. Beyond practical advantages like travel and career opportunities, language learning also opens a window into another culture's values and humor. Research suggests that it can even improve memory and problem-solving skills. With patience and curiosity, anyone can make meaningful progress, one word at a time.",
            "Regular exercise is one of the most effective ways to improve both physical and mental health. Activities such as walking, cycling, or swimming strengthen the heart and help maintain a healthy weight. Exercise also releases endorphins, which can lift mood and reduce feelings of anxiety. Importantly, it does not need to be intense to be beneficial; even thirty minutes of moderate activity most days can make a significant difference. By finding an activity they genuinely enjoy, people are more likely to stay consistent over the long term.",
            "Social media has transformed the way people communicate, share information, and build communities. Platforms make it easy to stay connected with friends and family across great distances and to discover new ideas in real time. However, they also present challenges, including the spread of misinformation and the pressure to compare oneself with others. Studies have linked heavy use to increased anxiety, particularly among young people. Using social media mindfully, with clear boundaries, allows people to enjoy its benefits while limiting its downsides.",
            "There is something quietly comforting about a rainy day. The steady rhythm of raindrops against the window creates a soothing background that invites reflection and rest. Streets grow calmer as people stay indoors, and the air carries the fresh, earthy scent of wet soil. It is the perfect excuse to curl up with a warm drink, a good book, or a favorite film. In a busy world, a rainy day can serve as a gentle reminder to slow down and appreciate simple pleasures.",
            "Volunteering is a powerful way to make a positive difference in the community. Whether helping at a food bank, tutoring students, or cleaning up local parks, volunteers address real needs while building meaningful connections. The experience also benefits the volunteers themselves, offering a sense of purpose and opportunities to develop new skills. Many people find that giving their time reduces stress and increases overall happiness. In the end, volunteering strengthens both individuals and the communities they serve.",
            "Cities play a central role in the fight against climate change. Because they concentrate people, transportation, and energy use, urban areas are responsible for a large share of global greenhouse gas emissions. At the same time, this density creates opportunities for efficient solutions, such as expanded public transit, energy-efficient buildings, and green spaces that reduce heat. Many cities are already setting ambitious goals to cut emissions and adapt to rising temperatures. Thoughtful urban planning can help create communities that are both sustainable and livable.",
            "The first day at a new job is often a mix of excitement and nervousness. New employees are introduced to unfamiliar faces, systems, and expectations, which can feel overwhelming at first. Taking notes, asking questions, and showing genuine curiosity can help ease the transition. It is also a valuable opportunity to begin building relationships with colleagues and to understand the team's culture. While it may take time to feel fully comfortable, a positive attitude on the first day lays the foundation for future success.",
            "Technology has reshaped education in profound ways. Online platforms, interactive tools, and digital resources give students access to information and learning opportunities that were once out of reach. Teachers can use technology to personalize instruction, track progress, and engage students through multimedia content. However, challenges such as unequal access to devices and the risk of distraction must be addressed. When used thoughtfully, technology can enhance learning and prepare students for an increasingly digital world.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Order matters: expected human, unsure, ai.
        #   1. Known human: Pride and Prejudice, ch. 1 — Jane Austen (1813).
        #   2. Borderline: AI-written paragraph, lightly edited by hand.
        #   3. AI-generated: the Willow Creek paragraph.
        "texts": [
            "Mr. Bennet was so odd a mixture of quick parts, sarcastic humour, reserve, and caprice, that the experience of three-and-twenty years had been insufficient to make his wife understand his character. Her mind was less difficult to develop. She was a woman of mean understanding, little information, and uncertain temper. When she was discontented, she fancied herself nervous. The business of her life was to get her daughters married; its solace was visiting and news.",
            "Remote work has changed how lots of people think about their jobs. Many workers like the flexibility it gives them, since they can set their own hours and skip the commute. But it isn't perfect. Some people feel lonely working from home, and it can be hard to separate work time from personal time. Companies are still figuring out the right balance between remote and office work.",
            "On a quiet Sunday afternoon, the small town of Willow Creek seemed to move at its own pace. A gentle breeze carried the scent of freshly brewed coffee through the streets, while golden leaves drifted slowly from the trees. At the corner bookstore, a young woman discovered an old journal tucked behind a row of forgotten novels. Its pages were filled with handwritten stories, mysterious sketches, and notes from someone who had lived there nearly a century earlier. What began as an ordinary afternoon soon turned into an unexpected adventure, reminding her that even the simplest moments can lead to extraordinary discoveries.",
        ],
    },
    # Criterion 4 (appeals) can't be expressed as a submission, so it lives in
    # run_extra_checks.py, which submits, appeals, and reads /log back.
    {
        "name": "bad input",
        "criterion": 5,
        # Cases 1–6 from criteria.md, in order. Case 7 (unparseable JSON) and
        # the /health check after each case are in run_extra_checks.py — a
        # body here is always sent as valid JSON.
        "bodies": [
            {"creator_id": "eval_bad_missing_text"},                  # 400
            {"text": "", "creator_id": "eval_bad_empty"},            # 400
            {"text": "A perfectly ordinary sentence of text."},      # 400
            {"text": 12345, "creator_id": "eval_bad_number"},        # 400
            {"text": "word " * 2001, "creator_id": "eval_bad_huge"}, # 413
            {"text": "   \n\t  ", "creator_id": "eval_bad_space"},   # 400
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
