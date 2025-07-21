# Developer Documentation - Glitch Object System

This document provides technical details for developers working with the Glitch game object data format and structure.

## 🏗️ Object Schema Structure

### Core Object Format

All Glitch objects follow this basic XML structure:

```xml
<game_object tsid="[OBJECT_ID]" ts="[TIMESTAMP]" label="[DISPLAY_NAME]" 
             class_tsid="[OBJECT_CLASS]" [additional_attributes]>
    <object id="dynamic">
        <!-- Dynamic properties and nested objects -->
    </object>
    <int id="x">-888888888</int>  <!-- X coordinate, -888888888 = not placed -->
    <int id="y">-888888888</int>  <!-- Y coordinate -->
    <!-- Static properties -->
</game_object>
```

### Key Attributes

- **`tsid`**: Thing String ID - unique identifier across the game world
- **`ts`**: Timestamp in milliseconds (Unix epoch * 1000)
- **`label`**: Human-readable display name
- **`class_tsid`**: Object class/type identifier
- **`container`**: TSID of containing object (for nested objects)
- **`upd_gs`**: Game server that last updated this object

## 📋 Object Classes Documented

### Player Objects (`class_tsid="human"`)

**Primary Object**: `PDOADP8FT3V22TI` - Player "Apoidea"

**Key Properties**:
```xml
<object id="metabolics">
    <prop id="energy" name="energy" top="900">893</prop>
    <prop id="mood" name="mood" top="900">872</prop>
    <int id="tank">900</int>
</object>
```

**Avatar Customization** (`a2` object):
- Clothing slots: hat, coat, shirt, pants, dress, skirt, shoes
- Physical features: eyes, ears
- Numeric IDs reference game asset catalog

**Critical References**:
- `skills`: Link to skill progression data
- `recipes`: Learned crafting recipes
- `achievements`: Achievement progress tracking
- `quests`: Quest state management
- `friends`: Social network connections

### Data Containers (`class_tsid="dc"`)

Generic containers for structured game data:

#### Skills Container (`DDOADR8FT3V22TN`)
```xml
<object id="skills">
    <int id="animalkinship_1">1336771091</int>  <!-- Unix timestamp when learned -->
    <int id="ezcooking_1">1336771806</int>
    <int id="mining_1">1337043000</int>
    <!-- Additional skill entries -->
</object>
```

**Skill Naming Convention**: `[skill_name]_[tier]`
- Examples: `mining_1`, `mining_2`, `meditativearts_1`
- Timestamps indicate when skill was learned
- Progressive unlocking system (tier 1 → tier 2 → etc.)

#### Recipe Container (`DDOADS8FT3V22TF`)
```xml
<object id="recipes">
    <int id="12">1336771806</int>    <!-- Recipe ID 12 learned at timestamp -->
    <int id="14">1336771806</int>
    <int id="97">1336771806</int>
    <!-- Numeric recipe IDs with learning timestamps -->
</object>
```

#### Achievement Container (`DDOADU8FT3V22TO`)
```xml
<object id="achievements">
    <int id="pennypincher">1336771076</int>
    <int id="junior_ok_explorer">1336771685</int>
    <int id="big_spender">1336771766</int>
    <!-- Achievement keys with completion timestamps -->
</object>
```

**Achievement Categories**:
- **Exploration**: `junior_ok_explorer`, `senior_ok_explorer`, `rambler_*`
- **Economic**: `pennypincher`, `big_spender`, `moneybags`
- **Social**: Various interaction-based achievements
- **Collection**: Item and resource gathering achievements
- **Skill**: Progression and mastery achievements

#### Counter Container (`DDOAEP8FT3V22UD`)
```xml
<object id="counters">
    <object id="items_collected">
        <int id="grain">727</int>           <!-- 727 grain collected total -->
        <int id="plain_bubble">364</int>    <!-- 364 bubbles collected -->
        <int id="meat">211</int>            <!-- 211 meat items -->
        <!-- Comprehensive collection tracking -->
    </object>
</object>
```

### Bag Objects (`class_tsid="bag_*"`)

Container objects for inventory management:

#### Furniture Bag (`BDOAES8FT3V22UJ`)
```xml
<objrefs id="items">
    <objref tsid="BHFDL2CS7T230LT" label="Cabinet"/>
    <objref tsid="IUV67A83N223H6V" label="Gem Trophy"/>
    <!-- Array of item references -->
</objrefs>
```

**Key Properties**:
- `container`: Parent object (usually player)
- `x`, `y`: Coordinates (-888888888 = not placed in world)
- `items`: Array of contained object references

### Item Objects (`class_tsid="[item_type]"`)

Individual game entities and objects:

#### Tree Objects (`class_tsid="trant_bubble"`)
```xml
<object id="instanceProps">
    <int id="health">10</int>           <!-- Current health -->
    <int id="maturity">10</int>         <!-- Growth stage -->
    <int id="fruitCount">263</int>      <!-- Available fruit -->
    <int id="fruitCapacity">288</int>   <!-- Maximum fruit capacity -->
    <int id="cultivation_wear">2064</int> <!-- Tool wear from cultivation -->
</object>
```

### Group Objects (`class_tsid="group"`)

Social and organizational containers:

```xml
<object id="chat_roster">
    <objref id="PIF1SSTQT4T70" tsid="PIF1SSTQT4T70" label="jdawg"/>
    <objref id="PIF5NL12S3D1BH3" tsid="PIF5NL12S3D1BH3" label="Jade"/>
</object>
```

## 🔗 Reference Resolution

### Object References (`<objref>`)

Objects reference each other using:
```xml
<objref id="container" tsid="PDOADP8FT3V22TI" label="Apoidea"/>
```

To resolve references:
1. Find the target object file: `[tsid].xml`
2. Load and parse the referenced object
3. Follow nested references as needed

### Reference Arrays (`<objrefs>`)

Collections of object references:
```xml
<objrefs id="items">
    <objref tsid="OBJECT_1" label="Item 1"/>
    <objref tsid="OBJECT_2" label="Item 2"/>
</objrefs>
```

## 🕐 Timestamp Analysis

All timestamps are in **milliseconds since Unix epoch**:

```javascript
// Convert to readable date
const timestamp = 1336771091;
const date = new Date(timestamp * 1000); // Multiply by 1000 for milliseconds
console.log(date); // May 11, 2012
```

**Timeline Context**:
- Game launch: September 2011
- Data snapshot: December 2012
- Timestamps track player progression over ~1.3 years

## 🛠️ Development Tools & Utilities

### XML Parsing Examples

#### Python
```python
import xml.etree.ElementTree as ET

def parse_glitch_object(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    tsid = root.get('tsid')
    label = root.get('label')
    class_type = root.get('class_tsid')
    
    return {
        'tsid': tsid,
        'label': label,
        'class': class_type,
        'data': parse_dynamic_object(root.find('.//object[@id="dynamic"]'))
    }

def parse_dynamic_object(obj):
    if obj is None:
        return {}
    
    result = {}
    for child in obj:
        if child.tag == 'int':
            result[child.get('id')] = int(child.text)
        elif child.tag == 'str':
            result[child.get('id')] = child.text
        elif child.tag == 'object':
            result[child.get('id')] = parse_dynamic_object(child)
    
    return result
```

#### JavaScript/Node.js
```javascript
const fs = require('fs');
const xml2js = require('xml2js');

async function parseGlitchObject(filename) {
    const xml = fs.readFileSync(filename, 'utf8');
    const parser = new xml2js.Parser();
    const result = await parser.parseStringPromise(xml);
    
    const obj = result.game_object.$;
    return {
        tsid: obj.tsid,
        label: obj.label,
        class: obj.class_tsid,
        timestamp: parseInt(obj.ts),
        data: result.game_object
    };
}
```

### Reference Graph Analysis

Build object relationship graphs:

```python
def build_reference_graph(object_files):
    graph = {}
    
    for filename in object_files:
        obj = parse_glitch_object(filename)
        graph[obj['tsid']] = {
            'label': obj['label'],
            'class': obj['class'],
            'references': extract_references(obj['data'])
        }
    
    return graph

def extract_references(data):
    refs = []
    
    def find_objrefs(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'objref' and isinstance(value, list):
                    for ref in value:
                        if '$' in ref and 'tsid' in ref['$']:
                            refs.append(ref['$']['tsid'])
                elif isinstance(value, (dict, list)):
                    find_objrefs(value)
    
    find_objrefs(data)
    return refs
```

## 🔍 Analysis Patterns

### Progression Tracking

Track player progression through timestamps:

```python
def analyze_progression(skills_data):
    skill_timeline = []
    
    for skill_id, timestamp in skills_data['skills'].items():
        skill_timeline.append({
            'skill': skill_id,
            'timestamp': timestamp,
            'date': datetime.fromtimestamp(timestamp)
        })
    
    return sorted(skill_timeline, key=lambda x: x['timestamp'])
```

### Collection Analysis

Analyze collection patterns:

```python
def analyze_collections(counters_data):
    items = counters_data['counters']['items_collected']
    
    total_items = sum(items.values())
    most_collected = max(items.items(), key=lambda x: x[1])
    
    return {
        'total_collected': total_items,
        'unique_types': len(items),
        'most_collected': most_collected,
        'distribution': sorted(items.items(), key=lambda x: x[1], reverse=True)
    }
```

## 🧪 Testing & Validation

### Object Integrity Checks

```python
def validate_object_references(objects_dir):
    errors = []
    object_ids = set()
    references = set()
    
    # Collect all object IDs
    for filename in os.listdir(objects_dir):
        if filename.endswith('.xml'):
            tsid = filename[:-4]  # Remove .xml extension
            object_ids.add(tsid)
    
    # Check references
    for filename in os.listdir(objects_dir):
        if filename.endswith('.xml'):
            obj = parse_glitch_object(os.path.join(objects_dir, filename))
            refs = extract_references(obj['data'])
            
            for ref in refs:
                if ref not in object_ids:
                    errors.append(f"Missing reference: {ref} from {obj['tsid']}")
    
    return errors
```

## 📊 Performance Considerations

### Large File Handling

Some objects (like `DDOAEQ8FT3V22UD.xml` at 2,387 lines) require efficient parsing:

- Use streaming XML parsers for large files
- Implement lazy loading for reference resolution  
- Cache parsed objects to avoid re-parsing
- Consider extracting specific data rather than loading entire objects

### Memory Management

```python
# Efficient partial loading
def load_object_metadata(filename):
    with open(filename, 'r') as f:
        # Read only the first line for basic attributes
        first_line = f.readline()
        # Parse just the game_object tag attributes
        # Return lightweight metadata object
```

## 🔧 Common Development Tasks

### Finding Related Objects

```python
def find_player_inventory(player_tsid):
    player = parse_glitch_object(f"{player_tsid}.xml")
    inventory_refs = []
    
    # Extract bag references from player object
    # Follow container references
    # Build complete inventory tree
    
    return inventory_refs
```

### Skill Tree Analysis

```python
def build_skill_tree(skills_data):
    skills = skills_data['skills']
    tree = {}
    
    for skill_id, timestamp in skills.items():
        skill_name, tier = skill_id.rsplit('_', 1)
        if skill_name not in tree:
            tree[skill_name] = {}
        tree[skill_name][int(tier)] = timestamp
    
    return tree
```

### Achievement Progress

```python
def calculate_achievement_completion(achievements_data):
    completed = len(achievements_data['achievements'])
    # Compare against known total achievement count
    total_known = 150  # Approximate based on game documentation
    
    return {
        'completed': completed,
        'completion_rate': completed / total_known,
        'recent_achievements': get_recent_achievements(achievements_data)
    }
```

---

This documentation provides the foundation for working with Glitch object data. The format is complex but well-structured, offering rich insights into MMO game design and player behavior patterns.