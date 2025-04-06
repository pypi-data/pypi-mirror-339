from dataclasses import dataclass, field
from collections import Counter
import numpy as np
import itertools
from itertools import combinations
from math import comb


@dataclass
class PlayingCardsR1:
    seen_cards: list[int]
    _theo: float = field(init=False)
    
    
    def __post_init__(self) -> None:
        self._calculate_theo()
    
        
    def __repr__(self) -> str:
        print(f"Theoretical value {round(self._theo, 3)}")
        return ""


    def _calculate_theo(self) -> None:
        deck = list(range(1,14))*4
        for card in self.seen_cards:
            deck.remove(card)
        self._theo = np.mean(deck) * (10 - len(self.seen_cards)) + sum(self.seen_cards)

        
    def add_card(self, card: int) -> None:
        self.seen_cards.append(card)
        self._calculate_theo()
    



@dataclass
class PlayingCardsR2:
    seen_cards_1: list[int]
    seen_cards_2: list[int]
    _theo_sum_1: float = field(init=False)
    _theo_sum_2: float = field(init=False)
    _theo_abs_diff: float = field(init=False)
    
    
    def __post_init__(self) -> None:
        self._calculate_theos()
    
    
    def __repr__(self) -> str:
        print(f"Theo Sum Deck 1: {round(self._theo_sum_1, 3)}")
        print(f"Theo Sum Deck 2: {round(self._theo_sum_2, 3)}")
        print(f"Theo Abs Diff: {round(self._theo_abs_diff, 3)}")
        return ""
    
    
    def _calculate_theos(self) -> None:
        self._theo_sum_1 = self._compute_expected_sum(self.seen_cards_1)
        self._theo_sum_2 = self._compute_expected_sum(self.seen_cards_2)
        self._theo_abs_diff = self._expected_abs_diff()
    
    
    def _compute_expected_sum(self, seen: list[int]) -> float:
        full_deck = [i for i in range(1, 14)] * 4
        for card in seen:
            full_deck.remove(card)
        remaining = 10 - len(seen)
        return np.mean(full_deck) * remaining + sum(seen)
    
    
    def _get_sum_distribution(self, seen: list[int], hand_size: int = 10) -> dict:
        full_deck = [i for i in range(1, 14)] * 4
        for card in seen:
            full_deck.remove(card)
        remaining = hand_size - len(seen)
        
        count = Counter()
        count[0] = 1

        for card in full_deck:
            new_count = Counter()
            for total, ways in count.items():
                new_count[total + card] += ways
            count += new_count
            
        valid = Counter()
        for combo in itertools.combinations(full_deck, remaining):
            valid[sum(combo)] += 1
        
        total = sum(valid.values())
        return {k + sum(seen): v / total for k, v in valid.items()}
    
    
    def _expected_abs_diff(self) -> float:
        dist1 = self._get_sum_distribution(self.seen_cards_1)
        dist2 = self._get_sum_distribution(self.seen_cards_2)

        vals1 = np.array(list(dist1.keys()))
        vals2 = np.array(list(dist2.keys()))
        probs1 = np.array(list(dist1.values()))
        probs2 = np.array(list(dist2.values()))

        x, y = np.meshgrid(vals1, vals2)
        px, py = np.meshgrid(probs1, probs2)
        return np.sum(np.abs(x - y) * (px * py))
        
    
    
@dataclass
class PlayingCardsR3:
    clubs: list[int]
    spades: list[int]
    diamonds: list[int]
    hearts: list[int]
    
    _theo_sum: float = field(init=False)
    _theo_rb_prod: float = field(init=False)
    _theo_suit_prod: float = field(init=False)
    
    def __post_init__(self) -> None:
        self._calculate_theos()
        
    def __repr__(self) -> str:
        print(f"Theoretical value: {round(self._theo_sum, 3)}")
        print(f"Theoretical red-black product: {round(self._theo_rb_prod, 3)}")
        print(f"Theoretical suit product: {round(self._theo_suit_prod, 3)}")
        return ""
    
    def _calculate_theos(self) -> None:
        all_cards = self.clubs + self.spades + self.diamonds + self.hearts
        self._theo_sum = PlayingCardsR1(all_cards)._theo
        self._theo_rb_prod = self._expected_red_black_product()
        self._theo_suit_prod = self._expected_suit_frequency_product()
    
    def _build_deck(self):
        suits = ['C', 'S', 'D', 'H']
        deck = []
        for s in suits:
            for v in range(1, 14):
                deck.append((s, v))
        return deck

    def _expected_red_black_product(self):
        seen_red = [('D', v) for v in self.diamonds] + [('H', v) for v in self.hearts]
        seen_black = [('C', v) for v in self.clubs] + [('S', v) for v in self.spades]
        full_deck = self._build_deck()
        seen_cards = seen_red + seen_black
        remaining_deck = [card for card in full_deck if card not in seen_cards]
        n = 10 - len(seen_cards)

        red_suits, black_suits = {'D', 'H'}, {'C', 'S'}
        remaining_reds = [v for s, v in remaining_deck if s in red_suits]
        remaining_blacks = [v for s, v in remaining_deck if s in black_suits]

        sum_seen_red, sum_seen_black = sum(v for _, v in seen_red), sum(v for _, v in seen_black)

        red_dist = Counter()
        for k in range(min(n, len(remaining_reds)) + 1):
            for red_combo in combinations(remaining_reds, k):
                red_sum = sum(red_combo)
                remaining_k = n - k
                if remaining_k > len(remaining_blacks):
                    continue
                for black_combo in combinations(remaining_blacks, remaining_k):
                    black_sum = sum(black_combo)
                    red_dist[(red_sum, black_sum)] += 1

        total = sum(red_dist.values())
        ev = 0
        for (r, b), count in red_dist.items():
            r_total = r + sum_seen_red
            b_total = b + sum_seen_black
            ev += r_total * b_total * count

        return ev / total if total > 0 else sum_seen_red * sum_seen_black

    def _expected_suit_frequency_product(self):
        seen = {
            'C': len(self.clubs),
            'S': len(self.spades),
            'D': len(self.diamonds),
            'H': len(self.hearts)
        }
        total_seen = sum(seen.values())
        n = 10 - total_seen
        suit_counts = {'C': 13 - seen['C'], 'S': 13 - seen['S'], 'D': 13 - seen['D'], 'H': 13 - seen['H']}
        
        total, prod_sum = 0, 0
        for c in range(min(n, suit_counts['C']) + 1):
            for s in range(min(n - c, suit_counts['S']) + 1):
                for d in range(min(n - c - s, suit_counts['D']) + 1):
                    h = n - c - s - d
                    if 0 <= h <= suit_counts['H']:
                        ways = (comb(suit_counts['C'], c) *
                                comb(suit_counts['S'], s) *
                                comb(suit_counts['D'], d) *
                                comb(suit_counts['H'], h))
                        prod = (c + seen['C']) * (s + seen['S']) * (d + seen['D']) * (h + seen['H'])
                        prod_sum += ways * prod
                        total += ways
        return prod_sum / total if total > 0 else seen['C'] * seen['S'] * seen['D'] * seen['H']
    
    
    
@dataclass
class PlayingCardsR4:
    red: list[int]
    black: list[int]
    
    _market1: float = field(init=False)
    _market2: float = field(init=False)
    _market3: float = field(init=False)
    
    def __post_init__(self) -> None:
        self._calculate_markets()
        
    def __repr__(self) -> str:
        print(f"Market 1: {round(self._market1, 3)}")
        print(f"Market 2: {round(self._market2, 3)}")
        print(f"Market 3: {round(self._market3, 3)}")
        return ""
    
    def _calculate_markets(self) -> None:
        all_cards = self.red + self.black
        self._market1 = PlayingCardsR1(all_cards)._theo
        self._market2 = self._expected_red_minus_black_plus_100()
        self._market3 = self._expected_face_times_nonface()

    def _expected_red_minus_black_plus_100(self):
        full_red = [i for i in range(1, 14)] * 2
        full_black = [i for i in range(1, 14)] * 2

        remaining_red = full_red.copy()
        remaining_black = full_black.copy()
        for card in self.red:
            remaining_red.remove(card)
        for card in self.black:
            remaining_black.remove(card)

        seen_red_sum = sum(self.red)
        seen_black_sum = sum(self.black)
        n = 10 - (len(self.red) + len(self.black))

        dist = Counter()
        for k in range(min(n, len(remaining_red)) + 1):
            for red_combo in combinations(remaining_red, k):
                red_sum = sum(red_combo)
                rem_k = n - k
                if rem_k > len(remaining_black):
                    continue
                for black_combo in combinations(remaining_black, rem_k):
                    black_sum = sum(black_combo)
                    dist[(red_sum, black_sum)] += 1

        total = sum(dist.values())
        if total == 0:
            return seen_red_sum - seen_black_sum + 100

        ev = sum((r + seen_red_sum - b - seen_black_sum) * count for (r, b), count in dist.items())
        return ev / total + 100

    def _expected_face_times_nonface(self):
        face_cards = {1, 11, 12, 13}
        nonface_cards = set(range(2, 11))

        seen_face = sum(1 for v in self.red + self.black if v in face_cards)
        seen_nonface = sum(1 for v in self.red + self.black if v in nonface_cards)
        seen_total = seen_face + seen_nonface
        n = 10 - seen_total

        remaining_face = 16 - seen_face
        remaining_nonface = 36 - seen_nonface

        total = 0
        weighted_sum = 0
        for k in range(min(n, remaining_face) + 1):
            f = k
            nf = n - k
            if nf > remaining_nonface:
                continue
            ways = comb(remaining_face, f) * comb(remaining_nonface, nf)
            product = (f + seen_face) * (nf + seen_nonface) * 10
            weighted_sum += ways * product
            total += ways

        if total == 0:
            return seen_face * seen_nonface * 10
        return weighted_sum / total
    
    

@dataclass
class PlayingCardsR5:
    clubs: list[int]
    spades: list[int]
    diamonds: list[int]
    hearts: list[int]
    n_cards: int = 10          # Total hand size is 10 cards
    n_trials: int = 5_000    # Number of Monte Carlo iterations
    
    _expected_value: float = field(init=False)
    
    def __post_init__(self):
        self._simulate_expected_value()
    
    def _build_deck(self):
        suits = ['C', 'D', 'H', 'S']
        return [(s, v) for s in suits for v in range(1, 14)]
    
    def _simulate_expected_value(self):
        # Build full deck as (suit, rank) tuples.
        deck = self._build_deck()
        # Create the list of shown cards from the four input lists.
        shown_cards = []
        shown_cards += [('C', v) for v in self.clubs]
        shown_cards += [('S', v) for v in self.spades]
        shown_cards += [('D', v) for v in self.diamonds]
        shown_cards += [('H', v) for v in self.hearts]
        
        # Remove shown cards from deck.
        remaining_deck = [card for card in deck if card not in shown_cards]
        n_to_draw = self.n_cards - len(shown_cards)
        
        total_value = 0.0
        # Run Monte Carlo simulation.
        for _ in range(self.n_trials):
            drawn = random.sample(remaining_deck, n_to_draw)
            full_hand = shown_cards + drawn
            best_val = self._best_hand_value(full_hand)
            total_value += best_val
        self._expected_value = total_value / self.n_trials
    
    def _best_hand_value(self, ten_cards):
        best = 0
        # Evaluate every 5-card combination out of the 10 cards.
        for five in combinations(ten_cards, 5):
            val = self._evaluate_hand(five)
            if val > best:
                best = val
        return best
    
    def _evaluate_hand(self, hand):
        # Sum card values (using card rank as the value, with Ace=1, J=11, Q=12, K=13)
        card_sum = sum(card[1] for card in hand)
        category = self._hand_category(hand)
        multiplier = self._hand_multiplier(category)
        return multiplier * card_sum
    
    def _hand_category(self, hand):
        suits = [card[0] for card in hand]
        ranks = [card[1] for card in hand]
        # Count occurrences of each rank.
        rank_counts = {r: ranks.count(r) for r in set(ranks)}
        is_flush = (len(set(suits)) == 1)
        sorted_ranks = sorted(ranks)
        is_straight = False
        # Check for five consecutive ranks.
        if sorted_ranks == list(range(sorted_ranks[0], sorted_ranks[0] + 5)):
            is_straight = True
        # Royal Flush: flush and contains {10, 11, 12, 13, 1}
        if is_flush and set(ranks) == {10, 11, 12, 13, 1}:
            return 'royal_flush'
        if is_flush and is_straight:
            return 'straight_flush'
        if 4 in rank_counts.values():
            return 'four_of_a_kind'
        if sorted(rank_counts.values()) == [2, 3]:
            return 'full_house'
        if is_flush:
            return 'flush'
        if is_straight:
            return 'straight'
        if 3 in rank_counts.values():
            return 'three_of_a_kind'
        if list(rank_counts.values()).count(2) == 2:
            return 'two_pair'
        if 2 in rank_counts.values():
            return 'pair'
        return 'high_card'
    
    
    def _hand_multiplier(self, category):
        # Mapping chosen so that examples match:
        mapping = {
            'royal_flush': 500,
            'straight_flush': 300,
            'four_of_a_kind': 200,
            'full_house': 100,
            'flush': 75, 
            'straight': 50,
            'three_of_a_kind': 25,
            'two_pair': 10, 
            'pair': 5,
            'high_card': 1
        }
        return mapping.get(category, 1)
    
    def __repr__(self):
        return f"Expected Poker Hand Value: {self._expected_value:.2f}"