import json
J=json.load(open('jobs.json'))['panel']
T=" Keep the exact hand-drawn colored-pencil and watercolor style of the image, the same stick-figure characters (round heads, dot eyes, thin navy stick arms and legs), camera almost still, gentle natural motion, no text, no new characters."
M={1:"The lights go out: the ceiling lamp flickers off and the man on the sofa looks up, surprised, in the dark living room.",
5:"The two children on the sofa grumble in the dark, the phone screen glows on their faces and flickers.",
29:"The candle flames flicker gently around the dark room while the boy walks slowly past them.",
45:"The man inside the car plugs the phone cable into the dashboard and the phone screen lights up.",
48:"The woman opens the fridge door with a flashlight, looks inside and the cold air puffs out.",
57:"The man switches on the flashlight and the warm beam sweeps slowly across the dark living room.",
59:"The two children switch on their flashlights and smile, the beams move around the dark bedroom.",
65:"The man puts his hand on the fridge door, hesitates, then takes his hand away and nods.",
69:"Holding a flashlight, the man crouches and pulls the TV plug out of the wall socket.",
76:"The man pushes the window wide open and the night breeze moves the curtains.",
78:"The family walks out through the front door into the yard at night, flashlight beams moving.",
85:"The grandpa looks at the insulin pen under the flashlight, thinking, and turns it in his hand.",
94:"The grandma gently places the medicine wrapped in a cloth into the cooler with ice and closes the lid.",
98:"The two children make animal shadow puppets on the wall with their flashlights and laugh.",
112:"The dog wags its tail happily next to the bag of dog food and the water jug.",
118:"The couple arranges the emergency kit on the kitchen table: flashlight, batteries, water bottles and radio.",
119:"The ceiling light switches on and the whole family raises their arms and cheers.",
122:"The man plugs the TV back into the socket calmly, one device at a time.",
129:"The doctor listens to the woman's chest with the stethoscope while she breathes calmly.",
141:"The whole family waves and smiles in the backyard at sunset, the dog wags its tail and the cat blinks."}
R=[{"index":k,"params":{"model":"gemini_omni_flash_1_2","prompt":v+T,"mode":"image-to-video","resolution":"720p","duration":15,"aspect_ratio":"16:9","medias":[{"value":J[str(k)],"role":"start_image"}]}} for k,v in M.items()]
print(json.dumps(R[:10])); print(json.dumps(R[10:]))
