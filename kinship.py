"""Find the relationship between 2 individuals in a family tree"""

from argparse import ArgumentParser
import json
import relationships
import sys

class Person:
   """Represents a person in the family.
   
   Attributes:
      name (str): name of person
      gender (str): gender of person
      parents (list): parents of person
      spouse (str): spouse of person
   """
   def __init__(self, name, gender):
      """set attributes of Person

      Args:
          name (str): name of the person
          gender (str): gender of the person
          
      Side effects:
         self.parents and self.spuse may be changed depending on the person 
         and relationship.
      """
      self.name = name
      self.gender = gender
      self.parents = []
      self.spouse = None
      
   def add_parent(self, parent):
      """Adds parents to list of parents of the person.

      Args:
          parent (str): name of parent
          
      Side effects:
         adds parent(s) to list of self.parents
      """
      self.parents.append(parent)
   
   def set_spouse(self, spouse):
      """Sets spouse for person, if applicable.

      Args:
          spouse (str): spouse of person
      """
      self.spouse = spouse
   
   def connections(self):
      """identify connections to relatives who might be LCR.

      Returns:
          cdict: dictionary of connections
          
      Side effects:
         changing to cdict dictionary and queue as connections are being made.
      """
      cdict = {self:""}
      queue = [self]
      while len(queue) > 0:
         person = queue.pop(0)
         personpath = cdict[person]
         for parent in person.parents:
            if parent not in cdict:
               cdict[parent]= personpath + "P"
               queue.append(parent)
         if person.spouse and "S" not in personpath:
               spouse = person.spouse
               if spouse not in cdict:
                  cdict[spouse] = personpath + "S"
                  queue.append(spouse)
      return cdict
   
   def relation_to(self, relation):
      """determines relationship of two individuals.

      Args:
          relation (str): the person being connected/finding relation to

      Returns:
          None: if no shared connection
          str: kinship term or if they are not directly related
      """
      connection1 = self.connections()
      connection2 = relation.connections()
      shared = set(connection1.keys()) & set(connection2.keys())
      if not shared:
         return None
      combined_paths = []
      for person in shared:
         path1 = connection1[person]
         path2 = connection2[person]
         paths = f"{path1}:{path2}"
         combined_paths.append(paths)
      lcr_path = min(combined_paths)
      gender = self.gender
      if lcr_path in relationships.relationships:
         return relationships.relationships[lcr_path][gender]
      else:
         return "distant relative"
      
      
class Family:
   """Keeps track of Person instances made.
   
   Attributes:
      self.people (dict): dictionary of people relations
   """
   def __init__(self, dict1):
      """set attributes of Family

      Args:
          dict1 (dictionary): dictionary of family characteristics
          
      Side effects:
         can change value of parent and spouse through add_parent or add_spouse.
      """
      self.people = {}
      individuals = dict1["individuals"]
      parents = dict1["parents"]
      couples = dict1["couples"]

      for name, gender in individuals.items():
         self.people[name] = Person(name, gender)

      for person_name, parent_names in parents.items():
         person = self.people[person_name]
         for parent_name in parent_names:
            parent = self.people[parent_name]
            person.add_parent(parent)

      for couple in couples:
         person1 = self.people[couple[0]]
         person2 = self.people[couple[1]]
         person1.set_spouse(person2)
         person2.set_spouse(person1)

   def relation(self, name1, name2):
      """finds kinship term or lack thereof

      Args:
          name1 (str): first persons name
          name2 (str): second persons name

      Returns:
          str: person of Persons relation_to method
      """
      person1 = self.people.get(name1)
      person2 = self.people.get(name2)
      return person1.relation_to(person2)


def main(filepath, name1, name2):
   """opens file and sets output

   Args:
       filepath (str): filepath of relationships
       name1 (str): name of a person in the relationship file
       name2 (str): name of second person in relationship file
       
   Side effects:
      prints the relationship (or lackthereof) of the two individuals.
   """
   with open(filepath, "r") as f:
      familydata = json.load(f)
   family = Family(familydata)
   relationship = family.relation(name1, name2)
   if relationship == None:
        print(f"{name1} is not related to {name2}")
   else:
        print(f"{name1} is {name2}'s {relationship}")
   

def parse_args(arglist):
   """parses the arguments and code given in our main() function

   Args:
       arglist (str): list of arguments to parse

   Returns:
       str: parsed arguments from those given
   """
   parser = ArgumentParser()
   parser.add_argument("filepath", help = "Provide filepath")
   parser.add_argument("name1", help = "Provide name 1")
   parser.add_argument("name2", help = "Provide name 2")
   return parser.parse_args(arglist)


if __name__ == "__main__":
   args = parse_args(sys.argv[1:])
   main(args.filepath, args.name1, args.name2)