GoogleDescription = """The following are the suggestions for google ads campaigns of my products:

Product Name : PC Bluetooth adapter
Product Description: The PC Bluetooth adapter applies the latest Bluetooth 5.1 chipset greatly reduces the power consumption of Bluetooth(BLE).
Tone : Professional
Output: us English
Google Ads suggestion :The World's Most Advanced Bluetooth(BLE) 5.1 Chipset

Generate a google ads suggestion for this product:
Product Name : {}
Product Description: {}
Tone:{}
Output Language : {}
Google Ads suggestion : 
"""

ProductDescription_prompt = """Generate me a  {user_template_name} for my product or brand named {product_name}.
-With these features :{user_product_description}.
-In this Language: {output_language}.
-with this tone: {tone}."""

UserReview = """Generate me a user product review for my product or brand {}."""

FacebookListicle = """
The following are Facebook Listicle for some products:

Product Name: Bluetooth Adapter
Output Language: us English
Product Description: The PC Bluetooth adapter applies the latest Bluetooth 5.1 chipset greatly reduces the power consumption of Bluetooth(BLE). 
Facebook Listicle:
Connect Your PC To The Smartest Technology Available
✅ Easily Pair With Any Bluetooth Device 📱
✅ Stream Music 👂
✅ Connect To Wi-Fi With Ease 🌆
✅ Extend Battery Life 👌

Generate a Facebook Listicle for my product named: {}
Add some emoticons, please!
In {} Language.
In a {} tone.
Product  description :{}
Facebook Listicle:
"""

BlogIdeaPrompt = """Generate me in {} with {} Tone 5 Blog Post ideas suggestions for {} which {}.
"""

Cancellation_email_prompt = """"Write a {} cancellation email for my product or Brand.

Product or brand Name : {}
Product Description : {}
Cancellation email in {} :
"""

marketing_formulas = """Generate in {} Language a {} {} marketing formula for my product in this order :\n
{}
Product name: {}.\n
Product Description: {}\n
{} language {}:
"""

four_steps_marketing = """Please propose a {} four-step process for creating effective marketing messages by  "Problem-Promise-Proof-Proposal" formula for my product named: {}.
using this language: {}.
using theses features: {}."""

Three_steps_marketing = """Please propose a {} three-step process for creating effective marketing messages by  {} formula for my product named: {}.
using this language: {}.
using theses features: {}."""


"""REVOMED 
step_list = user_template_name.split("-")
        steps = ':\n\n-'.join(step_list)
"""
