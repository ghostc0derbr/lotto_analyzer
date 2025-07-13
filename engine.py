import random
import feedback_db
from config import *

class CalculationEngine:
    def __init__(self, user_inputs, active_filters):
        self.inputs = user_inputs
        self.filters = active_filters
        self.all_numbers = set(range(1, TOTAL_NUMBERS + 1))
        self.feedback_weights = feedback_db.get_feedback_weights()
        print(f"Pesos de feedback carregados: {self.feedback_weights}")

    def get_number_properties(self, number):
        props = {}
        for color, numbers_in_color in CORES.items():
            if number in numbers_in_color: props['color'] = color
        props['parity'] = 'Ímpar' if number % 2 != 0 else 'Par'
        props['hilo'] = 'Lo' if number <= HI_LO_SPLIT_POINT else 'Hi'
        props['is_fibonacci'] = number in FIBONACCI_NUMBERS
        props['is_prime'] = number in PRIME_NUMBERS
        props['is_square'] = number in SQUARE_NUMBERS
        return props

    def get_combo_properties_for_feedback(self, combo):
        props = {}
        props['prime_count'] = sum(1 for n in combo if self.get_number_properties(n)['is_prime'])
        props['fibonacci_count'] = sum(1 for n in combo if self.get_number_properties(n)['is_fibonacci'])
        even_count = sum(1 for n in combo if n % 2 == 0)
        props['parity_pattern'] = f"{even_count}P/{NUM_TO_PICK - even_count}I"
        return props

    def generate_5_number_suggestions(self, count=5):
        hot=self.inputs['general_hot']; cold=self.inputs['general_cold']; eligible_pool=list(self.all_numbers-cold)
        if len(eligible_pool) < NUM_TO_PICK: raise ValueError("Números elegíveis insuficientes.")
        candidate_combos = {tuple(sorted(random.sample(eligible_pool, NUM_TO_PICK))) for _ in range(10000)}
        
        scored_combos = []
        for combo in candidate_combos:
            score = 0
            score += len(set(combo) & hot) * 20
            for i, num in enumerate(combo):
                pos = i + 1; props = self.get_number_properties(num); stats = self.inputs['positional_stats'][pos]
                score += stats['colors'].get(props['color'], 0)/10 + stats['odd_even'].get(props['parity'], 0)/10 + stats['hi_lo'].get(props['hilo'], 0)/10
            if self.filters.get('use_fibonacci'): score += sum(1 for n in combo if self.get_number_properties(n)['is_fibonacci']) * 5
            if self.filters.get('use_primes'): score += sum(1 for n in combo if self.get_number_properties(n)['is_prime']) * 5
            if self.filters.get('use_squares'): score += sum(1 for n in combo if self.get_number_properties(n)['is_square']) * 5
            if self.filters.get('use_sum') and 75 <= sum(combo) <= 115: score += 10
            
            combo_props_for_feedback = self.get_combo_properties_for_feedback(combo)
            for key, value in combo_props_for_feedback.items():
                feedback_key = f"{key}_{value}"
                if feedback_key in self.feedback_weights:
                    score += self.feedback_weights[feedback_key] * 2
            
            scored_combos.append({'combo': list(combo), 'score': score})
        
        sorted_combos = sorted(scored_combos, key=lambda x: x['score'], reverse=True)
        final_suggestions = [];
        if not sorted_combos: return []
        final_suggestions.append(sorted_combos.pop(0)['combo'])
        while len(final_suggestions) < count and sorted_combos:
            best_candidate = None; max_diversity_score = -1
            for candidate in sorted_combos[:200]:
                min_overlap = float('inf')
                for suggestion in final_suggestions:
                    overlap = len(set(candidate['combo']) & set(suggestion))
                    if overlap < min_overlap: min_overlap = overlap
                diversity_score = (NUM_TO_PICK - min_overlap)
                if diversity_score > max_diversity_score: max_diversity_score = diversity_score; best_candidate = candidate
            if best_candidate: final_suggestions.append(best_candidate['combo']); sorted_combos.remove(best_candidate)
            else: break
        return final_suggestions

    def generate_1st_number_suggestions(self, count=10):
        scores = {}
        stats1 = self.inputs['first_number_stats']; pos1_stats = self.inputs['positional_stats'][1]
        for num in self.all_numbers:
            score = 0; props = self.get_number_properties(num)
            score += stats1['hot_frequencies'].get(num, 0) * 2
            score += pos1_stats['colors'].get(props['color'],0)/10 + pos1_stats['odd_even'].get(props['parity'],0)/10 + pos1_stats['hi_lo'].get(props['hilo'],0)/10
            if self.filters.get('use_fibonacci') and props['is_fibonacci']: score += 2
            if self.filters.get('use_primes') and props['is_prime']: score += 2
            if self.filters.get('use_squares') and props['is_square']: score += 2
            scores[num] = round(score, 2)
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:count]