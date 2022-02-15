from DNAContamination import DNAContamination
from struttureImpiegate.chain_hash_map import ChainHashMap



def test(s, k, l):
    """
    Function that tests the string s with the contaminants contained in the file .fasta that have a contamination degree at least of l.
    :param s: the string that is used as reference.
    :param k: the values required.
    :param l: the current required threshold value.
    :return:
    """
    contaminer = DNAContamination(s, l)
    id_string_map = ChainHashMap(cap=20000)
    with open("./target_batch.fasta", "r") as file:
        while True:
            id = file.readline()
            if id == '':
                break
            contaminant = file.readline()[:-1]
            id_string_map[contaminant] = int(id[1:])
            contaminer.addContaminant(contaminant)
    string = ''

    max_contaminants = contaminer.getContaminants(k)
    all_contaminants = []
    for contaminant in max_contaminants:
        all_contaminants.append(id_string_map[contaminant])
    for contaminant in sorted(all_contaminants):
        string += ", " + str(contaminant)
    return string[2:]



if __name__ == "__main__":
    s = "TGGTGTATGAGCTACCAGCCGTGCGAAACTCATACTATTATCTAATCAGGGACAATACCTCAGGCAGGACTGTGCTGTGTAGATAGCTGGAGAGTATTTCTGATTGTCTCCGAGGGGTGTAAAGGTACTTGCAAGGCCACTCAACTCATGCAGCGTTTCCATTTGAGTTGCCTTGAGTAAACGTCAACGCAGCTGGGAGTAGTACCTCTTGGAGGTTGTGACCGCCGCTGCCCGCATGGACAGACGCACGGAAATGTATTAACACTAACTATACT"
    print(test(s, 20, 7))


