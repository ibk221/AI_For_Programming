"""Print the GC content percentage for each sequence in a FASTA file."""

import argparse
import sys


def fasta_records(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence_parts = []

    with open(path) as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence_parts)
                header = line[1:]
                sequence_parts = []
            elif header is None:
                raise ValueError("FASTA sequence data must follow a header line.")
            else:
                sequence_parts.append("".join(line.split()))

    if header is not None:
        yield header, "".join(sequence_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Print GC content percentages for sequences in a FASTA file."
    )
    parser.add_argument("fasta_file", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="minimum GC percentage; only print records strictly above this value",
    )
    args = parser.parse_args()

    for header, sequence in fasta_records(args.fasta_file):
        if not sequence:
            print(f"Warning: skipping empty sequence for header >{header}", file=sys.stderr)
            continue
        sequence = sequence.upper()
        gc_count = sequence.count("G") + sequence.count("C")
        gc_percentage = gc_count / len(sequence) * 100
        if args.min_gc is not None and gc_percentage <= args.min_gc:
            continue
        print(f">{header}\t{gc_percentage:.2f}%")


if __name__ == "__main__":
    main()
