"""Statistics and percentile calculation functions."""


def calculate_percentile(value, all_values):
    """Calculate what percentile a value falls into."""
    if not all_values:
        return 0

    count_below = sum(1 for v in all_values if v < value)
    percentile = (count_below / len(all_values)) * 100

    return percentile


def calculate_criteria_percentiles(player_stats, all_criteria_values):
    """Calculate percentiles for all 6 criteria.

    For defense, we first normalize each component to z-scores, average them,
    then calculate the percentile of the composite score. This preserves
    the proper distribution unlike averaging percentiles.
    """
    percentiles = {}
    for criterion, value in player_stats.items():
        if criterion == 'defense':
            # Defense is special: normalize each component, average, then percentile
            # This preserves the distribution better than averaging percentiles

            # Get component values
            player_xg = value['xg_pct']
            player_take = value['takeaways_p60']
            player_block = value['blocks_p60']

            all_xg = all_criteria_values['defense']['xg_pct']
            all_take = all_criteria_values['defense']['takeaways_p60']
            all_block = all_criteria_values['defense']['blocks_p60']

            # Normalize to z-scores (subtract mean, divide by std dev)
            import statistics

            mean_xg = statistics.mean(all_xg)
            std_xg = statistics.stdev(all_xg) if len(all_xg) > 1 else 1
            z_xg = (player_xg - mean_xg) / std_xg if std_xg > 0 else 0

            mean_take = statistics.mean(all_take)
            std_take = statistics.stdev(all_take) if len(all_take) > 1 else 1
            z_take = (player_take - mean_take) / std_take if std_take > 0 else 0

            mean_block = statistics.mean(all_block)
            std_block = statistics.stdev(all_block) if len(all_block) > 1 else 1
            z_block = (player_block - mean_block) / std_block if std_block > 0 else 0

            # Average z-scores to get composite
            composite_z = (z_xg + z_take + z_block) / 3

            # Calculate all composite scores for percentile
            all_composite_scores = []
            for i in range(len(all_xg)):
                z_xg_i = (all_xg[i] - mean_xg) / std_xg if std_xg > 0 else 0
                z_take_i = (all_take[i] - mean_take) / std_take if std_take > 0 else 0
                z_block_i = (all_block[i] - mean_block) / std_block if std_block > 0 else 0
                all_composite_scores.append((z_xg_i + z_take_i + z_block_i) / 3)

            # Now get percentile of composite score
            percentiles[criterion] = calculate_percentile(composite_z, all_composite_scores)
        else:
            percentiles[criterion] = calculate_percentile(value, all_criteria_values[criterion])
    return percentiles


def get_grade(percentile):
    """Convert percentile to grade (F to S)."""
    if percentile >= 95:
        return "S"
    elif percentile >= 85:
        return "A"
    elif percentile >= 70:
        return "B"
    elif percentile >= 50:
        return "C"
    elif percentile >= 25:
        return "D"
    else:
        return "F"


def get_rating(percentile):
    """Convert percentile to rating (Bad, OK, Good)."""
    if percentile < 50:
        return "No"
    elif percentile < 80:
        return "Maybe"
    else:
        return "Yes"


def get_rating_color(rating):
    """Get color for rating."""
    if rating == "No":
        return "red"
    elif rating == "Maybe":
        return "blue"
    else:
        return "green"


def create_hexagon_visualization(percentiles):
    """Create horizontal bar chart showing 6 criteria breakdown."""

    # Define criteria order and labels
    criteria_order = [
        ('scoring', 'scoring'),
        ('shooting', 'shooting'),
        ('playmaking', 'playmaking'),
        ('defense', 'defense'),
        ('physicality', 'physicality'),
        ('possession', 'possession')
    ]

    lines = []
    bar_length = 20  # Total length of bar

    for key, label in criteria_order:
        percentile = percentiles[key]
        filled = int((percentile / 100) * bar_length)
        empty = bar_length - filled

        bar = '█' * filled + '░' * empty
        grade = get_grade(percentile)

        lines.append(f"{label:<13} {bar} {grade}")

    return '\n'.join(lines)
