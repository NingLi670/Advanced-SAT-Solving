import argparse
from cdcl_lrb import CDCL_LRB
from cdcl_chb import CDCL_CHB
from cdcl import cdcl
from restart import CDCL_SOLVER
from utils import read_cnf
from preprocess import preprocess, postprocess
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="examples/and1.cnf")
    parser.add_argument("-d", "--decide", type=int, default=1)  # 0->vsids, 1->lrb, 2->chb
    parser.add_argument("-r", "--restart", type=int, default=0) # 0->no restart, 1->restart
    parser.add_argument("-m", "--MAB", type=int, default=0)     # 0->no MAB rechoosing, 1->MOSS, 2->UCB1
    parser.add_argument('-b', '--bve', type=int, default=0)
    parser.add_argument('-s', '--subsumption', type=int, default=0, choices=[0, 1])

    return parser.parse_args()


def main(args):
    # Create problem.
    with open(args.input, "r") as f:
        sentence, num_vars = read_cnf(f)
    start = time.time()
    # Create CDCL solver and solve it!
    heuristic = args.decide

    # Preprocess
    if args.bve or args.subsumption:
        ori_sentence = sentence.copy()
        sentence, removed_val = preprocess(
            sentence, num_vars, args.bve, args.subsumption)

    # Change heuristic algorithm
    if args.restart == 0 and args.MAB == 0:
        if heuristic == 1:
            print('Using heuristic: lrb')
            solver = CDCL_LRB(sentence, num_vars)
            res = solver.run()

        if heuristic == 2:
            print('Using heuristic: chb')
            solver = CDCL_CHB(sentence, num_vars)
            res = solver.run()

        if heuristic == 0:
            print('Using heuristic: vsids')
            res = cdcl(sentence, num_vars)
    else:
        # Restart
        solver = CDCL_SOLVER(sentence, num_vars,
                             args.restart, args.MAB, args.decide)
        res = solver.run()

    # Preprocess
    if args.bve:
        res = postprocess(res, removed_val)

    end = time.time()
    t = end - start
    if res is None:
        print("✘ No solution found")
    else:
        print(f"✔ Successfully found a solution: {res}")
    print('总用时：'+str(t))


if __name__ == "__main__":
    args = parse_args()
    main(args)
