import worldapi as wr

# Create a person
i = wr.Person('artem', 16)

# Create a coordinates object
new_position = wr.Coordinates(100, 200, 300)

# Move the person to the new position
wr.World.move(i, new_position)

# Print the new position of the person
print(i.getPoz())