# scripts-reverse_complement.py
# Reads a DNA sequence from a single-record FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}


def read_fasta_sequence(path):
    """Return the sequence from a single-record FASTA file."""
    with open(path) as f:
        lines = f

        sequence_parts = []
        found_header = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if found_header:
                    raise ValueError("FASTA file must contain exactly one record.")
                found_header = True
            elif not found_header:
                raise ValueError("FASTA sequence must start with a header line.")
            else:
                sequence_parts.append(line)

    if not found_header:
        raise ValueError("FASTA file must contain a header line.")
    return "".join(sequence_parts)


def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    seq = seq.upper()
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Sequence contains invalid character {error.args[0]!r}; "
            "only A, T, C, and G are allowed."
        ) from error


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print the reverse complement of a FASTA sequence.")
    parser.add_argument("fasta_file", help="path to a single-record FASTA file")
    args = parser.parse_args()
    seq = read_fasta_sequence(args.fasta_file)
    print(reverse_complement(seq))