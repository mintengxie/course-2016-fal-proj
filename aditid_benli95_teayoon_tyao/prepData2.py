import json
import dml
import prov.model
import datetime
import uuid
from bson.code import Code


class prepData2(dml.Algorithm):

    contributor = 'aditid_benli95_teayoon_tyao'
    reads = ['aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadius', 'aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadiusDrug']
    writes = ['aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment', 'aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment', 'aditid_benli95_teayoon_tyao.averageAll', 'aditid_benli95_teayoon_tyao.averageDrug']


    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aditid_benli95_teayoon_tyao', 'aditid_benli95_teayoon_tyao')

        print("hello from prepData2")

        ''' This commented out portion will be important for data visualisation later on '''

        #'''The following map reduce code takes the numberOfEstablishmentsinRadius and the numberOfEstablishmentsinRadiusDrug repos and returns a distribution of the number of crimes that have x children establishments within a certain proximity '''
        #
        ##find the number of crimes with the same number of establishments
        #map_function = Code('''function() {
        #    emit(this.total, {count:1, fake:0});
        #    }''')
        #
        #
        #reduce_function = Code('''function(k, vs) {
        #    var total = 0;
        #    for (var i = 0; i < vs.length; i++)
        #    total += vs[i].count;
        #    return {count:total, fake: 0};
        #    }''')
        #
        ##reset resulting directory
        #repo.dropPermanent('aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment')
        #repo.createPermanent('aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment')
        #
        #repo.aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadius.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment');
        #
        #
        ##find the number of drug crimes with the same number of establishments
        #
        #
        ##reset resulting directory
        #repo.dropPermanent('aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment')
        #repo.createPermanent('aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment')
        #
        #repo.aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadiusDrug.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment');


        '''The following map reduce code takes the numberOfEstablishmentsinRadius and the numberOfEstablishmentsinRadiusDrug repos and returns a distribution of the number of crimes that have x children establishments within a certain proximity as well as the product of the crimes by establishments and a temporary variable (temp) that will allow for the entire repo to be collapsed into a single key during the next map reduce '''


        map_function = Code('''function() {
            emit(this.total, {crimes:1, total:this.total, product:this.total, temp:5});
            }''')


        reduce_function = Code('''function(k, vs) {
            var total_crimes = 0;
            var tot = vs[0].total;
            
            for (var i = 0; i < vs.length; i++)
            total_crimes += vs[i].crimes;
            
            var prod = tot * total_crimes
            return {crimes:total_crimes, total:vs[0].total, product: prod, temp:5};
            }''')

        #reset resulting directory
        repo.dropPermanent('aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment')
        repo.createPermanent('aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment')

        repo.aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadius.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment');


        #reset resulting directory
        repo.dropPermanent('aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment')
        repo.createPermanent('aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment')

        repo.aditid_benli95_teayoon_tyao.numberOfEstablishmentsinRadiusDrug.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment');


        ''' This takes the previous map reduced repositories and returns the total sum of establishments around crimes and the number of crimes. Using these values the average number of establishments around each crime can be calculated.'''


        #find the number of crimes with the same number of establishments
        map_function = Code('''function() {
            for(var i in this.value) {
            emit(this.value[i].temp, {crimes:this.value.crimes, product:this.value.product});
            break;
            }
            }''')


        reduce_function = Code('''function(k, vs) {
            var total_crime = 0;
            var total_prod = 0;
            for (var i = 0; i < vs.length; i++)
            {
            total_crime += vs[i].crimes;
            total_prod += vs[i].product;
            }
            return {crimes:total_crime, product:total_prod};
            }''')

        #reset resulting directory
        repo.dropPermanent('aditid_benli95_teayoon_tyao.averageAll')
        repo.createPermanent('aditid_benli95_teayoon_tyao.averageAll')

        repo.aditid_benli95_teayoon_tyao.crimesPerNumberOfEstablishment.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.averageAll');

        #reset resulting directory
        repo.dropPermanent('aditid_benli95_teayoon_tyao.averageDrug')
        repo.createPermanent('aditid_benli95_teayoon_tyao.averageDrug')

        repo.aditid_benli95_teayoon_tyao.drugCrimesPerNumberOfEstablishment.map_reduce(map_function, reduce_function, 'aditid_benli95_teayoon_tyao.averageDrug');

        endTime = datetime.datetime.now()
        return {"Start ":startTime, "End ":endTime}

    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aditid_benli95_teayoon_tyao', 'aditid_benli95_teayoon_tyao')
        pass



prepData2.execute()
doc = prepData2.provenance()

