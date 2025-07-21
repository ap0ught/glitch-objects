#!/usr/bin/env python3
"""
Glitch Object Analyzer
A demonstration tool for exploring Glitch game object data.

Usage:
    python analyze_objects.py [command] [options]

Commands:
    summary     - Show overview of all objects
    player      - Analyze player object details  
    inventory   - Show inventory contents
    progression - Show skill/achievement progression
    references  - Map object relationships

Example:
    python analyze_objects.py summary
    python analyze_objects.py player PDOADP8FT3V22TI
    python analyze_objects.py progression --skills
"""

import xml.etree.ElementTree as ET
import os
import sys
from datetime import datetime
from collections import defaultdict

class GlitchObjectAnalyzer:
    
    def __init__(self, data_dir="."):
        self.data_dir = data_dir
        self.objects = {}
        self.load_objects()
    
    def load_objects(self):
        """Load all XML objects from directory"""
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.xml'):
                try:
                    tsid = filename[:-4]
                    self.objects[tsid] = self.parse_object(filename)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def parse_object(self, filename):
        """Parse a single XML object file"""
        tree = ET.parse(os.path.join(self.data_dir, filename))
        root = tree.getroot()
        
        return {
            'tsid': root.get('tsid'),
            'label': root.get('label', 'Unknown'),
            'class': root.get('class_tsid', 'unknown'),
            'timestamp': int(root.get('ts', 0)),
            'container': root.get('container'),
            'xml': root
        }
    
    def get_object_counts(self):
        """Count objects by type"""
        counts = defaultdict(int)
        for obj in self.objects.values():
            class_type = obj['class']
            if class_type.startswith('bag_'):
                counts['Bags'] += 1
            elif class_type == 'dc':
                counts['Data Containers'] += 1
            elif class_type == 'human':
                counts['Players'] += 1
            elif class_type == 'group':
                counts['Groups'] += 1
            elif class_type.startswith('trant_'):
                counts['Trees/Plants'] += 1
            else:
                counts['Items'] += 1
        return dict(counts)
    
    def analyze_player(self, player_tsid):
        """Analyze player object in detail"""
        if player_tsid not in self.objects:
            return f"Player {player_tsid} not found"
        
        player = self.objects[player_tsid]
        xml = player['xml']
        
        # Extract metabolics
        metabolics = xml.find('.//object[@id="metabolics"]')
        energy = mood = tank = "Unknown"
        
        if metabolics is not None:
            energy_prop = metabolics.find('.//prop[@id="energy"]')
            mood_prop = metabolics.find('.//prop[@id="mood"]')
            tank_elem = metabolics.find('.//int[@id="tank"]')
            
            if energy_prop is not None:
                energy = f"{energy_prop.text}/{energy_prop.get('top')}"
            if mood_prop is not None:
                mood = f"{mood_prop.text}/{mood_prop.get('top')}"
            if tank_elem is not None:
                tank = tank_elem.text
        
        # Count references
        references = xml.findall('.//objref')
        ref_count = len(references)
        
        return {
            'name': player['label'],
            'tsid': player_tsid,
            'energy': energy,
            'mood': mood,
            'tank': tank,
            'references': ref_count,
            'last_update': datetime.fromtimestamp(player['timestamp'] / 1000)
        }
    
    def find_containers(self, container_tsid):
        """Find all objects contained within a specific container"""
        contained = []
        for obj in self.objects.values():
            if obj['container'] == container_tsid:
                contained.append(obj)
        return contained
    
    def analyze_skills(self, skills_tsid):
        """Analyze skill progression"""
        if skills_tsid not in self.objects:
            return "Skills object not found"
        
        skills_obj = self.objects[skills_tsid]
        skills_elem = skills_obj['xml'].find('.//object[@id="skills"]')
        
        if skills_elem is None:
            return "No skills data found"
        
        skills = []
        for skill in skills_elem:
            if skill.tag == 'int':
                skill_id = skill.get('id')
                timestamp = int(skill.text)
                date = datetime.fromtimestamp(timestamp)
                skills.append({
                    'skill': skill_id,
                    'learned': date,
                    'timestamp': timestamp
                })
        
        # Sort by learning date
        skills.sort(key=lambda x: x['timestamp'])
        return skills
    
    def analyze_achievements(self, achievements_tsid):
        """Analyze achievement progress"""
        if achievements_tsid not in self.objects:
            return "Achievements object not found"
        
        ach_obj = self.objects[achievements_tsid]
        ach_elem = ach_obj['xml'].find('.//object[@id="achievements"]')
        
        if ach_elem is None:
            return "No achievements data found"
        
        achievements = []
        for ach in ach_elem:
            if ach.tag == 'int':
                ach_id = ach.get('id')
                timestamp = int(ach.text)
                date = datetime.fromtimestamp(timestamp)
                achievements.append({
                    'achievement': ach_id,
                    'completed': date,
                    'timestamp': timestamp
                })
        
        achievements.sort(key=lambda x: x['timestamp'])
        return achievements

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    analyzer = GlitchObjectAnalyzer()
    command = sys.argv[1]
    
    if command == 'summary':
        print("=== Glitch Objects Summary ===")
        print(f"Total objects: {len(analyzer.objects)}")
        print("\nObject type breakdown:")
        counts = analyzer.get_object_counts()
        for obj_type, count in sorted(counts.items()):
            print(f"  {obj_type}: {count}")
        
        # Find the player object
        players = [obj for obj in analyzer.objects.values() if obj['class'] == 'human']
        if players:
            player = players[0]
            print(f"\nMain player: {player['label']} ({player['tsid']})")
            
            # Show connected objects
            contained = analyzer.find_containers(player['tsid'])
            print(f"Connected objects: {len(contained)}")
            for obj in contained[:5]:  # Show first 5
                print(f"  - {obj['label']} ({obj['class']})")
            if len(contained) > 5:
                print(f"  ... and {len(contained) - 5} more")
    
    elif command == 'player':
        if len(sys.argv) < 3:
            print("Usage: analyze_objects.py player <TSID>")
            return
        
        player_tsid = sys.argv[2]
        result = analyzer.analyze_player(player_tsid)
        
        if isinstance(result, dict):
            print(f"=== Player Analysis: {result['name']} ===")
            print(f"TSID: {result['tsid']}")
            print(f"Energy: {result['energy']}")
            print(f"Mood: {result['mood']}")
            print(f"Tank: {result['tank']}")
            print(f"Connected objects: {result['references']}")
            print(f"Last update: {result['last_update']}")
        else:
            print(result)
    
    elif command == 'progression':
        # Find skills and achievements for the main player
        players = [obj for obj in analyzer.objects.values() if obj['class'] == 'human']
        if not players:
            print("No player object found")
            return
        
        player = players[0]
        player_xml = player['xml']
        
        # Find skills reference
        skills_ref = player_xml.find('.//objref[@id="skills"]')
        if skills_ref is not None:
            skills_tsid = skills_ref.get('tsid')
            skills = analyzer.analyze_skills(skills_tsid)
            
            print("=== Skill Progression ===")
            if isinstance(skills, list):
                print(f"Total skills learned: {len(skills)}")
                print("Recent skills:")
                for skill in skills[-5:]:  # Last 5 skills
                    print(f"  {skill['learned'].strftime('%Y-%m-%d')}: {skill['skill']}")
            else:
                print(skills)
        
        # Find achievements reference  
        ach_ref = player_xml.find('.//objref[@id="achievements"]')
        if ach_ref is not None:
            ach_tsid = ach_ref.get('tsid')
            achievements = analyzer.analyze_achievements(ach_tsid)
            
            print("\n=== Achievement Progress ===")
            if isinstance(achievements, list):
                print(f"Total achievements: {len(achievements)}")
                print("Recent achievements:")
                for ach in achievements[-5:]:  # Last 5 achievements
                    print(f"  {ach['completed'].strftime('%Y-%m-%d')}: {ach['achievement']}")
            else:
                print(achievements)
    
    elif command == 'inventory':
        # Find bags for the main player
        players = [obj for obj in analyzer.objects.values() if obj['class'] == 'human']
        if not players:
            print("No player object found")
            return
        
        player = players[0]
        bags = analyzer.find_containers(player['tsid'])
        bag_objects = [obj for obj in bags if obj['class'].startswith('bag_')]
        
        print("=== Inventory Analysis ===")
        print(f"Total bags: {len(bag_objects)}")
        
        for bag in bag_objects:
            print(f"\n{bag['label']} ({bag['class']}):")
            
            # Count items in this bag
            bag_xml = bag['xml']
            items = bag_xml.findall('.//objref')
            print(f"  Items: {len(items)}")
            
            # Show some item names
            for item in items[:3]:  # First 3 items
                print(f"    - {item.get('label')}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == '__main__':
    main()