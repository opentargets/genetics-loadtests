from locust import HttpLocust, TaskSet, task
import random

gene_list = open("resources/gene_ids.txt","r").read().splitlines()
study_list = open("resources/study_ids.txt", "r").read().splitlines()
trait_list = open("resources/trait_list.txt", "r").read().splitlines()

variant_list = open("resources/variants_sample.txt", "r").read().splitlines()

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

def generateVariant():
    """return an ensembl Gene ID ENSG"""
    return random.choice(variant_list)

def generateStudy():
    """return a random Study ID"""
    return random.choice(study_list)

def generateTraitSection():
    """return a random section of 2 words of a random reported_trait"""
    reported_trait = random.choice(trait_list).split(" ")
    pos = random.randint(0, max(len(reported_trait) - 2, 2))
    return " ".join(reported_trait[pos:pos+2])

def enc_gql(gql, *args):
    """from multiline to an interpolated line"""
    joint_line = " ".join(map(lambda el: el.strip(), gql.splitlines()))
    tupled_args = tuple(args)
    enc_line = joint_line

    if tupled_args:
        enc_line = joint_line % tupled_args

    return enc_line


class SearchQ(TaskSet):
    @task
    def search1(self):
        query_tokens = generateTraitSection()
        gql = '''
            query test4 { 
                search(queryString:"%s", pageIndex:0, pageSize:10) { 
                    totalGenes 
                    totalVariants 
                    totalStudies 
                    genes { 
                        id 
                    } 
                    variants { 
                        variant { 
                            id 
                        }
                    } 
                    studies { 
                        studyId 
                    } 
                }
            }
        '''
        self.client.post("/graphql", json = {'query': enc_gql(gql, query_tokens)})

class ApiBehavior(TaskSet):
    tasks = {SearchQ: 1}

    @task(5)
    def studyInfo(self):
        study_id = generateStudy()
        gql = '''
            query test4 { 
                studyInfo(studyId:"%s") { 
                    pmid 
                    pubDate 
                    pubJournal 
                    pubTitle 
                    pubAuthor 
                    studyId 
                    traitCode 
                    traitReported 
                    traitEfos 
                } 
            }
        '''
        self.client.post("/graphql", json={'query': enc_gql(gql, study_id)})

    @task(5)
    def variantInfo(self):
        variant_id = generateVariant()
        gql = '''
            query test4 { 
                variantInfo(variantId:"%s") { 
                    id 
                    rsId  
                    nearestGene { 
                        id 
                        symbol
                    } 
                    nearestCodingGene { 
                        id 
                        symbol 
                    } 
                }
            } 
        '''

        self.client.post("/graphql", json = {'query':enc_gql(gql, variant_id)})

    @task(2)
    def studiesForGene(self):
        gene_id = generateGene()
        gql = '''
            query test4 { 
                studiesForGene(geneId:"%s") { 
                    study { 
                        studyId 
                        traitCode 
                        traitReported 
                        traitEfos 
                        pmid 
                        pubDate 
                        pubJournal 
                        pubTitle 
                        pubTitle 
                        pubAuthor 
                        ancestryInitial 
                        ancestryReplication 
                        nInitial 
                        nReplication 
                        nCases 
                        traitCategory 
                    } 
                }
            }        
        '''
        self.client.post("/graphql", json = {'query':enc_gql(gql, gene_id)})

    @task(3)
    def topOverlappedStudies(self):
        study_id = generateStudy()
        gql = '''
            query test4 { 
                topOverlappedStudies(studyId:"%s", pageSize:10) { 
                    study { 
                        studyId 
                    } 
                    topStudiesByLociOverlap { 
                        study { 
                            studyId 
                        } 
                        numOverlapLoci 
                    } 
                }
            }
        '''
        self.client.post("/graphql", json = {'query':enc_gql(gql, study_id)})

    @task(1)
    def indexVariantsAndStudiesForTagVariant(self):
        variant_id = generateVariant()
        gql = '''
            query test4 { 
                indexVariantsAndStudiesForTagVariant(variantId:"%s", pageIndex:0, pageSize:10) { 
                    associations { 
                        indexVariant { 
                            id 
                        } 
                        study { 
                            studyId 
                            traitCode 
                            traitReported 
                            traitEfos 
                            pmid 
                            pubDate 
                            pubJournal 
                            pubTitle 
                            pubAuthor 
                        } 
                        pval 
                        nTotal 
                        nCases 
                        overallR2 
                        afr1000GProp 
                        amr1000GProp 
                        eas1000GProp 
                        eur1000GProp 
                        sas1000GProp 
                        log10Abf 
                        posteriorProbability 
                    } 
                } 
            }
        '''
        self.client.post("/graphql", json = {'query':enc_gql(gql, variant_id)})

    @task(2)
    def tagsVariantsAndStudiesForIndexVariant(self):
        variant_id = generateVariant()
        gql = '''
            query test4 { 
                tagVariantsAndStudiesForIndexVariant(variantId:"%s", pageIndex:0, pageSize:1) { 
                    associations { 
                        tagVariant { 
                            id 
                        } 
                        study { 
                            studyId 
                            traitCode 
                            traitReported 
                            traitEfos 
                            pmid 
                            pubDate 
                            pubJournal 
                            pubTitle 
                            pubAuthor
                        } 
                        pval 
                        nTotal 
                        nCases 
                        overallR2 
                        afr1000GProp 
                        amr1000GProp 
                        eas1000GProp 
                        eur1000GProp 
                        sas1000GProp 
                        log10Abf 
                        posteriorProbability
                    }
                }
            }
           '''
        self.client.post("/graphql", json={'query': enc_gql(gql, variant_id)})

    @task(1)
    def gecko(self):
        region = generateRegion()
        gql = '''
            query test4 { 
                gecko(chromosome:"%s",start:%d,end:%d) { 
                    genes { 
                        id 
                        symbol 
                        chromosome 
                        start 
                        end 
                        tss 
                        bioType 
                        fwdStrand 
                        exons 
                    } 
                    tagVariants { 
                        id 
                        rsId 
                        chromosome 
                        position 
                        refAllele 
                        altAllele 
                    } 
                    indexVariants { 
                        id 
                        rsId 
                        chromosome 
                        position 
                        refAllele 
                        altAllele 
                    } 
                    studies { 
                        studyId 
                        traitCode 
                        traitReported 
                        traitEfos 
                        pmid 
                        pubDate 
                        pubJournal 
                        pubTitle 
                        pubAuthor
                    } 
                    geneTagVariants { 
                        geneId 
                        tagVariantId 
                        overallScore 
                    } 
                    tagVariantIndexVariantStudies { 
                        tagVariantId 
                        indexVariantId 
                        studyId 
                        r2 
                        posteriorProbability 
                        pval
                    }
                }
            }
           '''
        self.client.post("/graphql", json={'query': enc_gql(gql, *region)})

    @task(2)
    def genesForVariant(self):
        variant_id = generateVariant()
        gql = '''
            query test4 {
                genesForVariant(variantId:"%s") { 
                    gene { 
                        id 
                        symbol 
                        chromosome 
                        start 
                        end 
                        tss 
                        bioType 
                        fwdStrand 
                        exons 
                    } 
                    overallScore 
                    qtls { 
                        typeId 
                        sourceId 
                        aggregatedScore 
                        tissues { 
                            tissue { 
                                id 
                                name 
                            } 
                            quantile 
                            beta 
                            pval 
                        } 
                    } 
                    intervals { 
                        typeId 
                        sourceId 
                        aggregatedScore 
                        tissues { 
                            tissue { 
                                id 
                                name 
                            } 
                            quantile 
                            score 
                        } 
                    } 
                    functionalPredictions { 
                        typeId 
                        sourceId 
                        aggregatedScore 
                        tissues { 
                            tissue { 
                                id 
                                name 
                            } 
                            maxEffectLabel 
                            maxEffectScore
                        }
                    }
                }
            }
        '''
        self.client.post("/graphql", json = {'query':enc_gql(gql, variant_id)})

    @task(5)
    def manhattan(self):
        study_id = generateStudy()
        gql = '''
            query test4 {
                manhattan(studyId:"%s") {
                    associations {
                        variant {
                            id
                            rsId
                            chromosome
                            position
                            refAllele
                            altAllele
                            nearestGene {
                                id
                                symbol
                            }
                            nearestCodingGene { 
                                id 
                                symbol 
                            } 
                        } 
                        pval 
                        bestGenes { 
                            gene { 
                                id 
                                symbol 
                            } 
                            score
                        } 
                        credibleSetSize 
                        ldSetSize 
                        totalSetSize
                    }
                }
            }
        '''
        self.client.post("/graphql", json={'query': enc_gql(gql, study_id)})


class WebsiteUser(HttpLocust):
    task_set = ApiBehavior
    min_wait = 500
    max_wait = 2000

