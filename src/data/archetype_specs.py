# archetype_specs.py
# --------------------------------------------------
# Dashboard-ready archetype descriptions
# Based on advanced clustering of current NBA players
# --------------------------------------------------

ARCHETYPE_SPECS = {

    "Movement Shooter": {
        "description": (
            "Off-ball perimeter scorers who generate offense through movement, "
            "spot-ups, and quick catch-and-shoot opportunities, primarily from "
            "the corners and above the break."
        ),
        "strengths": [
            "High-volume spot-up and catch-and-shoot three-point usage",
            "Strong corner three shot tendency",
            "Efficient shooting with minimal dribbling",
            "Low turnover offensive profile"
        ],
        "limitations": [
            "Minimal on-ball creation",
            "Limited rim pressure and paint scoring",
            "Low foul-drawing rates"
        ],
        "tags": [
            "Movement Shooter",
            "Spot-Up Threat",
            "Floor Spacer",
            "Low Usage"
        ],
        "examples": [
            "Keegan Murray",
            "Klay Thompson",
            "Buddy Hield",
            "Kentavious Caldwell-Pope"
        ]
    },

    "3&D": {
        "description": (
            "Low-usage wings who provide spacing through corner shooting while "
            "contributing defensive activity and effort without demanding the ball."
        ),
        "strengths": [
            "Heavy corner three-point involvement",
            "Reliable spot-up shooting role",
            "Strong defensive movement and perimeter activity",
            "Low-mistake offensive decision-making"
        ],
        "limitations": [
            "Very limited self-creation",
            "Below-average scoring efficiency overall",
            "Minimal playmaking responsibility"
        ],
        "tags": [
            "3&D",
            "Corner Spacer",
            "Perimeter Defender",
            "Low Usage"
        ],
        "examples": [
            "Herbert Jones",
            "Josh Green",
            "Toumani Camara",
            "Royce O’Neale"
        ]
    },

    "Wing Shot Creator": {
        "description": (
            "Versatile scoring wings who can create offense from multiple areas, "
            "including isolation, post-ups, and pick-and-rolls, while maintaining "
            "positional flexibility."
        ),
        "strengths": [
            "Strong isolation and post-up scoring efficiency",
            "Comfortable handling the ball in half-court sets",
            "Can score against mismatches in the post",
            "Reliable secondary creators"
        ],
        "limitations": [
            "Higher turnover risk in isolation",
            "Less off-ball shooting volume than pure spacers",
            "Moderate defensive variability depending on role"
        ],
        "tags": [
            "Wing Creator",
            "Isolation Scorer",
            "Post Mismatch",
            "Secondary Handler"
        ],
        "examples": [
            "Jayson Tatum",
            "Jaylen Brown",
            "Mikal Bridges",
            "Paolo Banchero"
        ]
    },

    "All-Around Guard": {
        "description": (
            "Balanced guards who handle the ball frequently, operate in pick-and-roll, "
            "and contribute across multiple offensive areas without specializing in "
            "one extreme role."
        ),
        "strengths": [
            "Comfortable pick-and-roll ball handlers",
            "High on-ball time and dribble volume",
            "Versatile offensive involvement",
            "Capable secondary playmakers"
        ],
        "limitations": [
            "Limited off-ball cutting and finishing",
            "Minimal interior scoring impact",
            "Below-average size for defensive matchups"
        ],
        "tags": [
            "Combo Guard",
            "Balanced Creator",
            "PnR Handler",
            "Versatile"
        ],
        "examples": [
            "Cameron Payne",
            "Mike Conley",
            "Anfernee Simons",
            "Chris Paul"
        ]
    },

    "Rim Runner / Protector": {
        "description": (
            "Interior-focused bigs who generate offense around the rim through cuts, "
            "rolls, and putbacks while anchoring the paint defensively."
        ),
        "strengths": [
            "Elite rim involvement and paint touch frequency",
            "Strong finishing efficiency near the basket",
            "High cutting and putback activity",
            "Shot-blocking and interior defensive presence"
        ],
        "limitations": [
            "Minimal shooting range",
            "Very limited off-dribble or perimeter offense",
            "Low three-point efficiency"
        ],
        "tags": [
            "Rim Runner",
            "Interior Finisher",
            "Roll Man",
            "Paint Protector"
        ],
        "examples": [
            "Rudy Gobert",
            "Jarrett Allen",
            "Walker Kessler",
            "Ivica Zubac"
        ]
    },

    "Shot Creator Guard": {
        "description": (
            "Primary on-ball offensive engines who generate scoring and playmaking "
            "through isolation, drives, and pick-and-roll creation."
        ),
        "strengths": [
            "High-usage pick-and-roll handling",
            "Strong isolation and pull-up scoring volume",
            "High assist generation and playmaking load",
            "Frequent downhill rim pressure"
        ],
        "limitations": [
            "Elevated turnover rates",
            "Heavy ball dominance",
            "Defensive impact varies by matchup"
        ],
        "tags": [
            "Primary Creator",
            "Isolation Scorer",
            "PnR Engine",
            "High Usage"
        ],
        "examples": [
            "Anthony Edwards",
            "Devin Booker",
            "James Harden",
            "Trae Young"
        ]
    },

    "Glue Guy": {
        "description": (
            "Low-usage role players who fill gaps, rebound uncontested possessions, "
            "and contribute without commanding offensive opportunities."
        ),
        "strengths": [
            "Opportunistic rebounding",
            "Low-mistake offensive play",
            "Willing off-ball contributors",
            "Flexible role adaptability"
        ],
        "limitations": [
            "Limited scoring efficiency",
            "Minimal transition and cutting impact",
            "Low offensive ceiling"
        ],
        "tags": [
            "Glue Guy",
            "Role Player",
            "Low Usage",
            "Utility"
        ],
        "examples": [
            "Bruce Brown",
            "Caleb Martin",
            "Delon Wright"
        ]
    },

    "Stretch Big": {
        "description": (
            "Frontcourt players who provide spacing through spot-up shooting while "
            "contributing as roll finishers without significant ball-handling responsibility."
        ),
        "strengths": [
            "Pick-and-roll finishing efficiency",
            "Spot-up and catch-and-shoot shooting presence",
            "Floor spacing from the frontcourt",
            "Positional versatility between PF/C"
        ],
        "limitations": [
            "Minimal on-ball creation",
            "Limited passing and playmaking",
            "Defensive role varies by matchup"
        ],
        "tags": [
            "Stretch Big",
            "Floor Spacer",
            "Roll Finisher",
            "Low Usage"
        ],
        "examples": [
            "Myles Turner",
            "Al Horford",
            "Jabari Smith Jr.",
            "Bobby Portis"
        ]
    },

    "All-Around Big": {
        "description": (
            "Complete frontcourt players who combine post scoring, interior defense, "
            "and roll finishing with strong physical presence."
        ),
        "strengths": [
            "High post-up usage and efficiency",
            "Strong interior defensive impact",
            "Effective roll finishing",
            "Physical size and rebounding presence"
        ],
        "limitations": [
            "Limited perimeter defensive range",
            "Moderate ball-handling ability",
            "Shot creation depends on matchup"
        ],
        "tags": [
            "Two-Way Big",
            "Post Scorer",
            "Interior Anchor",
            "Physical"
        ],
        "examples": [
            "Nikola Jokić",
            "Bam Adebayo",
            "Anthony Davis",
            "Domantas Sabonis"
        ]
    },

    "Pure Point Guard": {
        "description": (
            "Pass-first guards who control tempo, initiate offense, and prioritize "
            "playmaking over scoring."
        ),
        "strengths": [
            "High passing volume and assist rates",
            "Strong pick-and-roll orchestration",
            "Excellent ball control and tempo management",
            "Reliable decision-making"
        ],
        "limitations": [
            "Lower scoring efficiency",
            "Limited physical size",
            "Relies on teammates for scoring impact"
        ],
        "tags": [
            "Pure PG",
            "Floor General",
            "Playmaker",
            "Pass-First"
        ],
        "examples": [
            "Tyrese Haliburton",
            "Isaiah Collier",
            "Andrew Nembhard"
        ]
    },

    "Post Scorer": {
        "description": (
            "Interior scorers who operate primarily from the post and elbows, "
            "leveraging size and strength to generate offense near the basket."
        ),
        "strengths": [
            "Heavy post-up usage and efficiency",
            "Strong interior touch and finishing",
            "Physical presence in half-court offense",
            "Reliable paint scoring"
        ],
        "limitations": [
            "Limited shooting range",
            "Minimal perimeter creation",
            "Pace-dependent offensive impact"
        ],
        "tags": [
            "Post Scorer",
            "Interior Offense",
            "Physical Big"
        ],
        "examples": [
            "Jonas Valančiūnas",
            "Deandre Ayton",
            "Nic Claxton"
        ]
    }
}
