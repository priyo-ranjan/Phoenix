from cogs.hatching import hatch_creature
from collections import Counter

EGG_TYPE = "mythic"
TESTS = 10000

results = []

for _ in range(TESTS):
    creature = hatch_creature(EGG_TYPE)

    if creature:
        results.append(creature["name"])

counts = Counter(results)

print(f"\nResults for {TESTS:,} {EGG_TYPE} eggs:\n")

for creature, count in counts.most_common():
    percentage = (count / TESTS) * 100
    print(f"{creature:<20} {count:>5}  ({percentage:.2f}%)")