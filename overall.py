from locust import HttpLocust, TaskSet, task
import random

gene_list = open("resources/gene_ids.txt","r").read().splitlines()
study_list = open("resources/study_ids.txt", "r").read().splitlines()
trait_list = study_list = open("resources/trait_list.txt", "r").read().splitlines()

chrom_lengths = {
    '1': 249250621,
    '10': 135534747,
    '11': 135006516,
    '12': 133851895,
    '13': 115169878,
    '14': 107349540,
    '15': 102531392,
    '16': 90354753,
    '17': 81195210,
    '18': 78077248,
    '19': 59128983,
    '2': 243199373,
    '20': 63025520,
    '21': 48129895,
    '22': 51304566,
    '3': 198022430,
    '4': 191154276,
    '5': 180915260,
    '6': 171115067,
    '7': 159138663,
    '8': 146364022,
    '9': 141213431,
    'X': 155270560,
    'Y': 59373566
}

def generateRegion():
    """return a random region (chrId, start, end)"""
    chr_id = random.choice(chrom_lengths.keys())
    max_len = chrom_lengths[chr_id]
    start = random.randint(1, max_len)
    end = start + random.randint(1000000, 2000000)

    return (chr_id, start, min(end, max_len))

def generateGene():
    """return an ensembl Gene ID ENSG"""
    return random.choice(gene_list)

def generateStudy():
    """return a random Study ID"""
    return random.choice(study_list)

def generateTraitSection():
    """return a random section of 2 words of a random reported_trait"""
    reported_trait = random.choice(trait_list).split(" ")
    pos = random.randint(0, max(len(reported_trait) - 2, 2))
    return " ".join(reported_trait[pos:pos+2])

class SearchQ(TaskSet):
    @task
    def search1(self):
        query_tokens = generateTraitSection()
        gql = 'query test4 { search(queryString:"%s", pageIndex:0, pageSize:10) { totalGenes totalVariants totalStudies genes { id } variants { variant { id } } studies { studyId } } }' % query_tokens
        self.client.post("/graphql", json = {'query': gql})

class ApiBehavior(TaskSet):
    tasks = {SearchQ: 1}

    @task(5)
    def studyInfo(self):
        study_id = generateStudy()
        gql = 'query test4 { studyInfo(studyId:"%s") { pmid pubDate pubJournal pubTitle pubAuthor studyId traitCode traitReported traitEfos } }' % study_id
        self.client.post("/graphql", json={'query': gql})

    @task(5)
    def variantInfo(self):
        self.client.post("/graphql", json = {'query':'query test4 { variantInfo(variantId:"15_63605080_C_T") { id rsId  nearestGene { id symbol  } nearestCodingGene { id symbol } } } '})

    # @task(1)
    # def variantsForGene(self):
    #     self.client.post("/graphql", json = {'query':'query test4 { variantsForGene(geneId:"ENSG00000132485") { gene { id symbol } variant overallScore qtls { typeId sourceId aggregatedScore } intervals { typeId sourceId aggregatedScore } functionalPredictions { typeId sourceId aggregatedScore } }'})

    @task(2)
    def studiesForGene(self):
        self.client.post("/graphql", json = {'query':'query test4 { studiesForGene(geneId:"ENSG00000132485") { study { studyId traitCode traitReported traitEfos pmid pubDate pubJournal pubTitle pubTitle pubAuthor ancestryInitial ancestryReplication nInitial nReplication nCases traitCategory } } }'})

    @task(3)
    def topOverlappedStudies(self):
        self.client.post("/graphql", json = {'query':'query test4 { topOverlappedStudies(studyId:"NEALEUKB_L03", pageSize:10) { study { studyId } topStudiesByLociOverlap { study { studyId } numOverlapLoci } } }'})

    @task(1)
    def indexVariantsAndStudiesForTagVariant(self):
        self.client.post("/graphql", json = {'query':'query test4 { indexVariantsAndStudiesForTagVariant(variantId:"1_42318930_A_G", pageIndex:0, pageSize:10) { associations { indexVariant { id } study { studyId traitCode traitReported traitEfos pmid pubDate pubJournal pubTitle pubAuthor } pval nTotal nCases overallR2 afr1000GProp amr1000GProp eas1000GProp eur1000GProp sas1000GProp log10Abf posteriorProbability } } }'})


class WebsiteUser(HttpLocust):
    task_set = ApiBehavior
    min_wait = 500
    max_wait = 2000

