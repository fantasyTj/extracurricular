# Calculate the accuracy of a baseline that simply predicts "London" for every
#   example in the dev set.
# Hint: Make use of existing code.
# Your solution here should only be a few lines.
import utils

filepath = 'birth_dev.tsv'
with open(filepath, encoding='utf-8') as fin:
    length = len([x for x in fin])
    predicted_places = ['London'] * length
    total, correct = utils.evaluate_places(filepath, predicted_places)
    acc = correct/total
    print("Reference acc(all predicted 'London'): {}".format(acc))
