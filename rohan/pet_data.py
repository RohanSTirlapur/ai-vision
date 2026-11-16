"""
PetVision AI - Supported Pet Animal Categories and Knowledge Base
Contains rich metadata, care tips, fun facts, and biological profiles
for the 8 supported pet animal categories.
"""

PET_PROFILES = {
    "Dog": {
        "display_name": "Dog",
        "category_id": 1,
        "emoji": "🐕",
        "scientific_name": "Canis lupus familiaris",
        "class": "Mammalia",
        "diet": "Omnivorous (High-quality protein, balanced grains & vegetables)",
        "lifespan": "10 – 15 years (varies by size)",
        "temperament": "Loyal, social, intelligent, energetic",
        "key_care_tips": [
            "Daily physical exercise and mental stimulation are essential.",
            "Maintain regular vaccinations, dental checks, and vet checkups.",
            "Provide consistent positive reinforcement training and socialization.",
            "Ensure fresh water is available at all times."
        ],
        "fun_facts": [
            "A dog's sense of smell is up to 100,000 times more acute than a human's.",
            "Each dog has a unique nose print, much like human fingerprints.",
            "Dogs can learn over 100 words and basic gestures."
        ],
        "activity_level": "High",
        "badge_color": "#3B82F6"
    },
    "Cat": {
        "display_name": "Cat",
        "category_id": 2,
        "emoji": "🐱",
        "scientific_name": "Felis catus",
        "class": "Mammalia",
        "diet": "Obligate Carnivore (Animal protein rich, taurine essential)",
        "lifespan": "12 – 18+ years (indoor cats often live longer)",
        "temperament": "Independent, curious, agile, affectionate",
        "key_care_tips": [
            "Provide scratching posts to maintain claw health and mark territory.",
            "Clean litter boxes daily and place in quiet, accessible locations.",
            "Keep interactive toys for predatory play (feathers, laser pointers).",
            "High-protein wet and dry food rotation prevents kidney dehydration."
        ],
        "fun_facts": [
            "Cats spend roughly 70% of their lives sleeping and 15% grooming.",
            "A domestic cat can run at speeds up to 30 mph (48 km/h) in short bursts.",
            "Purring is not just for happiness; it also promotes bone and tissue healing."
        ],
        "activity_level": "Moderate",
        "badge_color": "#8B5CF6"
    },
    "Rabbit": {
        "display_name": "Rabbit",
        "category_id": 3,
        "emoji": "🐰",
        "scientific_name": "Oryctolagus cuniculus",
        "class": "Mammalia",
        "diet": "Herbivorous (80% fresh Timothy hay, dark leafy greens, limited pellets)",
        "lifespan": "8 – 12 years",
        "temperament": "Gentle, timid, inquisitive, social with patience",
        "key_care_tips": [
            "Fresh timothy hay must make up at least 80% of their daily diet to wear down continuously growing teeth.",
            "House rabbits need rabbit-proofed rooms to roam freely.",
            "Never pick a rabbit up by its ears; always support the hindquarters.",
            "Sensitive digestive system: watch out for GI stasis signs."
        ],
        "fun_facts": [
            "When happy, rabbits perform an acrobatic twist and leap called a 'binky'.",
            "Their teeth never stop growing throughout their entire lifetime.",
            "Rabbits have nearly 360-degree panoramic vision to detect predators."
        ],
        "activity_level": "Moderate to High (crepuscular: active dawn & dusk)",
        "badge_color": "#EC4899"
    },
    "Bird": {
        "display_name": "Bird",
        "category_id": 4,
        "emoji": "🦜",
        "scientific_name": "Aves (Parrots, Finches, Canaries, etc.)",
        "class": "Aves",
        "diet": "Herbivorous / Frugivorous / Granivorous (Pellets, seeds, fresh veggies & fruits)",
        "lifespan": "5 – 60+ years (small birds ~10 yrs, large parrots 50+ yrs)",
        "temperament": "Vocal, intelligent, social, observant",
        "key_care_tips": [
            "Never expose pet birds to non-stick Teflon cookware fumes (PTFE is fatal).",
            "Provide spacious cages with horizontal bars for climbing and multiple perch textures.",
            "Rotate foraging toys to prevent feather plucking from boredom.",
            "Provide natural sunlight or avian full-spectrum lighting for vitamin D3."
        ],
        "fun_facts": [
            "Birds have hollow bones filled with air sacs that enable flight efficiency.",
            "Parrots are among the few animal groups that can mimic human speech with precise cadence.",
            "Avian vision detects ultraviolet (UV) light invisible to the human eye."
        ],
        "activity_level": "High",
        "badge_color": "#10B981"
    },
    "Hamster": {
        "display_name": "Hamster",
        "category_id": 5,
        "emoji": "🐹",
        "scientific_name": "Cricetinae (Syrian, Dwarf, Roborovski)",
        "class": "Mammalia",
        "diet": "Omnivorous (Hamster seed mix, pellets, occasional mealworms & fresh veggies)",
        "lifespan": "2 – 3 years",
        "temperament": "Solitary (especially Syrians), nocturnal, burrowing",
        "key_care_tips": [
            "Syrian hamsters MUST be housed alone; they are strictly territorial.",
            "Provide deep bedding (at least 6-8 inches) for natural burrowing behaviors.",
            "Supply a solid-surface exercise wheel with adequate diameter to prevent back curvature.",
            "Handle gently in evening hours when they are naturally awake."
        ],
        "fun_facts": [
            "Hamsters have cheek pouches that can stretch back to their shoulders to carry food.",
            "They can run up to 5 to 6 miles (9 km) in a single night on their exercise wheel.",
            "Their name comes from the German word 'hamstern', which means 'to hoard'."
        ],
        "activity_level": "High at night (strictly nocturnal)",
        "badge_color": "#F59E0B"
    },
    "Guinea Pig": {
        "display_name": "Guinea Pig",
        "category_id": 6,
        "emoji": "🐹",
        "scientific_name": "Cavia porcellus",
        "class": "Mammalia",
        "diet": "Herbivorous (Timothy hay unlimited, Vitamin C fortified pellets & fresh greens)",
        "lifespan": "5 – 8 years",
        "temperament": "Social, vocal, gentle, communicative",
        "key_care_tips": [
            "Guinea pigs CANNOT synthesize Vitamin C; daily dietary supplementation is mandatory (bell peppers, kale).",
            "Always keep them in pairs or small bonded groups; they suffer deep loneliness alone.",
            "Need flat-bottom cages without wire flooring to protect delicate footpads (bumblefoot).",
            "Constant supply of fresh timothy hay is mandatory for digestion and dental care."
        ],
        "fun_facts": [
            "They make a distinct cheerful squeaking sound called 'wheeking' when they smell vegetables.",
            "When excited, they jump straight up into the air in a behavior called 'popcorning'.",
            "Guinea pigs are born fully furred with eyes open and teeth ready to chew."
        ],
        "activity_level": "Moderate (active in short bursts day and night)",
        "badge_color": "#E11D48"
    },
    "Fish": {
        "display_name": "Fish",
        "category_id": 7,
        "emoji": "🐠",
        "scientific_name": "Actinopterygii (Goldfish, Bettas, Tetras, Clownfish, etc.)",
        "class": "Actinopterygii",
        "diet": "Varies by species (Flakes, pellets, frozen brine shrimp, algae wafers)",
        "lifespan": "3 – 20+ years (Goldfish can live 15-20+ years in proper tanks!)",
        "temperament": "Peaceful to territorial (species dependent)",
        "key_care_tips": [
            "Always cycle your aquarium nitrogen cycle before introducing any fish.",
            "Test water parameters (ammonia, nitrite, nitrate, pH, temperature) regularly.",
            "Avoid overfeeding; unconsumed food decays into toxic ammonia.",
            "Perform weekly 20-25% water changes with dechlorinated water."
        ],
        "fun_facts": [
            "Goldfish have a memory span of at least 3 to 5 months, debunking the '3-second memory' myth.",
            "Fish communicate using acoustic sounds, bioluminescence, and chemical pheromones.",
            "Most fish possess a lateral line system that senses vibrations and water pressure changes."
        ],
        "activity_level": "Continuous",
        "badge_color": "#06B6D4"
    },
    "Turtle": {
        "display_name": "Turtle",
        "category_id": 8,
        "emoji": "🐢",
        "scientific_name": "Testudines (Red-eared sliders, Box turtles, Mud turtles, etc.)",
        "class": "Reptilia",
        "diet": "Omnivorous (Aquatic pellets, leafy greens, earthworms, crickets, aquatic plants)",
        "lifespan": "25 – 50+ years (a lifelong commitment)",
        "temperament": "Placid, observant, sun-basking, solitary",
        "key_care_tips": [
            "A dry basking dock with BOTH heat lamp and UVB lighting is mandatory for shell calcification.",
            "Water temperature and basking temperature gradients must be maintained with heaters.",
            "Powerful filtration is required as aquatic turtles produce significant waste.",
            "Wash hands thoroughly after handling to prevent Salmonella transmission."
        ],
        "fun_facts": [
            "A turtle's shell is actually part of its skeleton, composed of over 50 interconnected bones.",
            "Turtles have walked the Earth for over 220 million years, pre-dating many dinosaurs.",
            "They can absorb oxygen through their cloaca while hibernating underwater in cold winters."
        ],
        "activity_level": "Low to Moderate (alternating between swimming and basking)",
        "badge_color": "#059669"
    }
}
