def can_fly(animal):
    birds = ["sparrow", "eagle", "parrot", "penguin", "ostrich"]
    non_flying_bird_exceptions = ["penguin", "ostrich"]
    special_flyers = ["bat"]

    print("Reasoning trace:")
    a = animal.lower()

    if a in birds:
        print(f"1. {animal.capitalize()} is identified as a bird.")
        print("2. Default belief: birds can fly. (Rule R1)")
        if a in non_flying_bird_exceptions:
            print(f"3. But {animal.capitalize()} is a known non-flying bird. (Rule R2)")
            print(f"4. Belief revised: {animal.capitalize()} cannot fly.")
            return False
        else:
            print(f"3. No exception found for {animal.capitalize()}.")
            print(f"4. Belief kept: {animal.capitalize()} can fly.")
            return True

    elif a in special_flyers:
        print(f"1. {animal.capitalize()} is not a bird.")
        print(f"2. But {animal.capitalize()} is known to fly. (Rule R3)")
        print(f"3. Therefore, {animal.capitalize()} can fly.")
        return True

    else:
        print(f"1. {animal.capitalize()} is not in the knowledge base as a bird.")
        print("2. No default rule applies.")
        print("3. Flying ability cannot be determined.")
        return None


animal_name = input("Enter the name of an animal: ")
result = can_fly(animal_name)

if result is True:
    print(f"\nConclusion: {animal_name.capitalize()} can fly.")
elif result is False:
    print(f"\nConclusion: {animal_name.capitalize()} cannot fly.")
else:
    print(f"\nConclusion: Unable to determine if {animal_name.capitalize()} can fly.")
