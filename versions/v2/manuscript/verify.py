import itertools
import json


def rays_le(first, second):
    return first == (0, 0) or (first[0] == second[0] and first[1] <= second[1])


def tail_le(first, second):
    return first <= second and (first, second) != (1, 2)


def check_order(elements, relation):
    assert all(relation(element, element) for element in elements)
    for first, second in itertools.product(elements, repeat=2):
        assert not (relation(first, second) and relation(second, first)) or first == second
    for first, second, third in itertools.product(elements, repeat=3):
        assert not (relation(first, second) and relation(second, third)) or relation(first, third)


def check_embedding(images, relation):
    assert len(set(images)) == 3
    for first, second in itertools.product(range(3), repeat=2):
        assert relation(images[first], images[second]) == (first == 0 or first == second)


def check_finite_posets():
    counts = {}
    for size in range(1, 6):
        strict_pairs = list(itertools.combinations(range(size), 2))
        count = 0
        for mask in range(1 << len(strict_pairs)):
            pairs = {(point, point) for point in range(size)}
            pairs.update(pair for index, pair in enumerate(strict_pairs) if mask & (1 << index))
            if any((first, third) not in pairs for first, middle, third in
                   itertools.product(range(size), repeat=3)
                   if (first, middle) in pairs and (middle, third) in pairs):
                continue
            maxima = [point for point in range(size) if not any(
                point != other and (point, other) in pairs for other in range(size)
            )]
            heights = []
            for point in range(size):
                heights.append(1 + max((heights[lower] for lower in range(point)
                                       if (lower, point) in pairs), default=0))
            height = max(heights)
            assert maxima
            assert all(any((point, maximal) in pairs for maximal in maxima) for point in range(size))
            assert (len(maxima) == 1) == any(
                all((point, greatest) in pairs for point in range(size)) for greatest in range(size)
            )
            base = [(0, point, 0) for point in range(size)]
            rays = [(1, maximal, index) for maximal in maxima for index in range(2)]

            def relation(first, second):
                if first[0] == 0:
                    return (first[1], second[1]) in pairs
                return second[0] == 1 and first[1] == second[1] and first[2] <= second[2]

            check_order(base + rays, relation)
            for maximal in maxima:
                cone = [point for point in base if (point[1], maximal) in pairs]
                cone += [point for point in rays if point[1] == maximal]
                for ray_point in [point for point in rays if point[1] == maximal]:
                    assert all(relation(point, ray_point) or relation(ray_point, point) for point in cone)
                if len(maxima) > 1:
                    assert sum((point, maximal) in pairs for point in range(size)) < size
                    strict_cone = [point for point in range(size)
                                   if point != maximal and (point, maximal) in pairs]
                    assert max((heights[point] for point in strict_cone), default=0) < height
            count += 1
        counts[str(size)] = count
    return counts


def check_lifting_and_ordinal_fibers():
    lifting_subsets = 0
    ordinal_orders = 0
    for size in range(1, 4):
        strict_pairs = list(itertools.combinations(range(size), 2))
        for mask in range(1 << len(strict_pairs)):
            pairs = {(point, point) for point in range(size)}
            pairs.update(pair for index, pair in enumerate(strict_pairs)
                         if mask & (1 << index))
            if any((first, third) not in pairs for first, middle, third in
                   itertools.product(range(size), repeat=3)
                   if (first, middle) in pairs and (middle, third) in pairs):
                continue

            def lexicographic(first, second):
                return ((first[0] != second[0] and (first[0], second[0]) in pairs)
                        or (first[0] == second[0] and first[1] <= second[1]))

            for ordinal_size in range(1, 5):
                elements = list(itertools.product(range(size), range(ordinal_size)))
                check_order(elements, lexicographic)
                for first, second in itertools.product(range(size), repeat=2):
                    assert lexicographic((first, 0), (second, 0)) == ((first, second) in pairs)
                ordinal_orders += 1
            elements = list(itertools.product(range(size), range(4)))
            for subset_mask in range(1 << len(elements)):
                subset = {point for index, point in enumerate(elements)
                          if subset_mask & (1 << index)}
                images = []
                for point in subset:
                    upper = 1 + max(other[1] for other in subset if other[0] == point[0])
                    image = (point[0], upper + point[1])
                    assert image not in subset
                    assert image != point and lexicographic(point, image)
                    images.append(image)
                assert len(set(images)) == len(subset)
                lifting_subsets += 1
    for value in range(2048):
        exponent = 0
        odd_part = value + 1
        while odd_part % 2 == 0:
            exponent += 1
            odd_part //= 2
        index = (odd_part - 1) // 2
        assert value == 2 ** exponent * (2 * index + 1) - 1
    for chain_size in range(2, 11):
        assert (chain_size + 1) % chain_size != 0
    return {
        'lexicographic_orders': ordinal_orders,
        'finite_fiber_subsets': lifting_subsets,
        'ordinal_fiber_sizes': '1,...,4',
        'lifting_sections': 'subsets of {0,...,3} in each of at most three fibers',
        'countable_partition_values': '0,...,2047',
        'finite_skeleton_sizes': '2,...,10',
    }


def main():
    bound = 24
    rays = list(itertools.product(range(2), range(bound)))
    tail = list(range(2 * bound))
    check_order(rays, rays_le)
    check_order(tail, tail_le)
    check_embedding([(0, 0), (0, 1), (1, 0)], rays_le)
    check_embedding([0, 1, 2], tail_le)
    rays_triples = 0
    tail_triples = 0
    for first, second, third in itertools.product(rays, repeat=3):
        assert not (rays_le(first, third) and rays_le(second, third)) or (
            rays_le(first, second) or rays_le(second, first)
        )
        rays_triples += 1
    for first, second, third in itertools.product(tail, repeat=3):
        if not tail_le(first, second) and not tail_le(second, first):
            assert {first, second} == {1, 2}
            if first != third and tail_le(first, third):
                assert tail_le(second, third)
        tail_triples += 1
    for first, second in itertools.product(range(bound), repeat=2):
        for ray in range(2):
            assert rays_le((ray, first), (ray, second)) == (first <= second)
        assert tail_le(2 * first, 2 * second) == (first <= second)
        assert tail_le(2 * first + 1, 2 * second + 1) == (first <= second)
    assert set(range(0, 2 * bound, 2)).isdisjoint(range(1, 2 * bound, 2))
    assert set(range(0, 2 * bound, 2)) | set(range(1, 2 * bound, 2)) == set(tail)
    print(json.dumps({
        "status": "pass",
        "rays_domain": "{0,1} x {0,...,23}",
        "tail_domain": "{0,...,47}",
        "order_and_embedding_checks": "pass",
        "partition_enumeration_indices": "0,...,23",
        "rays_structural_triples": rays_triples,
        "tail_structural_triples": tail_triples,
        "naturally_labelled_posets_by_size": check_finite_posets(),
        "lifting_ordinal_and_partition_checks": check_lifting_and_ordinal_fibers(),
        "scope": "Finite checks of the displayed orders and implications; infinite statements have written proofs in note.tex."
    }, indent=2))


if __name__ == "__main__":
    main()
