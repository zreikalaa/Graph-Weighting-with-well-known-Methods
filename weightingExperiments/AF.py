class AF:

    def calculate_AF(self, concepts, elements):
        concepts_occurrences = {}
        concepts_weights = {}
        total_occurences = len(elements)
        for concept in concepts:
            concepts_occurrences[concept] = 0

        for element in elements:
            for concept in concepts:
                if concept in element:
                    concepts_occurrences[concept] += 1

        for concept in concepts:
            concepts_weights[concept] = concepts_occurrences[concept] / total_occurences



        return concepts_weights