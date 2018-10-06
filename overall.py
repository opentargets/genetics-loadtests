from locust import HttpLocust, TaskSet, task


class SearchQ(TaskSet):
    @task
    def search1(self):
        self.client.post("/graphql", json = {'query':'query test4 { search(queryString:"mt",pageIndex:0, pageSize:10) { totalGenes totalVariants totalStudies genes { id } variants { variant { id } } studies { studyId } }}'})

class ApiBehavior(TaskSet):
    tasks = {SearchQ: 5}

    @task(5)
    def studyInfo(self):
        self.client.post("/graphql", json={'query': 'query test4 { studyInfo(studyId:"GCST000001") { pmid pubDate pubJournal pubTitle pubAuthor studyId traitCode traitReported traitEfos } }'})

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

