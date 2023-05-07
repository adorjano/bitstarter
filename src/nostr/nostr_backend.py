# nostr_backend.py

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all resources

ideas = [
    {
        "id": '0adasdw3rw4f34f4f34',
        "name": "Eco-friendly City",
        "subtitle": "A vision for a greener urban environment",
        "message": "Let's build a city with more parks, green rooftops, and eco-friendly transportation. "
                   "Imagine a city where the air is clean and the streets are lined with trees. "
                   "We can create urban environments that promote health and well-being by "
                   "prioritizing green spaces and investing in public transportation options "
                   "like bike lanes, electric buses, and efficient rail systems. "
                   "Furthermore, we can encourage businesses to adopt sustainable practices "
                   "by offering incentives for green building design and renewable energy use. "
                   "Together, we can create a vibrant, thriving community that puts the environment first, "
                   "protecting the planet for future generations.",
        "bannerImage": "https://as1.ftcdn.net/v2/jpg/04/48/29/76/1000_F_448297652_sYW6YiBR2RXxzjkHCEhgdQSrHOQBuUkf.jpg",
    },
    {
        "id": "vrewt3tg45z56h56u67ujtz",
        "name": "Zero Waste Lifestyle",
        "subtitle": "Reducing our footprint one step at a time",
        "message": "Join the movement to eliminate single-use plastics and adopt sustainable practices. "
                   "Every day, we generate enormous amounts of waste, much of which ends up in landfills or the ocean. "
                   "By embracing a zero-waste lifestyle, we can significantly reduce our environmental impact. "
                   "Start by evaluating your daily habits and identifying areas where you can reduce waste. "
                   "Consider replacing disposable items with reusable alternatives, such as cloth shopping bags, "
                   "metal straws, and glass containers. Be mindful of your consumption and try to buy products "
                   "with minimal packaging. Support local farmers and businesses that prioritize sustainability. "
                   "Additionally, learn to compost your food scraps and recycle responsibly. "
                   "Remember, every small action adds up, and together, we can create a cleaner, greener world "
                   "for ourselves and future generations.",
        "bannerImage": "https://as1.ftcdn.net/v2/jpg/02/68/81/22/1000_F_268812279_cVMsQJ8UWfV8k8HO2oqjhRY1XhopgE68.jpg"
    },
    {
    "bannerImage": "https://as1.ftcdn.net/v2/jpg/02/17/88/55/1000_F_217885532_Pa1CrTUGWU7JIyJx73QhfL9n8SjWU7v6.jpg",
    "id": "1b1t5t4rt3rpr0m0t3",
    "message": "<h2 style='text-align:center;'>Welcome to <strong>Bitstarter</strong></h2><br><p style='font-size:18px; line-height:1.6; text-align:justify;'>The groundbreaking platform that is poised to revolutionize the way we innovate, collaborate, and fund the projects of the future. Our mission is to create an environment where visionary ideas meet cutting-edge technology and receive the financial support they need to flourish. Bitstarter connects idea generators, developers, and investors, providing a seamless and efficient platform for collaboration and growth.<br><br>At the core of our platform is the belief in decentralization and the transformative potential of open-source technology. Bitstarter leverages the power of Nostr and Bitcoin to foster a new era of innovation, empowering individuals and teams to think beyond the conventional boundaries and reshape the world around us. We are committed to nurturing an ecosystem that fosters creativity, collaboration, and progress.<br><br>By streamlining the communication between creators, tech experts, and funding sources, Bitstarter eliminates the barriers that have traditionally hindered the progress of groundbreaking ideas. Our platform offers a comprehensive suite of tools and resources to guide projects from inception to realization, ensuring that every project has the opportunity to reach its full potential.<br><br>Bitstarter is more than just a platform; it's a community of visionaries, developers, and investors who are passionate about driving change and pushing the boundaries of what is possible. Our users come from diverse backgrounds and industries, united by a shared vision of a future driven by innovation and collaboration.<br><br>We understand that great ideas require not only financial support but also the right environment to thrive. That's why we've built Bitstarter with a focus on user experience, providing a platform that is intuitive, user-friendly, and adaptable to the unique needs of every project. From customizable project pages to advanced communication and project management tools, we've designed Bitstarter to help bring your ideas to life.<br><br>The future of innovation lies in the hands of visionaries like you, and Bitstarter is here to support your journey. Join us as we embark on an exciting adventure to reshape the world through the power of decentralized collaboration and ground-breaking ideas. With Bitstarter, there are no limits to what we can achieve together.<br><br>Discover the potential of Bitstarter and join us on this exhilarating journey to shape a brighter, bolder, and more innovative tomorrow. Together, let's turn ideas into reality and transform the world, one project at a time.</p>",
    "name": "Bitstarter",
    "subtitle": "Revolutionizing the innovation ecosystem"
    }

    # ...
]


cards_lookup = {c["id"]: c for c in ideas}

comments_data = [
    {
        "idea_id": "1b1t5t4rt3rpr0m0t3",
        "pubkey": "a8bc84d333fse",
        "comment": "I really like this idea!",
    },
    {
        "idea_id": "1b1t5t4rt3rpr0m0t3",
        "pubkey": "a8bc84d333fse",
        "comment": "This is a game changer!",
    },
    {
        "idea_id": "1b1t5t4rt3rpr0m0t3",
        "pubkey": "a8bc84d333fse",
        "comment": "Can't wait to see this implemented!",
    },
]

@app.route('/comments/<string:idea_id>', methods=['GET'])
def get_comments(idea_id):
    comments_for_card = [comment for comment in comments_data if comment["idea_id"] == idea_id]
    return jsonify(comments_for_card)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    idea_id = request.form.get("idea_id")
    comment = request.form.get("comment")

    print(f"Idea ID: {idea_id}")
    print(f"Comment: {comment}")

    return '', 204

@app.route('/cards', methods=['GET'])
def get_cards():
    return jsonify(ideas)

@app.route('/cards/<string:card_id>', methods=['GET'])
def get_card(card_id):
    if card_id in cards_lookup:
        return jsonify(cards_lookup[card_id])
    else:
        return jsonify({"error": "Card not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
