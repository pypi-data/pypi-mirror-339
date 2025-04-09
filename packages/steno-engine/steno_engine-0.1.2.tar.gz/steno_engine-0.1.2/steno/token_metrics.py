import tiktoken


# the gpt-4o encoder is the cl200k. for our purposes this is sufficient.
encoder = tiktoken.encoding_for_model("gpt-4o")


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in the given text using the tiktoken library.
    """
    tokens = encoder.encode(text)
    return len(tokens)


def summary_metrics(original: str, final: str) -> list[dict]:
    """
    Generate summary statistics
    """
    original_count = count_tokens(original)
    final_count = count_tokens(final)
    n_saved = original_count - final_count
    percent_saved = (1 - final_count / original_count)
    return [
        dict(
            label='Original Count',
            value=original_count,
        ),
        dict(
            label='# Saved',
            value=n_saved
        ),
        dict(
            label='% Saved',
            value=percent_saved
        ),
        dict(
            label='Final Count',
            value=final_count,
        )
    ]


def summary(original: str, final: str) -> str:
    label = "Statistic".ljust(20)
    table = [f"{label}\tValue"]
    for metric in summary_metrics(original, final):
        label = metric['label'].ljust(20)
        value = metric['value']
        if '%' in label:
            value = f"{value:.2%}"
        row = f"{label}\t{value}"
        table.append(row)
    underline = '-' * (4 + max(len(row) for row in table))
    table = table[0:1] + [underline] + table[1:] + [underline]
    return '\n' + "\n".join(table)

    table = ["Statistic|Value"]
    for metric in summary_metrics(original, final):
        label = metric['label']
        value = metric['value']
        if '%' in label:
            value = f"{value:.2%}"
        row = f"{label}|{value}"
        table.append(row)
    return "\n".join(table)
