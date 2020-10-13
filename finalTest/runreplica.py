#YaYi 2020.10.13

import InitChainAndNodes
import ReplicationAlgorithms

"""
the main program.

"""




if __name__=='__main__':
    l=InitChainAndNodes.load_blockbits_and_targets(0,2016)
    print(l)