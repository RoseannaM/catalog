# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from database import Toy, Base, ToyStore

# engine = create_engine('sqlite:///toystore.db')

# # Bind the engine to the metadata of the Base class so that the
# # declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# # A DBSession() instance establishes all conversations with the database
# # and represents a "staging zone" for all the objects loaded into the
# # database session object. Any change made against the objects in the
# # session won't be persisted into the database until you call
# # session.commit(). If you're not happy about the changes, you can
# # revert all of them back to the last commit by calling
# # session.rollback()
# session = DBSession()


# # Toy data
# # toystore1 = ToyStore(name="Best Toys", description="Well known store that sells unique toys", address="34 Funnyway Carson", phone_number="7755550149")

# # session.add(toystore1)
# # session.commit()

# toystore = session.query(ToyStore).filter_by(name='Toys4All').one()


# toy11 = Toy(name="Stamp Set", description="Stamp set with a variety of stamps such as animals, shapes and letters.",
#            price="$5.00", color="Green", toystore=toystore)

# session.add(toy11)
# session.commit()


# # toy3 = Toy(name="Ultra LEGO Set", description="The best LEGO set in existence!",
# #            price="$100.00", color="Multi", toystore=toystore1)

# # session.add(toy3)
# # session.commit()

# # toy4 = Toy(name="Plush Chocolate Cake", description="fresh baked and made from plushie fabric. Please don't consume.",
# #            price="$9.00", color="Multi", toystore=toystore1)

# # session.add(toy4)
# # session.commit()

# # toy5 = Toy(name="Giant Panda Plush", description="huge panda soft toy. Great present.",
# #            price="$50.00", color="Multi", toystore=toystore1)

# # session.add(toy5)
# # session.commit()

# # toy6 = Toy(name="Darth Vader Cooking Set", description="Play time cooking set, but as Darth Vader. Because why not?",
# #            price="$9.00", color="Multi", toystore=toystore1)

# # session.add(toy6)
# # session.commit()

# # toy7 = Toy(name="Monopply", description="A classic boardgame about class warfare and the bourgeois",
# #            price="$20.00", color="Multi", toystore=toystore1)

# # session.add(toy7)
# # session.commit()

# # toy8 = Toy(name="Six Sided Dice", description="Only lands on six because each side is six",
# #            price="$1.00", color="blue", toystore=toystore1)

# # session.add(toy8)
# # session.commit()

# # toy9 = Toy(name="One Sided Dice", description="This is actually just a marble, but that's between us okay",
# #            price="$1.00", color="clear", toystore=toystore1)

# # session.add(toy9)
# # session.commit()


# print "added toys"