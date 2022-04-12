class CF:

    def calculate_CF(self, concepts, elements):
        concepts_occurrences = {}
        concepts_weights = {}
        total_occurences = 0
        for concept in concepts:
            concepts_occurrences[concept] = 0

        for element in elements:
            for concept in element:
                concepts_occurrences[concept] += 1
                total_occurences += 1

        for concept in concepts:
            concepts_weights[concept] = concepts_occurrences[concept]/total_occurences

        """"# Transform to [0 100] range
        # Code start here
        all_weight = concepts_weights.values()
        max_weight = max(all_weight)
        min_weight = min(all_weight)

        frac = (100 - 0) / (max_weight - min_weight)
        for concept in concepts:
            concepts_weights[concept] = int((concepts_weights[concept] - min_weight) * frac)
        # End"""

        return concepts_weights