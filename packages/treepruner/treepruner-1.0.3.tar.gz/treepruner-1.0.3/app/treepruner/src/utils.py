import ete3
import numpy as np

def one_primitive_step(tree, original_num_leaves, percent_left, longest_to_average):
    PRUNE = False
    longest_branch_length = 0
    longest_branch = None
    total_branch_length = 0
    branch_count = 0

    for node in tree.traverse():
        current = node.dist
        total_branch_length += current
        branch_count += 1
        if current > longest_branch_length:
            longest_branch_length = current
            longest_branch = node

    average_branch_length = total_branch_length / branch_count
    leaves_on_one_side = longest_branch.get_leaves()

    all_leaves = set(tree.get_leaves())
    num_leaves = len(all_leaves)
    one_side = len(leaves_on_one_side)
    other_side = num_leaves - one_side
    leaf_names = [leaf.name for leaf in leaves_on_one_side]
    leaves_on_other_side = all_leaves - set(leaves_on_one_side)
    other_leaf_names = [leaf.name for leaf in leaves_on_other_side]

    if longest_branch_length > longest_to_average*average_branch_length:
        if (percent_left * original_num_leaves) / 100 > one_side:
            tree.prune(other_leaf_names, preserve_branch_length=True)
            PRUNE = True
            percent_left -= 100 * one_side / original_num_leaves
        elif percent_left*original_num_leaves/100 > other_side:
            tree.prune(leaf_names, preserve_branch_length=True)
            PRUNE = True
            percent_left -= 100 * other_side / original_num_leaves
    return tree, PRUNE, percent_left

def is_valid_tree(file_path):
    try:
        tree_wannabe = ete3.Tree(file_path, format=1)
        return True
    except:
        return False


def calculate_iqr_threshold(values):
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    upper_fence = q3 + 3 * iqr
    return upper_fence


def prune_by_branch_length(tree, threshold):
    branch_lengths = [node.dist for node in tree.traverse() if not node.is_root()]
    upper_fence = calculate_iqr_threshold(branch_lengths)
    total_tips = len(tree.get_leaves())
    percent_left = 100 - threshold
    for node in tree.traverse():
        if not node.is_root():
            all_leaves = set(tree.get_leaves())
            num_leaves = len(all_leaves)
            leaves_on_one_side = node.get_leaves()
            one_side = len(leaves_on_one_side)
            leaf_names = [leaf.name for leaf in leaves_on_one_side]
            other_side = num_leaves - one_side
            leaves_on_other_side = all_leaves - set(leaves_on_one_side)
            other_side_names = [leaf.name for leaf in leaves_on_other_side]
            min_tips = min(one_side, other_side)
            if node.dist > upper_fence and min_tips < (percent_left * total_tips) / 100 :
                if one_side > other_side:
                    tree.prune(leaves_on_one_side, preserve_branch_length=True)
                    percent_left -= 100 * other_side / total_tips
                else:
                    tree.prune(leaves_on_other_side, preserve_branch_length=True)
                    percent_left -= 100 * one_side / total_tips
    return tree, percent_left


def prune_by_root_to_tip(tree, percent_left, original_num_leaves):
    tree.set_outgroup(tree.get_midpoint_outgroup())
    root_to_tip_distances = {leaf: tree.get_distance(leaf) for leaf in tree.get_leaves()}
    upper_fence = calculate_iqr_threshold(list(root_to_tip_distances.values()))
    outliers = [leaf for leaf, distance in root_to_tip_distances.items() if distance > upper_fence]
    num_outliers = len(outliers)
    if num_outliers > (percent_left * original_num_leaves) / 100:
        return tree
    else:
        removed_counter = 0
        while removed_counter < (percent_left * original_num_leaves) / 100:
            tree.set_outgroup(tree.get_midpoint_outgroup())
            root_to_tip_distances = {leaf: tree.get_distance(leaf) for leaf in tree.get_leaves()}
            upper_fence = calculate_iqr_threshold(list(root_to_tip_distances.values()))

            extreme_outlier = max(root_to_tip_distances, key=root_to_tip_distances.get)
            if root_to_tip_distances[extreme_outlier] > upper_fence:
                extreme_outlier.detach()
                removed_counter += 1
                percent_left -= 100 / original_num_leaves
            else:
                break
    tree.unroot()
    return tree

def validate_cpa_arguments(name_of_the_tree, root_to_node_ratio, min_num_of_roots, M_n, threshold, beta, radius_ratio, safe_tips, show_plot, show_pruned_tips, name_of_output):

    if not isinstance(name_of_the_tree, str):
        raise TypeError("`name_of_the_tree` must be a string.")
    if not is_valid_tree(name_of_the_tree):
        raise TypeError("`name_of_the_tree` must contain a valid .nwk or .newick tree.")

    if not isinstance(root_to_node_ratio, (int, float)):
        raise TypeError("`root_to_node_ratio` must be an integer or a float.")
    if not (0 <= root_to_node_ratio <= 1):
        raise ValueError("`root_to_node_ratio` is outside the expected [0,1] range.")

    if not isinstance(min_num_of_roots, int):
        raise TypeError("`min_num_of_roots` must be an integer.")
    if min_num_of_roots < 1:
        raise ValueError("`min_num_of_roots` must be at least 1.")

    if M_n != 0 and not callable(M_n):
        raise TypeError("`M_n` must be a function or 0.")

    if not isinstance(threshold, (int, float)):
        raise TypeError("`threshold` must be an integer or a float.")
    if not (0 <= threshold <= 100):
        raise ValueError("`threshold` is outside the expected [0,100] range.")

    if not isinstance(beta, (int, float)):
        raise TypeError("`beta` must be an integer or a float.")
    if not (0 <= beta <= 100):
        raise ValueError("`beta` is outside the expected [0,100] range.")

    if not isinstance(radius_ratio, (int, float)):
        raise TypeError("`radius_ratio` must be an integer or a float.")
    if not (0 <= radius_ratio <= 100):
        raise ValueError("`radius_ratio` is outside the expected [0,100] range.")
    
    if not isinstance(safe_tips, list) or not all(isinstance(tip, str) for tip in safe_tips):
        raise TypeError("`safe_tips` must be a list of strings.")

    if not isinstance(show_plot, bool):
        raise TypeError("`show_plot` must be a boolean.")

    if not isinstance(show_pruned_tips, bool):
        raise TypeError("`show_pruned_tips` must be a boolean.")

    if not isinstance(name_of_output, str):
        raise TypeError("`name_of_output` must be a string.")


def validate_psfa_arguments(name_of_the_tree,threshold,longest_to_average,name_of_output):
        
    if not isinstance(name_of_the_tree, str):
        raise TypeError("`name_of_the_tree` must be a string.")
    if not is_valid_tree(name_of_the_tree):
        raise TypeError("`name_of_the_tree` must contain a valid .nwk or .newick tree.")

    if not isinstance(threshold, (int, float)):
        raise TypeError("`threshold` must be an integer or a float.")
    if not (0 <= threshold <= 100):
        raise ValueError("`threshold` is outside the expected [0,100] range.")

    if not isinstance(longest_to_average, (int,float)):
        raise TypeError("`longest_to_average` must be an integer or a float.")
    if longest_to_average < 0:
        raise ValueError("`longest_to_average` must be at least 0.")
    
    if not isinstance(name_of_output, str):
        raise TypeError("`name_of_output` must be a string.")

def validate_iqr_arguments(name_of_the_tree,threshold,name_of_output):

    if not isinstance(name_of_the_tree, str):
        raise TypeError("`name_of_the_tree` must be a string.")
    if not is_valid_tree(name_of_the_tree):
        raise TypeError("`name_of_the_tree` must contain a valid .nwk or .newick tree.")

    if not isinstance(threshold, (int, float)):
        raise TypeError("`threshold` must be an integer or a float.")
    if not (0 <= threshold <= 100):
        raise ValueError("`threshold` is outside the expected [0,100] range.")

    if not isinstance(name_of_output, str):
        raise TypeError("`name_of_output` must be a string.")