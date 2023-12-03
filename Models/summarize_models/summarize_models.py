from summarizer import Summarizer

summary = """
TULSA, Okla., July 27, 2023 /PRNewswire/ -- CLEAR YOU, the secure identity company, today announced it is launching its identity verification technology at Tulsa International Airport (TUL)'s Main Terminal, bringing frictionless and predictable travel experiences to Tulsa. CLEAR's launch at TUL is expected to create 25 jobs and generate approximately $1.2 million annually in local economic impact.

"We're thrilled to welcome CLEAR to Tulsa along with the customer experience they will offer to our passengers," said Andrew Pierini, Executive Vice President and Chief Commercial Officer at Tulsa International Airport. "CLEAR brings a cutting-edge amenity that allows passengers a smooth, expedited journey through airport security and we are excited to have them operating at TUL."
"CLEAR is on the side of the American traveler, and our lanes help make the journey as joyful as the destination," said CLEAR CEO Caryn Seidman-Becker. "We're excited to bring Tulsa's travelers the predictable, seamless, and safe airport experience they deserve."
Today's launch represents continued growth in CLEAR's national footprint, where it serves a total of 53 airports and over 16 million members. CLEAR already serves 9 of TUL's top 10 domestic destinations, allowing members traveling through TUL to use CLEAR on both ends of their journey. Members use CLEAR's network of dedicated lanes to verify their identity with their eyes or fingers, replacing the need to take out their wallet and driver's license. After verification, a CLEAR Ambassador escorts members through the dedicated lane and directly to TSA physical security, saving them time waiting in line at the security checkpoint.
CLEAR Plus an opt-in membership that provides access to CLEAR's expedited identity verification lanes costs about $16 a month billed annually, with discounts available for Delta Air Lines, United Airlines, Alaska Airlines and American Express members. Newly enrolling active military, veterans, and government officials are also eligible for discounted memberships, and additional family members can be added to an existing CLEAR Plus account for just $70 per adult per year.

About CLEARCLEAR's mission is to create frictionless experiences. With more than 16 million members and a growing network of partners across the world, CLEAR's identity platform is transforming the way people live, work, and travel. Whether you are traveling, at the stadium, or on your phone, CLEAR connects you to the things that make you, you making everyday experiences easier, more secure, and friction-free. CLEAR is committed to privacy done right. Members are always in control of their own information, and we never sell member data. For more information, visit clearme.com.
About Tulsa International Airport Nearly 3 million people use Tulsa International Airport every year to connect with loved ones, pursue business opportunities or explore new destinations. At Tulsa International Airport, we take pride in welcoming visitors from around the world to Tulsa and continue to prioritize investments in our facilities and services that make their experience as smooth as possible. Visit www.flytulsa.com for more information.
SOURCE  CLEAR
© 2023 Benzinga.com. Benzinga does not provide investment advice. All rights reserved.
"""

summarizer = Summarizer()

summary = summarizer(summary, max_length=200, min_length=50, length_penalty=1.0, num_sentences=5)

# Print the generated summary
print("Input Text:")
print(summary)
print("\nGenerated summary:")
print(summary)
