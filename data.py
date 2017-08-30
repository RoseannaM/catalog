from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import ToyStore, Toy, User, Base

engine = create_engine('sqlite:///toystoredb.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# create users
User1 = User(name="Test User 1", email="test1@gmail.com", picture="https://images.pexels.com/photos/354951/pexels-photo-354951.jpeg?w=1260&h=750&auto=compress&cs=tinysrgb")
session.add(User1)
session.commit()

User2 = User(name="Test User 2", email="test2@gmail.com", picture="https://images.pexels.com/photos/9687/pexels-photo.jpg?w=1260&h=750&auto=compress&cs=tinysrgb")
session.add(User2)
session.commit()



#Toys for Toys4All, assigned to test user1
toystore1 = ToyStore(name = "Toys4All", description="This is a great place to buy cute things", address="123 Fake Street Washington", phone_number="2025550186", user_id=User1.id)

session.add(toystore1)
session.commit()


toy1 = Toy(name = "Beach Ball", description = "Large rubber beach ball. Bright blue and red colors", price = "$5.99", color = "Multi", toystore = toystore1, user_id=User1.id)

session.add(toy1)
session.commit()

toy2 = Toy(name = "LEGO Set Castle Magic", description = "LEGO set for building a great stone castle.", price = "$25.50", color = "Multi", toystore = toystore1, user_id=User1.id)

session.add(toy2)
session.commit()

toy3 = Toy(name = "Ultra LEGO Set", description = "The best LEGO set in existence!", price = "$100", color = "Multi", toystore = toystore1, user_id=User1.id)

session.add(toy3)
session.commit()

toy4 = Toy(name = "Plush Chocolate Cake", description = "Fresh baked and made from plushie fabric. Please don't consume.", price = "$9.00", color = "Multi", toystore = toystore1, user_id=User1.id)

session.add(toy4)
session.commit()

toy5 = Toy(name = "Talking Cat", description = "Cute talking cat. Can record and play back sound.", price = "$15.00", color = "Brown", toystore = toystore1, user_id=User1.id)

session.add(toy5)
session.commit()

toy6 = Toy(name = "Talking Dog", description = "Cute talking dog. Can record and play back sound.", price = "$15.00", color = "White", toystore = toystore1, user_id=User1.id)

session.add(toy6)
session.commit()


#Toys for Best Toys, assigned to test user1
toystore2 = ToyStore(name = "Best Toys", description="Well known store that sells unique toys", address="34 Funnyway Carson", phone_number="7755550149", user_id=User1.id)

session.add(toystore2)
session.commit()


toy1 = Toy(name = "Darth Vader Cooking Set", description = "Play time cooking set, but as Darth Vader. Because why not?", price = "$9.00", color = "Multi", toystore = toystore2, user_id=User1.id)

session.add(toy1)
session.commit()

toy2 = Toy(name = "Monopply", description = "A classic boardgame about class warfare and the bourgeois", price = "$25.00", color = "Multi", toystore = toystore2, user_id=User1.id)

session.add(toy2)
session.commit()

toy3 = Toy(name = "Six Sided Dice", description = "Only lands on six because each side is six", price = "$1.00", color = "Blue", toystore = toystore2, user_id=User1.id)

session.add(toy3)
session.commit()

toy4 = Toy(name = "One Sided Dice", description = "This is actually just a marble, but that's between us okay", price = "$1.00", color = "Clear", toystore = toystore2, user_id=User1.id)

session.add(toy4)
session.commit()

toy5 = Toy(name = "Cooking Set", description = "Childrens cooking set. Complete with toy oven, toy food and toy pans.", price = "$55.00", color = "Multi", toystore = toystore2, user_id=User1.id)

session.add(toy5)
session.commit()

toy6 = Toy(name = "Stamp Set", description = "Stamp set with a variety of stamps such as animals, shapes and letters.", price = "$5.00", color = "Multi", toystore = toystore2, user_id=User1.id)

session.add(toy6)
session.commit()

toy7 = Toy(name = "Laughing Cow", description = "Funny laughing cow, comes with dish but spoon sold seperately ", price = "$15.00", color = "Multi", toystore = toystore2, user_id=User1.id)

session.add(toy7)
session.commit()


#Toys for Smart Toys, assigned to test user2
toystore3 = ToyStore(name = "Smart Toys", description="A toystore that specialises in science and learning toys", address="237 Stanely Place Phoenix", phone_number="6025550184", user_id=User2.id)

session.add(toystore3)
session.commit()


toy1 = Toy(name = "Glow in the Dark Stars", description = "Glow in the dark stars in assorted sizes. Can be stuck to many surfaces.", price = "$10.00", color = "Green", toystore = toystore3, user_id=User2.id)

session.add(toy1)
session.commit()

toy2 = Toy(name = "Plastic Tool Set", description = "A plastic tool set complete with hammer, spanner, drill and nails.", price = "$12.00", color = "Multi", toystore = toystore3, user_id=User2.id)

session.add(toy2)
session.commit()

toy3 = Toy(name = "Robot Spider ", description = "Make a robot spider with this set.", price = "$55.00", color = "Black", toystore = toystore3, user_id=User2.id)

session.add(toy3)
session.commit()

toy5 = Toy(name = "Weather Forecasting Kit ", description = "MA kit for weather forecasting.", price = "$20.00", color = "Multi", toystore = toystore3, user_id=User2.id)

session.add(toy5)
session.commit()

toy6 = Toy(name = "Crystal Growing Kit", description = "Grow your own crystals with this set. Contains everything needed.", price = "$10.00", color = "Multi", toystore = toystore3, user_id=User2.id)

session.add(toy6)
session.commit()

toy7 = Toy(name = "Skeleton Anatomy Model", description = "Realistically detailed plastic model skeleton includes a display stand.", price = "$34.00", color = "White", toystore = toystore3, user_id=User2.id)

session.add(toy7)
session.commit()

toy8 = Toy(name = "Magnetic Science Kit", description = "Magnetic Science Kit. Learn about magnets and how they work!.", price = "$20.00", color = "Multi", toystore = toystore3, user_id=User2.id)

session.add(toy8)
session.commit()

print 'Toys added to the database'