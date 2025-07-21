# Glitch Game Objects - Historical MMO Data Archive

This repository contains a comprehensive collection of game objects exported from **Glitch**, a unique web-based MMO that ran from 2011-2012. Created by Tiny Speck (later Slack Technologies), Glitch was known for its whimsical art style, collaborative gameplay, and innovative social mechanics.

## 🎮 About Glitch

Glitch was a browser-based massively multiplayer game where players explored a colorful world, learned skills, crafted items, and collaborated on various activities. The game featured:

- **Skill-based progression** without traditional combat
- **Collaborative economics** and resource sharing  
- **Rich social systems** with friends, groups, and communication
- **Deep crafting and collection** mechanics
- **Unique world with 11 Giants** and whimsical lore

When Glitch shut down in December 2012, Tiny Speck open-sourced much of the game client and released anonymous player data, making it a valuable resource for game developers and researchers.

## 📁 Repository Contents

This repository contains **XML-serialized game objects** representing a complete player character and their associated data. The files demonstrate the complex interconnected systems that powered Glitch's gameplay.

### 🚀 Starting Point

**`PDOADP8FT3V22TI.xml`** - The main player object for "Apoidea" (userid: 122470)
- Contains metabolics (energy: 893/900, mood: 872/900)
- References to all connected subsystems
- Character appearance and clothing data
- Location and state information

## 🗂️ Object Types & File Structure

### Data Containers (`D*.xml`)
Complex data structures containing game progression and state:

- **`DDOADR8FT3V22TN.xml`** - Skills (animal kinship, cooking, mining, meditation, etc.)
- **`DDOADS8FT3V22TF.xml`** - Learned recipes with timestamps
- **`DDOADU8FT3V22TO.xml`** - 50+ achievements (from "pennypincher" to "executive_flunky")
- **`DDOAEP8FT3V22UD.xml`** - Item collection counters (727 grain, 364 bubbles, etc.)
- **`DDOAEQ8FT3V22UD.xml`** - Imagination upgrades and progression
- **Quest Systems**: Todo (`DDOADV8FT3V22T1`), Done (`DDOAE08FT3V22T0`), Failed (`DDOAE18FT3V22TR`)

### Bags & Containers (`B*.xml`)
Inventory management and storage systems:

- **`BDOAES8FT3V22UJ.xml`** - Private Furniture Storage (146 lines of furniture items)
- **`BHFOF9AMNL13SL0.xml`** - Main inventory with tools, food, and resources
- Various specialized bags for different item types

### Items (`I*.xml`)  
Individual game objects and entities:

- **`IHFB2H28AP23FVQ.xml`** - "Bubble Tree" (trant_bubble) with health/maturity
- **`IHFB2I28AP23G3J.xml`** - Another Bubble Tree instance
- Various furniture, decorations, and collectibles

### Groups & Social (`R*.xml`)
Social and communication systems:

- **`RA512UITCLA22AD.xml`** - "Live Help" chat group with active roster
- Other group containers for social organization

## 🔍 Hidden Complexity & Features

This data reveals the sophisticated systems that made Glitch unique:

### 🎯 Skill & Progression Systems
- **Timestamped learning**: Each skill shows Unix timestamp when learned
- **Complex progression trees**: Skills unlock other skills and capabilities
- **Achievement tracking**: Detailed progress on dozens of achievement categories

### 🎒 Advanced Inventory Management
- **Nested containers**: Bags within bags with item references
- **Specialized storage**: Separate systems for furniture, tools, consumables
- **Item state tracking**: Durability, enhancement, and usage data

### 🤝 Social & Communication
- **Multi-tier friends system**: Buddies, reverse contacts, ignore lists
- **Group management**: Chat rosters and member tracking
- **Mail system**: In-game messaging infrastructure

### 📊 Detailed Analytics
- **Collection counters**: Track every item type ever collected
- **Behavioral data**: Quest completion, recipe usage, social interactions
- **Economic tracking**: Currency, transactions, and resource flow

### 🏠 Housing & Decoration
- **Furniture storage**: Organized decoration and furniture systems
- **Room management**: Placement and arrangement data
- **Customization tracking**: Avatar appearance and housing choices

## 💡 Use Cases

### For Game Developers
- **Reference implementation** for MMO object systems and data modeling
- **Inventory management** patterns for complex nested containers
- **Social system architecture** with friends, groups, and communication
- **Progression mechanics** showing skill trees and achievement systems
- **Data persistence** examples for player state management

### For Researchers
- **Historical game data** from a significant indie MMO
- **Social network analysis** of player connections and group dynamics  
- **Economic modeling** of virtual world resource systems
- **Player behavior analysis** through quest and achievement data
- **Game design patterns** from an innovative non-combat MMO

### For Data Scientists
- **Complex XML parsing** examples with nested references
- **Relational data modeling** in NoSQL/document formats
- **Time series analysis** using progression timestamps
- **Network analysis** of social connections and item relationships

## 🔗 Object Relationships

The objects form a complex web of references:

```
PDOADP8FT3V22TI (Player "Apoidea")
├── DDOADR8FT3V22TN (Skills)
├── DDOADS8FT3V22TF (Recipes)  
├── DDOADU8FT3V22TO (Achievements)
├── DDOAEP8FT3V22UD (Counters)
├── DDOAEQ8FT3V22UD (Imagination)
├── BDOAES8FT3V22UJ (Furniture Storage)
│   ├── BHFDL2CS7T230LT (Cabinet)
│   ├── IUV67A83N223H6V (Gem Trophy)
│   └── [140+ furniture items...]
├── Quest System
│   ├── DDOADV8FT3V22T1 (Todo)
│   ├── DDOAE08FT3V22T0 (Done)
│   └── DDOAE18FT3V22TR (Failed)
└── Social Systems
    ├── DDOAEE8FT3V22UN (Buddies)
    ├── DDOAEG8FT3V22UH (Reverse Contacts)
    └── RA512UITCLA22AD (Live Help Group)
```

## 🛠️ File Naming Convention

Glitch used **TSID (Thing String ID)** format for object identification:
- **Format**: `[PREFIX][RANDOM_STRING].xml`
- **Prefixes**: 
  - `P` = Players
  - `D` = Data containers  
  - `B` = Bags/containers
  - `I` = Items/entities
  - `R` = Groups/rooms
  - `L` = Locations (referenced but not included)

## 📚 Getting Started

1. **Start with the player object**: `PDOADP8FT3V22TI.xml`
2. **Follow object references**: Look for `<objref>` tags to find connected objects
3. **Explore data containers**: Check `D*.xml` files for progression and stats
4. **Examine inventory**: Look at `B*.xml` files for items and storage
5. **Study timestamps**: Unix timestamps show progression over time

## 🔍 Notable Files to Explore

- **Largest data files**: `DDOAEQ8FT3V22UD.xml` (2,387 lines of imagination upgrades)
- **Rich inventory**: `BDOAES8FT3V22UJ.xml` (furniture collection)
- **Complex item**: `BHFOF9AMNL13SL0.xml` (main inventory bag)
- **Achievement data**: `DDOADU8FT3V22TO.xml` (complete achievement progress)

## 🏛️ Historical Significance

This data represents more than just game objects—it's a snapshot of an innovative MMO that influenced game design and company culture. Tiny Speck's experience with Glitch directly informed the creation of Slack, one of the most successful communication platforms in history.

The open-sourcing of this data reflects Glitch's community-first values and continues to provide value for developers, researchers, and game design students studying non-traditional MMO mechanics.

---

*For more information about Glitch, visit the [official archived documentation](http://www.glitchthegame.com/) or explore the [open-source client code](https://github.com/tinyspeck/glitch-client).*
