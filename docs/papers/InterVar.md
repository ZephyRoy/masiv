ARTICLE
InterVar: Clinical Interpretation of Genetic Variants
by the 2015 ACMG-AMP Guidelines
Quan Li1,4 and Kai Wang1,2,3,*
In2015,theAmericanCollegeofMedicalGeneticsandGenomics(ACMG)andtheAssociationforMolecularPathology(AMP)pub-
lishedupdatedstandardsandguidelinesfortheclinicalinterpretationofsequencevariantswithrespecttohumandiseasesonthebasis
of28criteria.However,variabilitybetweenindividualinterpreterscanbeextensivebecauseofreasonssuchasthedifferentunderstand-
ingsoftheseguidelinesandthelackofstandardalgorithmsforimplementingthem,yetcomputationaltoolsforsemi-automatedvariant
interpretationarenotavailable.Toaddresstheseproblems,weproposeasuiteofmethodsforimplementingthesecriteriaandhave
developedatoolcalledInterVartohelphumanreviewersinterprettheclinicalsignificanceofvariants.InterVarcantakeapre-annotated
orVCFfileasinputandgenerateautomatedinterpretationon18criteria.Furthermore,wehavedevelopedacompanionwebserver,
wInterVar,toenableuser-friendlyvariantinterpretationwithanautomatedinterpretationstepandamanualadjustmentstep.These
toolsareespeciallyusefulforaddressingseverecongenitalorveryearly-onsetdevelopmentaldisorderswithhighpenetrance.Usingre-
sultsfromafewpublishedsequencingstudies,wedemonstratetheutilityofInterVarinsignificantlyreducingthetimetointerpretthe
clinicalsignificanceofsequencevariants.
Introduction dividual scoring systems, such as SIFT,10 PolyPhen-2,11
CADD,12 FATHMM,13 and MutationTaster,14 as well as
With the continued development and deployment of meta-predictors,suchasCondel15andMetaSVM.16Many
massivelyparallelnext-generationsequencing(NGS)tech- haveasimilartheoreticalbasis,buttheyalsohaveknown
nologies, clinical and molecular laboratories are now limitations,suchasmoderateaccuracy,lowspecificity,and
rapidly adopting NGS in genetic testing and human ge- over-prediction.17,18 Third and finally, public disease-spe-
netics research. Although it is becoming easier and more cific and gene-specific databases, such as the Human
affordable for individual laboratories to generate NGS Gene Mutation Database (HGMD),19 ClinVar,20 and
data, the major hurdle in utilizing these data lies in how variouslocus-specificdatabases,21candocumentfunction-
to interpret the genotype-phenotype relationships, espe- ally or clinically validated genetic variants that are
ciallyingenomicmedicinesettings.1,2Theprocessofiden- pathogenicforparticulardiseases.TheHGMDisacompre-
tifying disease-causing or disease-contributing variants hensivecollectionofgermlinemutationsinnucleargenes
among the thousands of genetic variants within an indi- that underlie, or are associated with, human inherited
vidual’s genome generally involves a number of steps, diseaseandiscompiledprimarilyfromthepublishedliter-
suchasvariantannotation,variantfiltering,insilicopre- ature.19 ClinVar20 archives the clinical significance of
diction, and clinical interpretation by human experts.3 variantsreporteddirectlyfromsubmitters.However,these
Eachofthesestepscaninvolvetheuseofspecificcompu- databasesoftencontainvariantsthatareincorrectlyclassi-
tationalandbioinformaticstools. fiedwithoutaprimaryreviewofevidence,andtheysome-
Severaltoolsanddatabaseshavebeendevelopedtoassist times have contradictory records on the assessment of
laboratories and clinicians with understanding the func- pathogenicity.TheNIHbegantheClinGeninitiative22to
tionalsignificanceofgeneticvariantswithrespecttotheir build an authoritative central resource that defines the
potentialeffectsongenesanddiseases.Theygenerallyfall clinicalrelevanceofgenesandvariantsforuseinprecision
intoseveralcategories.First,anumberofannotationtools, medicineandresearch.Toimprovetheaccuracyofvariant
such as ANNOVAR,4,5 VAAST,6 SeattleSeq,7 SNPeff,8 and interpretations, ClinGen uses a ranking system to denote
VEP,9 can predict how genetic variants affect transcript the quality associated with each submission to ClinVar.
structure or coding sequences. They can classify variants Despitetheexistenceofavarietyofresources,amoresys-
into intronic, intergenic, splice, and exonic variants, and tematicwaytoevaluatethepathogenicityofgeneticvari-
forexonicvariants,theycancomputehowaminoacidse- antsobservedinsequencingstudiesisneededtofacilitate
quencesareaffected.Second,forcodingvariants,avariety clinicalevaluationofvariantsandtoenablethepreciseim-
of tools can predict whether the variant is deleterious to plementationofgenomicmedicine.
proteinfunctionorstructurebyusingevolutionaryinfor- To standardize the clinical interpretation of genetic
mation, context within the protein sequence, and variants, the American College of Medical Genetics and
biochemicalproperties.Theseinsilicomethodsincludein- Genomics (ACMG) recommended standards for the
1ZilkhaNeurogeneticInstitute,UniversityofSouthernCalifornia,LosAngeles,CA90089,USA;2InstituteforGenomicMedicine,ColumbiaUniversity,
NewYork,NY10032,USA;3DepartmentofBiomedicalInformatics,ColumbiaUniversity,NewYork,NY10032,USA
4Presentaddress:FacultyofMedicine,MemorialUniversityofNewfoundland,St.John’s,NLA1B3V6,Canada
*Correspondence:kw2701@cumc.columbia.edu
http://dx.doi.org/10.1016/j.ajhg.2017.01.004.
(cid:1)2017AmericanSocietyofHumanGenetics.
TheAmericanJournalofHumanGenetics100,267–280,February2,2017 267

interpretation of sequence variations and offered a deci- a tool, InterVar (Clinical Interpretation of Genetic Vari-
sion-treealgorithmforvariantinterpretationin2000and ants), to fill these unmet needs on the basis of the
2007.23,24 With the rapid development and adoption of 2015 ACMG-AMP guidelines and user-supplied domain
| NGS, variant |     | interpretation |     | has | become | more | complex, | knowledge. |     |     |     |     |     |     |
| ------------ | --- | -------------- | --- | --- | ------ | ---- | -------- | ---------- | --- | --- | --- | --- | --- | --- |
andnewchallengesintheclinicalinterpretationofMen-
| delian | and complex |     | diseases | have | emerged. |     | To address |     |     |     |     |     |     |     |
| ------ | ----------- | --- | -------- | ---- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
thesechallengesandtoprovidemoreconcreteguidelines, Material and Methods
| the ACMG | and | the | Association |     | for Molecular |     | Pathology |     |     |     |     |     |     |     |
| -------- | --- | --- | ----------- | --- | ------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
(AMP)publishedupdatedguidelinesfortheinterpretation GenerationofVariantAnnotation
ofsequencevariantsinMayof2015.25Thisnewreportde- The required input for InterVar is a simple tab-delimited file
includingalistofvariantsthatarealreadyannotatedwithaset
| scribes | updated | standards |     | and guidelines |     | for | classifying |     |     |     |     |     |     |     |
| ------- | ------- | --------- | --- | -------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ofrequiredinformation,suchasaminoacidchangesandallelefre-
| sequence | variants | by  | using | criteria | informed |     | by expert |     |     |     |     |     |     |     |
| -------- | -------- | --- | ----- | -------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
quency.Userscangeneratethisinputfilethemselvesbyusingan
| opinion     | and        | experience. | To       | better     | describe | the  | causality |            |         |          |           |                |             |     |
| ----------- | ---------- | ----------- | -------- | ---------- | -------- | ---- | --------- | ---------- | ------- | -------- | --------- | -------------- | ----------- | --- |
|             |            |             |          |            |          |      |           | in-house   | variant | analysis | workflow; | alternatively, | InterVar    | can |
| of variants | identified |             | in genes | associated |          | with | Mendelian |            |         |          |           |                |             |     |
|             |            |             |          |            |          |      |           | take a VCF | file,   | call the | ANNOVAR   | software       | (a powerful | and |
diseases, the ACMG and AMP recommend a widely used widely used annotation tool), and generate the required input
five-tieredcategorizationsystem—pathogenic,likelypath- data. The following is an example command line for running
ogenic,uncertainsignificance,likelybenign,andbenign—
ANNOVAR:‘‘perltable_annovar.plinput.vcfhumandb/-buildver
for classifying variants. The system uses a total of 28 hg19 -remove -out output -protocol refGene,esp6500siv2_all,
criteriabasedondifferentsourcesofdata,suchaspopula- 1000g2015aug_all,avsnp144,dbnsfp30a,clinvar_20160302,exac03,
|            |      |              |            |      |         |                 |            | dbscsnv11,dbnsfp31a_interpro,rmsk,ensGene,knownGene |     |            |              |     |                 | -oper- |
| ---------- | ---- | ------------ | ---------- | ---- | ------- | --------------- | ---------- | --------------------------------------------------- | --- | ---------- | ------------ | --- | --------------- | ------ |
| tion data, | in   | silico data, | functional |      | data,   | and segregation |            |                                                     |     |            |              |     |                 |        |
|            |      |              |            |      |         |                 |            | ation g,f,f,f,f,f,f,f,f,r,g,g                       |     | -nastring. | -vcfinput.’’ |     | The description | for    |
| data. The  | ACMG | and          | AMP        | also | propose | a set           | of scoring |                                                     |     |            |              |     |                 |        |
rules,whichcombinecriteriatogivethefive-tierclassifica- these databases is given below: ‘‘esp6500siv2_all’’ is a database
|     |     |     |     |     |     |     |     | for allele | frequency | in the | NHLBI | Exome | Sequencing | Project |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | ------ | ----- | ----- | ---------- | ------- |
tionsystemforgeneticvariants.
|     |     |     |     |     |     |     |     | (ESP6500), | ‘‘refGene’’ | is a | database | for gene | annotation | from |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | ---- | -------- | -------- | ---------- | ---- |
AlthoughtheACMG-AMPguidelinesweredevelopedto
RefSeq,‘‘1000g2015aug_all’’isadatabaseforalternativeallelefre-
enable consistent and reliable interpretation of genetic quency (AAF) in the 1000 Genomes Project27 (version August
| variants, | application |     | of the | ACMG-AMP |     | criteria | still in- |     |     |     |     |     |     |     |
| --------- | ----------- | --- | ------ | -------- | --- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- |
2015),‘‘exac03’’isadatabaseforAAFintheExomeAggregation
volvessomediscrepanciesbetweenintra-andinter-labora- Consortium(ExAC)Browser28(version0.3),‘‘dbnsfp30a’’isadata-
tory settings. Some efforts have been taken to reduce baseforvariousfunctionaldeleteriousnesspredictionscoresfrom
inter-laboratory inconsistencies,26 but >66% of variant dbNSFP29,30(version3.0a),‘‘clinvar_20160302’’isforthevariants
classificationsarestilldiscordantininter-laboratoryclassi- reportedin ClinVar20 (version20160302), ‘‘avsnp144’’ isfor the
fications. There could be several reasons for the discor- ANNOVAR-compileddbSNP(version144),‘‘ensGene’’isforgene
dances. For many clinical labs, implementing the variant annotationfromEnsembl,‘‘knownGene’’isforgeneannotation
fromUCSCKnownGenes,‘‘dbnsfp31a_interpro’’isadatabaseof
| scoring | rules | into | a standardized |     | workflow |     | is difficult |     |     |     |     |     |     |     |
| ------- | ----- | ---- | -------------- | --- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
thedomaininformationfromdbNSFP29,30andInterPro31(which
| with available |     | informatics |     | tools. | For example, |     | the ACMG |     |     |     |     |     |     |     |
| -------------- | --- | ----------- | --- | ------ | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
integratesinformationaboutproteinfamilies,domains,andfunc-
| and AMP | recommend |     | using | 28  | criteria | during | the inter- |     |     |     |     |     |     |     |
| ------- | --------- | --- | ----- | --- | -------- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
tionalsites),‘‘dbscsnv11’’isadatabaseforpredictingthesplicing
pretation process; however, gathering information on impactbyAdaBoostandRandomForest,32and‘‘rmsk’’isadata-
| each of | the criteria |     | is quite | complicated |     | and | might not |     |     |     |     |     |     |     |
| ------- | ------------ | --- | -------- | ----------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
baseontherepeatmaskingtrackfromtheUCSCGenomeBrowser.
beeasilyaccomplishedbyindividualinterpretersormight These databases might be updated to new versions when they
| not be              | reproducible |     | by the   | same      | interpreter | at        | different | becomeavailable. |     |     |     |     |     |     |
| ------------------- | ------------ | --- | -------- | --------- | ----------- | --------- | --------- | ---------------- | --- | --- | --- | --- | --- | --- |
| times. Furthermore, |              |     | the ACMG |           | and AMP     | provide   | only      |                  |     |     |     |     |     |     |
| general             | guidelines   | on  | how      | to assess | each        | criterion | but       |                  |     |     |     |     |     |     |
CriteriaandScoringSystem
| do not | offer | specific | algorithms |     | for implementing |     | these |          |          |          |             |     |              |           |
| ------ | ----- | -------- | ---------- | --- | ---------------- | --- | ----- | -------- | -------- | -------- | ----------- | --- | ------------ | --------- |
|        |       |          |            |     |                  |     |       | Based on | the 2015 | ACMG-AMP | guidelines, |     | the criteria | fall into |
guidelines(forexample,whichdatabasestouse);different two sets: pathogenic or likely pathogenic (P/LP) and benign or
researchersmightprefertousedifferentalgorithms,mak- likelybenign(B/LB),whereas‘‘uncertainsignificance’’isassigned
ingtheresultslessreproduciblebetweendifferenthuman
tovariantsforwhichthecriteriaforP/LPandB/LBarecontradic-
interpreters.Finally,althoughavarietyofdatabases(such toryornotmet.Thereareatotalof28criteria:the16criteriafor
as ClinVar and the 1000 Genomes Project) or in silico theP/LPcriterionareverystrong(PVS1),strong(PS1–PS4),moder-
ate(PM1–PM6),orsupporting(PP1–PP5);whereasthe12criteria
| tools (such | as  | SIFT | and PolyPhen-2) |     | are | available | online |     |     |     |     |     |     |     |
| ----------- | --- | ---- | --------------- | --- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
fortheB/LBcriterionarestand-alone(BA1),strong(BS1–BS4),or
| and easily | accessible |     | to the | average | user, | there | is a lack |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | ------ | ------- | ----- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
of tools that combine all of these databases together to supporting(BP1–BP7).Ifacriterionispositive,InterVarwillassign
1;otherwise,InterVarwillassign0.Forthese28criteria,InterVar
| offer a     | one-stop     | shop    | for         | human | interpreters |       | to derive | a                 |      |           |             |      |           |           |
| ----------- | ------------ | ------- | ----------- | ----- | ------------ | ----- | --------- | ----------------- | ---- | --------- | ----------- | ---- | --------- | --------- |
|             |              |         |             |       |              |       |           | can automatically |      | generate  | predictions | on   | 18 (PVS1, | PS1, PS4, |
| final score | for          | genetic | variants.   |       | Addressing   | these | chal-     |                   |      |           |             |      |           |           |
|             |              |         |             |       |              |       |           | PM1, PM2,         | PM4, | PM5, PP2, | PP3, PP5,   | BA1, | BS1, BS2, | BP1, BP3, |
| lenges      | will require |         | easy-to-use | yet   | automated    |       | computa-  |                   |      |           |             |      |           |           |
BP4,BP6,andBP7)accordingtothecurrentannotationdatasets,
| tional tools     | and | web      | services | that      | can generate |     | versioned |              |       |           |            |            |           |              |
| ---------------- | --- | -------- | -------- | --------- | ------------ | --- | --------- | ------------ | ----- | --------- | ---------- | ---------- | --------- | ------------ |
|                  |     |          |          |           |              |     |           | yet the rest | (PS2, | PS3, PM3, | PM6, PP1,  | PP4,       | BS3, BS4, | BP2, and     |
| and reproducible |     | criteria |          | for every | variant      | and | help hu-  |              |       |           |            |            |           |              |
|                  |     |          |          |           |              |     |           | BP5) require | user  | input in  | the manual | adjustment |           | step. Below, |
man interpreters quickly understand the clinical signifi- wedescribethedetailsonhowtoassignthesecriteriafromvarious
cance of genetic variants. In this study, we present such sourcesofannotationinformation.
268 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

PVS1byAutomatedScoring datasets to assess the variant frequency: the NHLBI Exome
Thenullvariantsincludenonsensevariants,frameshiftindels,and SequencingProject(ESP6500),1000GenomesProject,andExAC
canonical splice variants, which often lead to loss of function Browser.IfanyoftheAAFsinanydatabaseis>5%,BA1willbeas-
(LOF).FromANNOVARannotations,theseLOFvariantsarerepre- signedas1.IftheAAFintheExACBrowserisgreatthanexpected
sentedasframeshiftindel,stop-gain,stop-loss,andsplicingvari- forthedisordercausedbymutationsinthecorrespondinggene,
ants in canonical transcripts. We first filtered ClinVar (version BS1willbeassignedas1(here,wesetadefaultcutoffas1%for
20160302)bytakingthosevariantsshowninMedGenandthen raredisease,butuserscanspecifytheirowncutoffintheconfigu-
removingcommonvariants(allelefrequencies>5%)andvariants rationfileofInterVar).Ifavariantisobservedinahealthyadultin
withconflictingannotations.ThevariantsinClinVarwereanno- the1000GenomesProjectasahomozygote(fordiseasesdefinedas
tatedbyANNOVARwithRefGenedefinitions,andweidentified recessiveinOMIM)orasaheterozygoteotherwise,thenBS2will
1,988 genes harboring at least one LOF variant that is ‘‘patho- beapplied.Wemanuallyremovedknownmajoradult-onsetdisor-
genic’’ in ClinVar. Recently, the ExAC analyzed high-quality ders from consideration. We did not use the ExAC Browser or
exome(protein-codingregion)DNAsequencedatafor60,706in- ESP6500herebecausethesedatasetscancontainvariantsfromin-
dividualsandidentified3,230genesasLOFintolerant.28Wecom- dividualswithvariousdiseases.
binedthesetwogenesetsfromClinVarandtheExACBrowserand Variants that are absent or are present at extremely low fre-
generated4,807genesasourfinalLOF-intolerantgenelist.Null quenciesinalargecontrolcohortcouldrepresentmoderateevi-
variants in the canonical transcripts for these 4,807 genes were dence for pathogenicity. If a variant that is responsible for
assignedaPVS1of1.However,onthebasisofthecanonicalrules dominant diseases is absent in all control subjects from
for nonsense-mediated mRNA decay,33 we did not consider ESP6500, 1000 Genomes Project, and the ExAC Browser, PM2
nonsense variants that are downstream of or within 50 nucleo- willbeapplied.Ifthevariantcausesrecessivediseasesandhasa
tidesofthefinalexon-junctioncomplex. very low frequency with AAF < 0.5%, then PM2 can also be
PS1andPM5byAutomatedScoring applied. Information on the gene-disease relationship, such as
Generallyspeaking,ifonemissensevariantispathogenic,thena dominanceorrecessiveness,isobtainedfromOMIM.
different nucleotide changethat resultsin the same amino acid Insomecases,pathogenicvariantshaveasignificantlyhigher
alteration should also be pathogenic for PS1. However, if a frequencyinaffectedsubjectsthanincontrolsubjects.Tohandle
different nucleotide change results in a different amino acid these variants, we also cataloged all variants with an odds ratio
change, then it suggests moderate evidenceof pathogenicity by (OR) > 5.0 from GWASdb34 version 2. For these variants, PS4
PM5.WefirstfilteredClinVar(subjecttothesamedata-cleaning willbeapplied.Forsomerarevariantswherecase-controlstudies
proceduredescribedabove),pickedoutallmissensevariantsanno- might not reach statistical significance, PS4 also can be down-
tated as pathogenic, and stored the amino acid changes in an gradedtoamoderatelevelduringthemanualadjustmentstep.
InterVar-specific database. We also inferred the splicing impact PM1byAutomatedScoring
of these exonic missense variants by ANNOVAR from the Manyproteindomainsplayessentialrolesforproteinfunction,so
‘‘dbscsnv11’’ database to assess the possibility that they act missense variants in these domains tend to be pathogenic. The
throughsplicingdisruptionratherthanaminoacidchanges.Ifa domaininformationcanbeinferredfromdbNSFPbyANNOVAR
variantsuppliedbytheuserresultsinthesameaminoacidchange, through the ‘‘dbnsfp31a_interpro’’ database. We first annotated
thePS1valuewillbeassignedas1.However,ifavariantsupplied allClinVarvariants(subjecttothesamedata-cleaningprocedure
bytheuserresultsinadifferentaminoacidchange,thenPM5will described above) with protein-domain information and then
beassignedas1. compiledalistinwhichdomainscontainedonlypathogenicor
PS2andPM6byManualScoring likelypathogenicvariantswithoutbenignorcommon(allelefre-
The de novo status of the variants gives strong support for the quency>5%)variants.ThislistisprovidedwithintheInterVar
pathogenicstatusforPS2ifbothmaternityandpaternitycanbe packageandwillbeupdatedregularly.Iftheuser’sinputvariants
confirmed;ifmaternityorpaternityisnotconfirmed,thenmoder- arelocatedinthesedomains,thenPM1willbeapplied.
ateevidenceofpathogenicityshouldbeappliedtoPM6.Because PM3andBP2byManualScoring
InterVarcannotdirectlyannotatethedenovostatusoftheuser’s Thepathogenicityofavariantalsoneedstobeevaluatedonthe
inputvariants,PS2andPM6aretreatedasuser-suppliedvaluesin basis of whether variants with known pathogenicity exist in cis
thesecondstep(manualadjustment)ofInterVar. ortranswithit.InterVardoesnotknowthecis/transstatusforvar-
PS3andBS3byManualScoring iants, so this needs to be provided by users in the second step
If in vitro or in vivo functional studies are supportive of a (manual adjustment) of InterVar. For two heterozygous variants
damagingeffectonthegeneorgeneproduct,PS3shouldbeas- that are present in a gene associated with recessive disorders, if
signed as 1. If in vitro or in vivo functional studies show no oneispathogenicandtheotherislocatedintrans,thenmoderate
damagingeffectonproteinfunctionorsplicing,BS3shouldbeas- evidence of PM3 will be applied. If more than two variants are
signedas1.InterVardoesnothavetheinformationonfunctional observedintrans,thenmoderateevidenceforpathogenicitycan
studies,sobydefaultthesevaluesare0andcanbeoverriddenby beupgradedtostrong.Ifthevariantsarepresentinageneassoci-
users.Inthefuture,wemightestablishadatabasewithvalidated atedwithdominantdiseases,yetonevariantispathogenicandthe
genetic variants that are known to affect the function of genes otherislocatedintrans,thensupportingevidenceofbenignstatus
orgeneproducts. willbeappliedtoBP2fortheothervariant.Regardlessofmodelsof
BA1,BS1,BS2,PS4,andPM2byAutomatedScoring diseaseinheritance,fortwovariants,ifoneispathogenicandthe
TheAAFsincontrolpopulationsareusefulforscoringthepatho- other is observed in cis, then BP2 will be applied for the other
genicityofvariants,giventhatfrequentlyoccurringvariantsinthe variant.
populationareunlikelytocauserarediseases.Weretrievedinfor- PM4andBP3byAutomatedScoring
mation on disease prevalence from OrphaNet and translated Indels and stop losses can change the length of proteins and
OrphaNetidentifiersintoOMIMidentifiers.Here,weusedthree disruptproteinfunction.Weannotatedtherepeatregionbyusing
TheAmericanJournalofHumanGenetics100,267–280,February2,2017 269

the‘‘rmsk’’databasefromtheUCSCGenomeBrowser.Thisdata- supportingevidenceforpathogenicity;insuchacase,PP4should
base was created by the RepeatMasker program, which screens beapplied.Thisinformationneedstobeprovidedbytheuserin
DNA sequences for interspersed repeats and low-complexity thesecondstep(manualadjustment)ofInterVar.
DNA sequences. When the variants are ‘‘non-frameshift inser- PP5andBP6byAutomatedScoring
tion,’’ ‘‘non-frameshift deletion’’ in the non-repeat region, or Ifareputablesourcehasalreadyreportedavariantaspathogenic
stop-lossvariants,PM4willbeapplied.Ifthevariantsare‘‘non- but the evidence is not provided for independent evaluation,
frameshiftinsertion’’or‘‘non-frameshiftdeletion’’intherepeatre- thenPP5willbeapplied.Whenareputablesourcehasalreadyre-
gion,BP3willbeapplied. portedabenignvariantbutwithoutdetailedevidence,thenBP6
PP1andBS4byManualScoring willbeapplied.InInterVar,weusedtheClinVardataset(subject
Familialsegregationofavariantwithadiseaseisanimportantsign tothesamedata-cleaningproceduredescribedabove)toperform
for linking the variant to the disease. If segregation is found in thisanalysisbydefault,butuserscanselecttouseHGMDorother
multipleaffectedfamilymembersandifthisgeneisdefinitively proprietarydatabasesforthisanalysis.
knowntobeassociatedwiththisdisease,thenPP1willbeapplied. BP5byManualScoring
Whenthereisalackofsegregationinaffectedmembersofafam- Ifadiseasehasanalternatemolecularbasis(causedbymorethan
ily,thenthebenignsupportingevidenceofBS4willbeapplied. onegene)andifavariantisobservedinagenerelatedtothedis-
BecauseInterVardoesnotknowtheinformationonsegregation, ease,thenitwillbesupportingevidenceforabenignstatus,and
this piece of evidence can be provided by users in the second BP5willbeassignedas1.Notethatthiscriterionisstrongerfor
step(manualadjustment)ofInterVar. a gene associated with a dominant disorder than for a gene
PP2andBP1byAutomatedScoring associated with a recessive disorder. Because of the multiple
Formanygenes,thespectrumordistributionofpathogenicand exceptionsforthiscriterion,asdescribedbefore,25userscanadjust
benignvariantscanbeinformativeforthepathogenicitystatus. thiscriterionbyusingtheirownknowledgeinthemanualadjust-
Foragivengene,ifthemissensevariantsarecommoncausesof mentstep.
the disorder and the gene also has very few benign variants, BP7byAutomatedScoring
thenamissensevariantinthisgenecanbesupportingevidence Ifasynonymous(silent)varianthasnoeffectonsplicingandifthe
forpathogenicity,andPP2willbeapplied.However,ifthetrun- nucleotidepositionisnothighlyconserved,thenwecanclassify
cating variants are major causes of the disease, then a missense thisvariantaslikelybenignandassignBP7as1.Theprediction
variantinthisgenecanbesupportingevidenceforabenignstatus, on the effect on splicing can be extracted by ANNOVAR with
andBP1willbeapplied. the ‘‘dbscSNV’’ database. Both scores dbscSNV_RF_SCORE and
WeannotatedallvariantsinClinVar(subjecttothesamedata- dbscSNV_ADA_SCORE should be <0.6 when the variant is pre-
cleaningproceduredescribedabove).Foragivengene,ifmostof dictedtohavenoimpactonsplicing.Theconservationinforma-
the pathogenic variants (>80% and at least one variant) are tionisretrievedfromthe‘‘dbnsfp30a’’database,whereaGERPþþ
missense, and if a small proportion (<10% and less than one score>2indicatesthatthenucleotideishighlyconserved.
variant)ofmissensevariantsarebenign,thenformissensevari-
ants,PP2willbe assignedas1. Thetreatmentfor BP1issimilar
tothatforPP2,butweassesswhethermostofpathogenicvariants InterVarandwInterVar
(>80%andatleastonevariant)aretruncatingvariants.Thetrun-
InterVarisacommand-line-drivensoftwarewritteninPythonand
catingvariantsaredefinedasstop-gain,stop-loss,frameshiftindel, canbeusedasastandaloneapplicationonavarietyofoperating
orthosedisruptingsplicesites.Iftheuser’svariantsaremissensein systems—includingWindows,Linux,andMacOS—wherePython
thisgene,BP1willbeassignedas1. isinstalled.ThesourcecodeofInterVarisavailablefromGitHub
PP3andBP4byAutomatedScoring (seeWebResources).
Whenmultiplepiecesofcomputationalevidencesupportadelete- InterVartakeseitherpre-annotatedfilesintab-delimitedformats
rious effect on the gene or gene product (conservation, evolu- or unannotated input files in VCF format or ANNOVAR input
tionary, splicing impact, etc.), then the supporting pathogenic format, where each line corresponds to one genetic variant. If
evidenceofPP3willbeassignedas1.Incomparison,whenmulti- the input files are unannotated, InterVar will call ANNOVAR to
ple pieces of computational evidence suggest no impact on the generatenecessaryannotations.Userscanalsousesoftwaretools
gene or gene product, then supporting benign evidence of BP4 otherthanANNOVARtogeneratepre-annotatedfiles.Theexecu-
willbeassignedas1.Allsetsofinsilicoresultsmustagreewhen tionofInterVarmainlyconsistsoftwomajorsteps:(1)automati-
PP3orBP4isassigned. callyinterpretingthevariantbyusingthecriteriaoutlinedabove
These multiple pieces of computational evidence can be pro- and(2)manuallyadjustingspecificcriteriatore-interprettheclin-
vided by ANNOVAR from the ‘‘dbnsfp30a’’ database, where the ical significance. However, users can also specify their own evi-
MetaSVM score16 is used for deleteriousness prediction and dencefileforasubsetofthecriteriaandimportitintoInterVar
GERPþþisusedforevolutionaryconservation.Thesplicingim-
byusingtheargument‘‘-evidence_file’’sothatonesinglestepis
pacts can be inferredby ANNOVAR from the‘‘dbscsnv11’’ data- sufficienttogeneratethefinalresults.Intheoutput,onthebasis
base. For the evidence of PP3 and BP4, we set the cutoff to 0.0 ofall28piecesofcriteriathatareeitherautomaticallygeneratedor
forMetaSVMscores(greaterscoresindicatemorelikelydeleterious manually supplied by the user, each variant will be assigned as
effects),2.0forGERPþþ_RS(smallerscoresindicatelessconserva-
pathogenic, likely pathogenic, uncertain significance, likely
tion),and0.6foradaptiveboosting(ADA)andrandomforest(RF) benign, or benign by rules specified in the 2015 ACMG-AMP
scoresofdbscSNVassplicingimpact(largerscoresindicatemore guidelines.25
likelysplicealtering). WealsodevelopedawebservercalledwInterVar,whichoffersa
PP4byManualScoring graphicaluserinterfaceforInterVar(seeWebResources).Userscan
Foragivengene,iftheindividual’sphenotypeorfamilyhistoryis directlyinputtheirmissensevariantsintowInterVarbychromo-
highlyspecifictothedisorderassociatedwiththegene,thenitis somal position, by dbSNP identifier, or by gene name with the
270 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

| Figure1. | FlowchartoftheTwo-StepProcedureofInterVar |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Underlinedandboldfontsdenoteautomatedcriteria.
nucleicacidchange.ThewInterVarserverwillprovidefulldetails of the variant and presents all relevant evidence for
on the variants, including all automatically generated criteria, manualreview.Currently,18piecesofcriteriacanbeauto-
mostofthesupportiveevidence,andsub-populationinformation. maticallygeneratedandusedinthefirststep.Duringthe
Usersthenhavetheabilitytomanuallyadjustthesecriteriaand
|            |           |                              |     |           |           |            | second   | step, the    | user | can manually      | adjust | each     | of the  |
| ---------- | --------- | ---------------------------- | --- | --------- | --------- | ---------- | -------- | ------------ | ---- | ----------------- | ------ | -------- | ------- |
| resubmitto | theserver | to performre-interpretation. |     |           |           | We scanned |          |              |      |                   |        |          |         |
|            |           |                              |     |           |           |            | criteria | on the basis | of   | prior information |        | (such as | a vari- |
| all exons, | and for   | each position                | we  | generated | all three | possible   |          |              |      |                   |        |          |         |
ant’sdenovostatus)orhisorherowndomainknowledge
| nucleotide        | changes.      | If the mutation |       | was       | non-synonymous, | we       |           |         |                 |            |           |            |      |
| ----------------- | ------------- | --------------- | ----- | --------- | --------------- | -------- | --------- | ------- | --------------- | ---------- | --------- | ---------- | ---- |
|                   |               |                 |       |           |                 |          | to reach  | a final | interpretation. | We         | emphasize | here       | that |
| kept it in        | our database. | The             | human | genome    | contains        | approxi- |           |         |                 |            |           |            |      |
|                   |               |                 |       |           |                 |          | automated | scoring | is based        | on default |           | parameters | and  |
| mately 80,000,000 |               | non-synonymous  |       | variants, | and             | we pre-  |           |         |                 |            |           |            |      |
computedthe18criteriaforallofthem.Therefore,theexecution that users are advised to examine detailed evidence and
ofwInterVarisveryfast,typicallylessthan1stoobtaintheresult usepriorknowledgeonethnicityand/ordiseasetoperform
|     |     |     |     |     |     |     | manual | adjustments. | A   | detailed explanation |     | of  | these 28 |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | --- | -------------------- | --- | --- | -------- |
onavariant.However,thewInterVarservercannotprocessother
typesofvariants(suchasindels),andtheuserwillneedtorelyon criteriaisgiveninFigure2.
InterVarinstead. For example, consider missense variant chr12:
52,093,447T>C(GRCh37coordinate)inexon7ofSCN8A
|         |     |     |     |     |     |     | (MIM: 600702),                                    |      | which   | causes early | infantile       | epileptic | en-    |
| ------- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | ---- | ------- | ------------ | --------------- | --------- | ------ |
| Results |     |     |     |     |     |     | cephalopathytype13(MIM:614558).Werecentlyreported |      |         |              |                 |           |        |
|         |     |     |     |     |     |     | thisvariant                                       | as a | de novo | mutation     | in a 4-year-old |           | female |
SummaryoftheInterpretationProcedure who,at5monthsofage,exhibitedsymptomsofepilepsy
A flowchart for InterVar is given in Figure 1. InterVar that progressed to a severe condition with very little
mainlyconsistsoftwomajorsteps:(1)automatedscoring movement, including the inability to sit or walk on her
oneachofthe18piecesofcriteriaand(2)manualreview own.35 We illustrate the scoring logic for this variant.
andadjustmentonspecificcriteriatoarriveatafinalinter- This variant is located in a protein domain called the
pretation. During the first step, InterVar calls an annota- ion transport domain. This domain does not have any
tion software, such as ANNOVAR,5 to obtain necessary benignvariantsinpublicdatabasescompiledbyInterVar,
annotation information on variants and then uses its so we assigned PM1 as 1. In addition, this variant is not
own internal annotation database to supplement addi- present in the 1000 Genomes Project, ExAC Browser, or
SCN8A,
tional annotations. Using these annotations on variants ESP6500, so PM2 was assigned as 1. For all
andgenes,InterVarperformsapreliminaryinterpretation known pathogenic variants are missense, so PP2 was
|     |     |     |     |     |     | TheAmericanJournalofHumanGenetics100,267–280,February2,2017 |     |     |     |     |     |     | 271 |
| --- | --- | --- | --- | --- | --- | ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |

Figure2. Illustrationofthe28Criteriafromthe2015ACMG-AMPGuidelines
Forsomecriteria,thenameoftheinternaldatabaseanditssizearedenotedwithinparentheses.
assigned as 1. According the 2015 ACMG-AMP rules, the changes in 3,462 genes, whereas 616 non-synonymous
variant falls into the class of ‘‘uncertain significance.’’ In variantswerepresentin592genesfromcontrolsubjects.
the second step, if we manually adjust the criteria by Wenextperformedautomatedvariantinterpretationby
providingdenovoinformationasPS2¼1,thentheclin- InterVaronallofthesevariantsbyusingdefaultoptionsin
icalsignificancewillchangeto‘‘likelypathogenic’’onthe theprogramandsettingexpectedprevalenceforthesedis-
basis of ‘‘1 strong (PS1–PS4) and 1–2 moderate (PM1– orders as 1% (Table 1). Given that each published exome
PM6).’’ This procedure illustrates how to use automated sequencing study used Sanger sequencing to validate the
interpretation and manual adjustment to derive a final denovostatusofthevariants,weassignedPM6as1,indi-
interpretation for genetic variants. cating that these variants were assumed to be de novo
without confirmed paternity or maternity. Among these
InterpretationofDeNovoVariantsin variants,4,459(53.4%)and493(51.4%)wereinterpreted
NeurodevelopmentalDisorders as having uncertain significance in affected and control
We compiled a dataset of 9,305 de novo variants from subjects, respectively. Among affected subjects, 430
12 published trio-based exome sequencing studies on (5.1%) and 1,666 (20.0%) variants were interpreted as
autism spectrum disorders,36,37 developmental disor- pathogenic and likely pathogenic, respectively. Among
ders,38 schizophrenia,39–42 epileptic encephalopathies,43 control subjects, 10 (1.0%) and 206 (21.5%) variants
and intellectual disability.44–47 Among them, 8,346 vari- were interpreted as pathogenic and likely pathogenic,
ants were detected from affected subjects (n ¼ 6,515), respectively.
and 959 were detected from control subjects (n ¼ 900). We next combined variants with a benign or likely
Amongthese8,346variantsfrom affectedsubjects,4,526 benign interpretation as one category (B/LB) and those
were non-synonymous, resulting in coding sequence withpathogenic or likely pathogenic asanothercategory
272 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

Table1. IllustrationofAutomatedInterpretationofDeNovoVariantsfromIndividualswithSeveralDifferentDiseasesandControl
Subjects
|                       |       |     |       |     |     | Affected | Control  |
| --------------------- | ----- | --- | ----- | --- | --- | -------- | -------- |
| Interpretation        | DD    | SCZ | ASD   | EE  | ID  | Subjects | Subjects |
| Benign                | 7     | 3   | 52    | 0   | 0   | 62       | 0        |
| Likelybenign          | 288   | 241 | 1,085 | 59  | 56  | 1,729    | 250      |
| Uncertainsignificance | 819   | 466 | 2,869 | 180 | 125 | 4,459    | 493      |
| Likelypathogenic      | 339   | 199 | 967   | 81  | 80  | 1,666    | 206      |
| Pathogenic            | 125   | 26  | 226   | 17  | 36  | 430      | 10       |
| Total                 | 1,578 | 935 | 5,199 | 337 | 297 | 8,346    | 959      |
| Benignandlikelybenign | 295   | 244 | 1,137 | 59  | 56  | 1,791    | 250      |
| Pathogenicandlikely   | 464   | 225 | 1,193 | 98  | 116 | 2,096    | 216      |
pathogenic
pvalue(comparedto 4.71E(cid:2)7 0.65 0.06 0.00061 2.07E(cid:2)6 0.0022 –
controlsubjects)a
ORand95%CI 0.55(0.44–0.69) 0.94(0.72–1.21) 0.82(0.67–1.00) 0.52(0.35–0.75) 0.42(0.29–0.60) 0.74(0.61–0.90) –
Abbreviationsareasfollows:DDD,developmentaldisorder;SCZ,schizophrenia;ASD,autismspectrumdisorder;EE,epilepticencephalopathy;ID,intellectual
disability;OR,oddsratio;andCI,confidenceinterval.
apvalueswerecalculatedwithatwo-sidedFisher’sexacttest.
(P/LP)andcomparedtheirfrequencybetweenaffectedand ComparativeAnalysisonClinVar
controlsubjects.(Pleasenotethatwedonothaveaccessto Although variant databases such as HGMD, ClinVar, and
individual-level data, so our analysis below focused on OMIMhavebeenveryhelpfulforcataloginggeneticvari-
comparingdetectedvariantsbetweenaffectedandcontrol ants known to be associated with human diseases, they
subjects.) Using Fisher’s exact test, we detected a strong alsohaveknownlimitations,e.g.,thataportionofbenign
enrichment of P/LP variants among de novo variants in variants are incorrectly classified as pathogenic vari-
affected subjects (p ¼ 0.0022) on the basis of automated ants.48,49Forexample,Dorschneretal.50manuallyexam-
interpretation. This result confirms that de novo variants ined primary literature for 239 unique variants reported
that might be pathogenic are more prevalent in subjects as pathogenic in HGMD and confirmed that only 7.5%
with neurodevelopmental disorders than in control sub- are actually pathogenic from the original publication.
jects. Please note that this analysis leveraged results only The discrepancy in variant clinical significance between
from automated interpretation (step 1) and did not ac- HGMD and clinical labs also highlights the lack of stan-
countformanualadjustment(step2)basedonadditional dardsininterpretingavariantaspathogenicorlikelypath-
domainknowledgeofthevariants,genes,phenotypes,or ogenic in the literature. Similarly, Bell et al.51 found that
diseases. 27% of the pathogenic variants cited in the literature are
In comparison, we also predicted the pathogenicity common polymorphisms or misannotated, underscoring
of these variants by using SIFT and PolyPhen-2 scores the need for better mutation databases. Interestingly, we
on a subset of the variants for which the scores were recentlysequencedapersonalgenomeandidentifiedtwo
available (Table 2). SIFT predicted 2,242 (26.8%) of variantsreportedaspathogenicinClinVar,butmanualex-
<
8,346 variants as deleterious (SIFT 0.05 as the cutoff) amination of the cited publication indicated that neither
for the subjects with neurodevelopmental disorders and was reported as pathogenic in the original publication.52
predicted 283 (29.5%) of 959 variants as deleterious This problem has been increasingly recognized in recent
years,48
for control subjects. PolyPhen-2 predicted 3,157 (37.8%) suggesting that ‘‘known’’ pathogenic variants in
of 8,346 variants as probably damaging or possibly various databases should not be taken at face value and
>
damaging (PolyPhen-2_HDIV 0.453 as the cutoff) for instead deserve more detailed re-examination. Here, we
affected subjects and predicted 403 (42.0%) of 959 vari- analyzedtheentireClinVardatasetandcomparedtheiran-
ants as probably damaging or possibly damaging for notations with the automated interpretation (step 1) by
controlsubjects.Comparingaffectedandcontrolsubjects InterVartoassesstheconcordanceratesandexaminesour-
(Table 2), we did not observe a strong enrichment of ces of discordance. We recognized that because InterVar
P/LP variants with these two methods (p ¼ 0.64 for SIFT compiled some of its internal databases from ClinVar, its
andp¼0.08forPolyPhen-2_HDIV).Theseresultsdemon-
|     |     |     |     | interpretation | might be slightly | biased | toward being |
| --- | --- | --- | --- | -------------- | ----------------- | ------ | ------------ |
strate that in silico predictions alone might not be suffi- moresimilartothatofClinVar.
cient to identify P/LP variants in exome sequencing WeretrievedClinVarversion2016-03-02andselectedall
studies. non-conflicting nonsynonymous variants categorized as
|     |     |     | TheAmericanJournalofHumanGenetics100,267–280,February2,2017 |     |     |     | 273 |
| --- | --- | --- | ----------------------------------------------------------- | --- | --- | --- | --- |

Table2. AnalysisofDeNovoVariantsbySIFTandPolyPhen-2
SIFT PolyPhen-2
Interpretation AffectedSubjects ControlSubjects AffectedSubjects ControlSubjects
Benignortolerated 2,608(31.2%) 343(35.7%) 1,426(17.1%) 214(22.3%)
Deleterious,probablydamaging, 2,242(26.8%) 283(29.5%) 3,157(37.8%) 403(42.0%)
orpossiblydamaging
Unknown 3,496(42.0%) 333(34.8%) 3763(45.1%) 342(35.7%)
Total 8,346 959 8,346 959
pvalue(comparedtocontrolsubjects)a 0.64 0.08
apvalueswerecalculatedwithatwo-sidedFisher’sexacttest.
one of the following: (1) benign or likely benign and (2) turning incidental findings from a minimum set of 56
pathogenic or likely pathogenic. We then re-interpreted actionable genes,53 but many researchers have used an
thesevariantsbyusingtheautomatedinterpretationfunc- expanded list of genes selected according to domain
tion in InterVar (Table 3). For the benign category in knowledge. Several studies have examined incidental
ClinVar, InterVar also classified 4,898 (80.6%) variants as findings from large-scale genome or exome sequencing
benignorlikelybenign,suggestingthatInterVarislargely projects, so here we investigated how InterVar classifies
consistentwithClinVaronthiscategoryofvariants.How- clinicallyactionable genetic variants reported in previous
ever,forvariantsinthepathogeniccategory,InterVarand studies.
ClinVar have large differences. In fact, InterVar classified Amendola et al.54 previously examined exome se-
only2,058(13.9%)variantsinthecategoryaslikelypath- quencing data on 4,300 European Americans and 2,203
ogenic yet none as pathogenic. Obviously, we acknowl- AfricanAmericansaspartofNHLBIESP6500andreported
edge that all of these interpretations by InterVar were 616variants in112actionablegenes(Table4).These616
based ononly 18 pieces ofcriteriain step1, andnone of variants were classified as actionable and pathogenic on
them were subjected to manual examination; yet, addi- thebasisofHGMDannotations.Amendolaetal.re-classi-
tionalinformationsuchasfamilialsegregation,familyhis- fied these 616 variants by using their own classification
tory, and de novo status could move some variants with criteria, such as rules based on allele frequency, segrega-
uncertain significance into a more deleterious category tion, de novo status, function data, etc. They found only
(likelypathogenicorpathogenic). 70 (11.4%) as pathogenic or likely pathogenic, yet most
Given the differences between ClinVar annotation and ofthem(66.4%)wereclassifiedasvariantsofuncertainsig-
InterVarprediction,weperformedamoredetailedanalysis nificance. Automated prediction (step 1) from InterVar
on the 513 (3.5%) variants that were classified as patho- classified only 33 (5.4%) variants as pathogenic or likely
genicbyClinVarbutpredictedasbenignorlikelybenign pathogenic, whereas most of the variants (43.2%) were
by InterVar. First, we plotted the distribution of the classifiedasbenignorlikelybenign.Pleasenotethatdur-
maximum AAF of these variants in three databases (1000 ingvariantclassification,Amendolaetal.leveragedinfor-
Genomes Project, ExAC Browser, and NHLBI ESP6500; mation such as segregation and de novo status, but we
Figure 3). From this analysis, we found that there were didnothaveaccesstothesepiecesofinformation.There-
>10% variants with AAF > 0.01 and 5% variants with fore, the number of pathogenic variants classified by
AAF>0.1.Clearly,>10%variantsmightbemerelygenetic InterVar in step 2 (manual adjustment) could increase
polymorphisms that were incorrectly cataloged as patho- significantly given additional information. Nevertheless,
genic in ClinVar. Nevertheless, we also confirmed that in these results already suggest that the interpretation of
ClinVar,morethanhalfofthepathogenicorlikelypatho- InterVar is consistent with the manual interpretation by
genic variants were very rare with an AAF < 0.0001, and Amendolaetal.,whoconcludedthatthevastmajorityof
>85% pathogenic variants had an AAF < 0.001, which variants annotated as pathogenic in HGMD are probably
fitsourexpectations.Formanualexaminationofthesevar- notreallypathogenic.Thisanalysisconfirmsthatincorrect
iants,thecutoffofdiseaseprevalencecouldbeessentialfor classification of the pathogenic variant, even in ACMG
assigningbenigncriteriasuchasBS1. actionable genes, represents a substantial issue when
HGMDistheonlycriterionusedforvariantinterpretation.
AnalysisonPreviouslyReportedClinicallyActionable
Variants ComparativeAnalysiswithCLINVITAE
Clinical exome and genome sequencing are likely to CLINVITAE(seeWebResources)isadatabaseofclinically
uncover ‘‘incidental findings’’ that are unrelated to the observed genetic variants aggregated from public sources
indication for ordering the sequencing tests but are and is operated and made freely available by INVITAE.
ofclinicalsignificance.53TheACMGhasrecommendedre- Although the vast majority of the variants were collected
274 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

Table3. IllustrationofAutomatedInterpretationofPathogenic
andBenignVariantsAnnotatedinClinVar
ClinVar
| InterVar(Automated    |     | Pathogenicor     |     |     | Benignor     |     |     |     |     |     |     |     |
| --------------------- | --- | ---------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
| Interpretation)       |     | LikelyPathogenic |     |     | LikelyBenign |     |     |     |     |     |     |     |
| Benign                |     | 65(0.4%)         |     |     | 1,505(24.8%) |     |     |     |     |     |     |     |
| Likelybenign          |     | 448(3.0%)        |     |     | 3,393(55.9%) |     |     |     |     |     |     |     |
| Uncertainsignificance |     | 12,207(82.6%)    |     |     | 1,173(19.3%) |     |     |     |     |     |     |     |
| Likelypathogenic      |     | 2,058(13.9%)     |     |     | 0(0%)        |     |     |     |     |     |     |     |
| Pathogenic            |     | 0(0%)            |     |     | 0(0%)        |     |     |     |     |     |     |     |
| Sumoffivetiers        |     | 14,778           |     |     | 6,071        |     |     |     |     |     |     |     |
| Benignandlikelybenign |     | 513(3.5%)        |     |     | 4,898(80.6%) |     |     |     |     |     |     |     |
| Pathogenicandlikely   |     | 2,058(13.9%)     |     |     | 0(0%)        |     |     |     |     |     |     |     |
pathogenic
|     |     |     |     |     |     |     | Figure3. | AAFDistributionofPathogenicorLikelyPathogenic |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------------------------------------------- | --- | --- | --- | --- |
from public databases, 11,696 variants were detected and ClinVar Variants Predicted to Be Benign or Likely Benign by
InterVarandAllPathogenicorLikelyPathogenicClinVarVariants
| classified | by the | INVITAE | team. | Unlike | ClinVar | and |     |     |     |     |     |     |
| ---------- | ------ | ------- | ----- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
HGMD,whichcompileinformationfromdiversesources,
|                      |             |             |        |                 |              |           | <5 min        | (~0.1 ms   | per variant) |              | if an        | existing ANNOVAR  |
| -------------------- | ----------- | ----------- | ------ | --------------- | ------------ | --------- | ------------- | ---------- | ------------ | ------------ | ------------ | ----------------- |
| CLINVITAE            | potentially | represents  |        | a more          | homogeneous  |           |               |            |              |              |              |                   |
|                      |             |             |        |                 |              |           | annotation    | file is    | already      | available.   |              | For the wInterVar |
| collection           | of variants | interpreted |        | by              | a consistent | set of    |               |            |              |              |              |                   |
|                      |             |             |        |                 |              |           | server, all   | annotation | results      | for          | all possible | non-synony-       |
| institution-specific |             | rules.      | Among  | these           | 11,696       | variants, |               |            |              |              |              |                   |
|                      |             |             |        |                 |              |           | mous variants | were       | already      | pre-computed |              | and imported      |
| 5,405 (46.2%)        |             | and 717     | (6.1%) | were classified |              | as benign |               |            |              |              |              |                   |
intoMongoDB,aNoSQLdatabasesystem.Therefore,users
| or likely | benign | and pathogenic |     | or  | likely | pathogenic, |     |     |     |     |     |     |
| --------- | ------ | -------------- | --- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
canquicklysearchspecificvariantsandreceiveanalmost
respectively.Amongthem,4,226(36.1%)benignorlikely
immediateresponse(<1sforavariant).Inaddition,users
| benign | variants     | were also | classified | as  | benign | or likely  |              |        |     |              |     |                  |
| ------ | ------------ | --------- | ---------- | --- | ------ | ---------- | ------------ | ------ | --- | ------------ | --- | ---------------- |
|        |              |           |            |     |        |            | can manually | adjust |     | the criteria |     | and re-submit to |
| benign | by InterVar, | whereas   | only       | 227 | (1.9%) | pathogenic |              |        |     |              |     |                  |
orlikelypathogenicvariantswereclassifiedaspathogenic wInterVartoobtainthefinalinterpretationwithanalmost
immediateresponse.
| or likely                                            | pathogenic | by         | InterVar        | (Table    | 5). This | analysis |            |     |     |     |     |     |
| ---------------------------------------------------- | ---------- | ---------- | --------------- | --------- | -------- | -------- | ---------- | --- | --- | --- | --- | --- |
| again demonstrates                                   |            | that       | the concordance |           | between  | auto-    |            |     |     |     |     |     |
| matedinterpretationofInterVarandexpert-compiledclas- |            |            |                 |           |          |          | Discussion |     |     |     |     |     |
| sification                                           | is higher  | for benign |                 | or likely | benign   | variants |            |     |     |     |     |     |
thanforpathogenicorlikelypathogenicvariants. Inthisarticle,wehavepresentedtwocomputationaltools,
|     |     |     |     |     |     |     | InterVar | and wInterVar, |     | for performing |     | evidence-based |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | --- | -------------- | --- | -------------- |
wIntervar:WebVersionofInterVartoFacilitateManual clinical interpretation of genetic variants according to
Interpretation the2015ACMG-AMPguidelines.Tothebestofourknowl-
wInterVar(seeWebResources)isawebimplementationof edge, we are not aware of software tools that are freely
InterVar so that users can use an online web server to availabletotheacademiccommunityandperformsimilar
perform interpretation on individual variants without functionalities. We wish to emphasize that although
using command-line tools. The wInterVar server has two InterVarisacomputationaltool,itrequireshumaninput
steps for assessing and adjusting the clinical significance toderiveaccurateresultswithatwo-stepdesign:inthefirst
of variants: users first input a variant to obtain pre- step,InterVarperformsautomatedinterpretationwithpre-
computed,automatedinterpretation(Figure4A).Afterre- liminaryresults,yetinthesecondstep,InterVartakesaddi-
viewing the results of automated interpretation, users tional information provided by human experts to adjust
canthenclickthe‘‘adjust’’buttontoperformthemanual the criteria and provide a final interpretation. The two-
adjustment step by selecting and de-selecting appro- step procedure allows InterVar to leverage automated in-
priate criteria according to additional information and formation retrieval as much as possible, yet also allows
domain knowledge. The wInterVar server will then additionalinputbyhumanexperts,toobtainthemostac-
performthefinalinterpretationwiththetwo-stepproced- curateinterpretationsforgeneticvariants.
ure(Figure4B). We applied InterVar to annotate and interpret de novo
WeassessedthespeedofInterVarandwInterVar.Usinga variants in subjects with neurodevelopmental disease
machinewith16GBofmemoryandtwoIntelXeonX5650 and control subjects and observed a strong enrichment
(2.67 GHz) CPUs, the InterVar pipeline takes approxi- of pathogenic or likely pathogenic variants in affected
mately 40 min to annotate 3,000,000 variants from a subjects. In comparison, simple deleteriousness predic-
whole genome. The runtime can be greatly reduced to tion algorithms such as SIFT and PolyPhen-2 failed to
TheAmericanJournalofHumanGenetics100,267–280,February2,2017 275

Table4. Interpretationof616HGMD-ClassifiedPathogenic Table5. ComparisonofVariantInterpretationbyCLINVITAEand
| VariantsfromNHLBIESP6500 |            |             |     | AutomatedInterpretationbyInterVar |            |     |     |
| ------------------------ | ---------- | ----------- | --- | --------------------------------- | ---------- | --- | --- |
|                          | InterVar   | ESP6500Team |     |                                   | InterVar   |     |     |
| Clinical                 | (Automated | (Manual     |     | Clinical                          | (Automated |     |     |
Significance Interpretation) Interpretation) Concordant Significance Interpretation) CLINVITAE Concordant
| Benign           | 5   | 0   | 0   | Benign           | 242   | 2,407 | 230   |
| ---------------- | --- | --- | --- | ---------------- | ----- | ----- | ----- |
| Likelybenign     | 261 | 137 | 77  | Likelybenign     | 6,593 | 2,998 | 2,428 |
| Likelypathogenic | 30  | 38  | 2   | Likelypathogenic | 286   | 106   | 11    |
| Pathogenic       | 3   | 32  | 0   | Pathogenic       | 137   | 611   | 132   |
| Uncertain        | 317 | 409 | 234 | Uncertain        | 4,438 | 5,574 | 3,047 |
| significance     |     |     |     | significance     |       |       |       |
Sumoffivetiers 616 616 313 Sumoffivetiers 11,696 11,696 5,848
| Benignorlikely   | 266 | 137 | 79  | Benignorlikely   | 6,835 | 5,405 | 4,226 |
| ---------------- | --- | --- | --- | ---------------- | ----- | ----- | ----- |
| benign           |     |     |     | benign           |       |       |       |
| Pathogenicor     | 33  | 70  | 6   | Pathogenicor     | 423   | 717   | 227   |
| likelypathogenic |     |     |     | likelypathogenic |       |       |       |
differentiate affected from control subjects. This observa- mon and complex traits. Therefore, we caution that the
tionsuggeststhatoneshouldcompilemultiplesourcesof current interpretation is appropriate only for Mendelian
criteria (in this case, up to 28 criteria), including deleteri- diseases or Mendelian forms of complex diseases. Third,
ousness prediction algorithms, to assess the potential although we provide a set of default databases to help
pathogenicityofgeneticvariantsratherthanrelyondele- implement 18 of the 2015 ACMG-AMP criteria, it is ex-
teriousnesspredictionalgorithmsonly. pected that different users or groups might want to use
Currently, a number of public databases, such ClinVar theirownversionsofthesecriteria.Therefore,wedesigned
andHGMD,documenttheclinicalsignificanceofgenetic InterVartobehighlyflexibleintakinguser-suppliedanno-
variants, which are mostly provided by submitters or tationsforeachofthecriteriatoaccommodateavarietyof
manually compiled from scientific literature. Because userswithdifferentneeds.
different submitters or different authors can have very Another issue we wish to emphasize is that the 2015
differentcriteriatoassessthepathogenicityofgeneticvar- ACMG-AMPguidelinesuse28criteriawithequalweights.
iants, the quality of entries in these databases can be One underlying rationale might be that it is difficult to
highlyheterogeneous.Asaresult,itisexpectedthatapro- quantify the contribution of each criterion given the
portion of pathogenic variants in these databases might complexityofinterpretinggeneticevidence.25Anotherpo-
simplybefalsepositivesthataremisclassified.48–51Several tentialreasonisthatequalweightingisintuitivelyeasierto
studieshavedemonstratedthataftermanualre-interpreta- understandand implement by cliniciansand researchers.
tion,manyofthepathogenicvariantsareindeedbenignor However, it is expected that different types of criteria
haveuncertainsignificance.55–57Ourresultsinthecurrent
|     |     |     |     | might have | different contributions | and | weights for the |
| --- | --- | --- | --- | ---------- | ----------------------- | --- | --------------- |
studyfurthersupporttheobservationthataverylargepro- classification of the pathogenicity or quantitative predic-
portion of documented pathogenic or likely pathogenic tionofpathogenicity.Ifwecanaccumulateverylargedata-
variants are indeed polymorphisms segregating in the sets of true positives and true negatives, it is possible to
population and areunlikely to contribute significantly to apply machine-learning approaches in the future for
diseaserisk.Theseobservationsfurthersupporttheimpor- more accurate prediction and quantitative assessment of
tanceofefforts,suchasClinGen,tocompilehigh-quality, pathogenicityforgeneticvariants.
gold-standard datasets with confidence scores to be used One important caveat that we wish to stress is that
by the community for more accurate interpretation of InterVarisbettersuitedtoaddressingthevariant-interpreta-
geneticvariants. tionproblemforseverecongenitalorveryearly-onsetdevel-
InterVar has several limitations that we wish to discuss opmental disorders with nearly 100% penetrance, but it
here.First,InterVarneedsavariantknowledgebaseforac- mightworklesswellforlate-onsetorrecessivediseases.For
curate interpretation, so some variants in some genes example,amyotrophiclateralsclerosis(ALS)isafatal,pro-
might be more accurately interpreted than others. For gressiveneurodegenerativedisease,andthenon-canonical
example, well-studied genes tend to havemore entries in IkB kinase family member TANK binding kinase 1 (TBK1
clinical databases and are more likely to be interpreted [MIM: 604834]) was recently identified as an ALS-related
accurately.Second,InterVarisdesignedtointerpretgenetic geneinwhole-exomesequencingof2,874ALSindividuals
variants thatarelikely tocauseMendeliandiseases orare and 6,405 control individuals.58 InterVar classified all
|                  |               |          | >          | TBK1variantsreportedinthestudyasbenignorhavingun- |     |     |     |
| ---------------- | ------------- | -------- | ---------- | ------------------------------------------------- | --- | --- | --- |
| highly penetrant | for Mendelian | diseases | (OR 5) and |                                                   |     |     |     |
cannot handle alleles that increase susceptibility to com- certain significance. Another example is TREM2 (MIM:
276 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

A
B
| Figure4. IllustrationofwInterVar |     |     |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
(A)Automaticinterpretationofgeneticvariants,whichcanbeenteredbyseveralmeans.
(B)Onceusersclick‘‘adjust,’’thefulllistofcriteriaisshownformanualadjustment,afterwhichthefinalresultsaregiven.
605086),associatedwithAlzheimerdisease,froma recent ical interpretation of genetic variants according to the
sequencingstudyonaheterogeneouspopulationof1,092 2015 ACMG-AMP guidelines. InterVar can automatically
affected and 1,107 control subjects.59 Rare variants in generate the preliminary interpretations for 18 criteria
TREM2(especiallySNPrs75932628,whichhasthestrongest
|     |     |     |     | and then allow | manual | adjustment | of additional | criteria |
| --- | --- | --- | --- | -------------- | ------ | ---------- | ------------- | -------- |
association)werereportedintheirstudy.However,noneof toarriveatthefinalinterpretation.InterVarcanbeeasily
thesevariantswerepredictedtobepathogenicbyInterVar. usedbyresearchersandcliniciansandwillgreatlyfacilitate
OnemainreasonisthatdatabasessuchastheExACBrowser our understanding of the functional consequences of ge-
andESP6500wereusedincompilingthecriteria,butthey neticvariantsinhumandiseases.
| are technically | not appropriate | control databases | because |     |     |     |     |     |
| --------------- | --------------- | ----------------- | ------- | --- | --- | --- | --- | --- |
theyareactuallycomposedofmanyadultindividualswith
Acknowledgments
diseases.Incomparison,the1000GenomeProjectisprob-
TheauthorsthankDr.FanXia(BaylorCollegeofMedicine)and
ablyamoreappropriatesourceofgeneralcontrolsubjects,
butitssamplesizeistoosmalltoenableadequateevaluation Dr. Rong Mao (ARUP Laboratories) for reading the manuscripts
|                   |        |                      |             | and offering | valuable suggestions | on  | the web server. | We thank |
| ----------------- | ------ | -------------------- | ----------- | ------------ | -------------------- | --- | --------------- | -------- |
| of rare variants. | In any | case, when databases | such as the |              |                      |     |                 |          |
threeanonymousreviewersfortheirvaluablecomments,which
| ExAC Browser | andESP6500             | areused,itcouldbetrickyto |            |                |                |                |             |              |
| ------------ | ---------------------- | ------------------------- | ---------- | -------------- | -------------- | -------------- | ----------- | ------------ |
|              |                        |                           |            | helped improve | the manuscript | substantially. | We          | also want to |
| assign BS1   | and BS2 to adult-onset | or late-onset             | disorders, |                |                |                |             |              |
|              |                        |                           |            | thank members  | of the K.W.    | lab for        | testing the | InterVar and |
andsomeuser-specificadjustmentsmightbenecessaryfor
wInterVartoolsandprovidingfeedback.Thisstudywassupported
thesediseases.
byNIHgrantsHG006465andMH108728.K.W.waspreviouslya
In summary, we have developed InterVar, a com- boardmemberandstockholderofTuteGenomics,abioinformat-
putational tool, and wInterVar, a web server, for the clin- icssoftwarecompany.
|     |     |     | TheAmericanJournalofHumanGenetics100,267–280,February2,2017 |     |     |     |     | 277 |
| --- | --- | --- | ----------------------------------------------------------- | --- | --- | --- | --- | --- |

Received:April27,2016 Drosophilamelanogasterstrainw1118;iso-2;iso-3.Fly(Aus-
| Accepted:December30,2016 |     |     |     |     |     |     | tin)6,80–92. |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Published:January26,2017 9. McLaren,W.,Pritchard,B.,Rios,D.,Chen,Y.,Flicek,P.,and
|     |     |     |     |     |     |     | Cunningham, | F.  | (2010). Deriving |     | the consequences |     | of  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---------------- | --- | ---------------- | --- | --- |
genomicvariantswiththeEnsemblAPIandSNPEffectPredic-
| WebResources |     |     |     |     |     |     | tor.Bioinformatics26,2069–2070. |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- |
10. Kumar,P.,Henikoff,S.,andNg,P.C.(2009).Predictingtheef-
1000GenomesProject,http://www.1000genomes.org/
fectsofcodingnon-synonymousvariantsonproteinfunction
ANNOVAR,http://annovar.openbioinformatics.org/ usingtheSIFTalgorithm.Nat.Protoc.4,1073–1081.
ClinVar,https://www.ncbi.nlm.nih.gov/clinvar/
11. Adzhubei,I.A.,Schmidt,S.,Peshkin,L.,Ramensky,V.E.,Gera-
CLINVITAE,http://clinvitae.invitae.com/
|     |     |     |     |     |     |     | simova, | A., Bork, | P., Kondrashov, | A.S., | and | Sunyaev, | S.R. |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --------------- | ----- | --- | -------- | ---- |
dbNSFP,https://sites.google.com/site/jpopgen/dbNSFP
|     |     |     |     |     |     |     | (2010). | A method | and server | for | predicting | damaging |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ---------- | --- | ---------- | -------- | --- |
dbscSNV,https://sites.google.com/site/jpopgen/dbNSFP
missensemutations.Nat.Methods7,248–249.
dbSNP,http://www.ncbi.nlm.nih.gov/SNP
12. Kircher,M.,Witten,D.M.,Jain,P.,O’Roak,B.J.,Cooper,G.M.,
Ensembl,http://www.ensembl.org/
andShendure,J.(2014).Ageneralframeworkforestimating
| Exome Aggregation | Consortium |     | (ExAC) | Browser, | http://exac. |     |              |               |     |       |         |           |      |
| ----------------- | ---------- | --- | ------ | -------- | ------------ | --- | ------------ | ------------- | --- | ----- | ------- | --------- | ---- |
|                   |            |     |        |          |              |     | the relative | pathogenicity | of  | human | genetic | variants. | Nat. |
broadinstitute.org
Genet.46,310–315.
GERPþþ,http://mendel.stanford.edu/SidowLab/downloads/gerp/
13. Shihab,H.A.,Gough,J.,Cooper,D.N.,Day,I.N.,andGaunt,
GWASdb,http://jjwanglab.org/gwasdb
|                          |     |     |     |     |     |     | T.R. (2013).   | Predicting | the functional      |     | consequences   |     | of can- |
| ------------------------ | --- | --- | --- | --- | --- | --- | -------------- | ---------- | ------------------- | --- | -------------- | --- | ------- |
| HGMD,http://www.hgmd.org |     |     |     |     |     |     |                |            |                     |     |                |     | 29,     |
|                          |     |     |     |     |     |     | cer-associated | amino      | acid substitutions. |     | Bioinformatics |     |         |
InterVar,https://github.com/WGLab/InterVar
1504–1510.
MedGen,https://www.ncbi.nlm.nih.gov/medgen/
14. Schwarz,J.M.,Ro¨delsperger,C.,Schuelke,M.,andSeelow,D.
| NHLBI Exome | Sequencing | Project | (ESP) | Exome | Variant | Server, |     |     |     |     |     |     |     |
| ----------- | ---------- | ------- | ----- | ----- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
(2010).MutationTasterevaluatesdisease-causingpotentialof
http://evs.gs.washington.edu/EVS/
sequencealterations.Nat.Methods7,575–576.
OMIM,http://omim.org/
15. Gonza´lez-Pe´rez,A.,andLo´pez-Bigas,N.(2011).Improvingthe
OrphaNet,http://www.orpha.net/
assessmentoftheoutcomeofnonsynonymousSNVswitha
PolyPhen-2,http://genetics.bwh.harvard.edu/pph2
consensusdeleteriousnessscore,Condel.Am.J.Hum.Genet.
RefSeq,http://www.ncbi.nlm.nih.gov/refseq
88,440–449.
RepeatMasker,http://www.repeatmasker.org/
16. Dong,C.,Wei,P.,Jian,X.,Gibbs,R.,Boerwinkle,E.,Wang,K.,
SIFT,http://sift.jcvi.org/
|     |     |     |     |     |     |     | and Liu, | X. (2015). | Comparisonand |     | integration | of  | deleteri- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | ------------- | --- | ----------- | --- | --------- |
UCSCGenomeBrowser,http://genome.ucsc.edu
|     |     |     |     |     |     |     | ousness | prediction | methods | for nonsynonymous |     | SNVs | in  |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------- | ------- | ----------------- | --- | ---- | --- |
wIntervar,http://wintervar.wglab.org/
|     |     |     |     |     |     |     | whole exome | sequencing |     | studies. | Hum. Mol. | Genet. | 24, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | -------- | --------- | ------ | --- |
2125–2137.
17. Thusberg,J.,Olatubosun,A.,andVihinen,M.(2011).Perfor-
References
|     |     |     |     |     |     |     | mance of | mutation | pathogenicity |     | prediction | methods | on  |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | ------------- | --- | ---------- | ------- | --- |
missensevariants.Hum.Mutat.32,358–368.
1. McPherson,J.D.(2009).Next-generationgap.Nat.Methods6
(11,Suppl),S2–S5. 18. Thompson,B.A.,Greenblatt,M.S.,Vallee,M.P.,Herkert,J.C.,
|     |     |     |     |     |     |     | Tessereau, | C., Young, | E.L., | Adzhubey, | I.A., Li, | B., | Bell, R., |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ----- | --------- | --------- | --- | --------- |
2. Lyon,G.J.,andWang,K.(2012).Identifyingdiseasemutations
Feng,B.,etal.(2013).Calibrationofmultipleinsilicotools
ingenomicmedicinesettings:currentchallengesandhowto
accelerateprogress.GenomeMed.4,58. for predicting pathogenicity of mismatch repair gene
missensesubstitutions.Hum.Mutat.34,255–265.
3. Quinta´ns,B.,Ordo´n˜ez-Ugalde,A.,Cacheiro,P.,Carracedo,A.,
and Sobrido, M.J. (2014). Medical genomics: The intricate 19. Stenson,P.D.,Mort,M.,Ball,E.V.,Shaw,K.,Phillips,A.,and
|     |     |     |     |     |     |     | Cooper, D.N. | (2014). | The Human | Gene | Mutation | Database: |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | --------- | ---- | -------- | --------- | --- |
pathfromgeneticvariantidentificationtoclinicalinterpreta-
tion.Appl.Transl.Genomics3,60–67. building a comprehensive mutation repository for clinical
4. Chang,X.,andWang,K.(2012).wANNOVAR:annotatingge- and molecular genetics, diagnostic testing and personalized
genomicmedicine.Hum.Genet.133,1–9.
| netic variants | for personal |     | genomes | via the | web. | J. Med. |     |     |     |     |     |     |     |
| -------------- | ------------ | --- | ------- | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
Genet.49,433–436. 20. Landrum, M.J., Lee, J.M., Benson, M., Brown, G., Chao, C.,
5. Wang, K., Li, M., and Hakonarson, H. (2010). ANNOVAR: Chitipiralla, S., Gu, B., Hart, J., Hoffman, D., Hoover, J.,
etal.(2016).ClinVar:publicarchiveofinterpretationsofclin-
| functional                                                 | annotation | of  | genetic | variants | from | high- |                 |           |         |       |      |       |       |
| ---------------------------------------------------------- | ---------- | --- | ------- | -------- | ---- | ----- | --------------- | --------- | ------- | ----- | ---- | ----- | ----- |
| throughputsequencingdata.NucleicAcidsRes.38,e164.          |            |     |         |          |      |       |                 |           |         |       | 44   |       |       |
|                                                            |            |     |         |          |      |       | ically relevant | variants. | Nucleic | Acids | Res. | (D1), | D862– |
| 6. Yandell,M.,Huff,C.,Hu,H.,Singleton,M.,Moore,B.,Xing,J., |            |     |         |          |      |       | D868.           |           |         |       |      |       |       |
Jorde, L.B., and Reese, M.G. (2011). A probabilistic disease- 21. Horaitis,O.,Talbot,C.C.,Jr.,Phommarinh,M.,Phillips,K.M.,
gene finder for personal genomes. Genome Res. 21, 1529– and Cotton, R.G. (2007). A database of locus-specific data-
bases.Nat.Genet.39,425.
1542.
22. Rehm,H.L.,Berg,J.S.,Brooks,L.D.,Bustamante,C.D.,Evans,
7. Ng,S.B.,Turner,E.H.,Robertson,P.D.,Flygare,S.D.,Bigham,
A.W.,Lee,C.,Shaffer,T.,Wong,M.,Bhattacharjee,A.,Eichler, J.P., Landrum, M.J., Ledbetter, D.H., Maglott, D.R., Martin,
E.E., et al. (2009). Targeted capture and massively parallel C.L., Nussbaum, R.L., et al.; ClinGen (2015). ClinGen–the
sequencingof12humanexomes.Nature461,272–276. Clinical Genome Resource. N. Engl. J. Med. 372, 2235–
2242.
| 8. Cingolani, | P., Platts, | A., Wang, | L., | Coon, | M., Nguyen, | T., |     |     |     |     |     |     |     |
| ------------- | ----------- | --------- | --- | ----- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
23. Kazazian,H.H.,Boehm,C.D.,andSeltzer,W.K.(2000).ACMG
Wang,L.,Land,S.J.,Lu,X.,andRuden,D.M.(2012).Apro-
gramforannotatingandpredictingtheeffectsofsinglenucle- recommendationsforstandardsforinterpretationofsequence
variations.Genet.Med.2,302–303.
| otide | polymorphisms, | SnpEff: | SNPs | in  | the genome | of  |     |     |     |     |     |     |     |
| ----- | -------------- | ------- | ---- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
278 TheAmericanJournalofHumanGenetics100,267–280,February2,2017

24. Richards,C.S.,Bale,S.,Bellissimo,D.B.,Das,S.,Grody,W.W., tionalandchromatingenesdisruptedinautism.Nature515,
Hegde,M.R.,Lyon,E.,Ward,B.E.;andMolecularSubcommit- 209–215.
tee of the ACMG Laboratory Quality Assurance Committee 37. Iossifov,I.,O’Roak,B.J.,Sanders,S.J.,Ronemus,M.,Krumm,
(2008).ACMGrecommendationsforstandardsforinterpreta- N.,Levy,D.,Stessman,H.A.,Witherspoon,K.T.,Vives,L.,Pat-
tion and reporting of sequence variations: Revisions 2007. terson,K.E.,etal.(2014).Thecontributionofdenovocoding
Genet.Med.10,294–300. mutationstoautismspectrumdisorder.Nature515,216–221.
25. Richards,S.,Aziz,N.,Bale,S.,Bick,D.,Das,S.,Gastier-Foster, 38. Deciphering Developmental Disorders, S.; and Deciphering
J.,Grody,W.W.,Hegde,M.,Lyon,E.,Spector,E.,etal.;ACMG DevelopmentalDisordersStudy(2015).Large-scalediscovery
Laboratory Quality Assurance Committee (2015). Standards of novel genetic causes of developmental disorders. Nature
and guidelines for the interpretation of sequence variants: 519,223–228.
ajointconsensusrecommendationoftheAmericanCollege 39. Girard, S.L., Gauthier, J., Noreau, A., Xiong, L., Zhou, S.,
of Medical Genetics and Genomics and the Association for Jouan,L.,Dionne-Laporte,A.,Spiegelman,D.,Henrion,E.,Di-
MolecularPathology.Genet.Med.17,405–424. allo,O.,etal.(2011).Increasedexonicdenovomutationrate
26. Amendola, L.M., Jarvik, G.P., Leo, M.C., McLaughlin, H.M., inindividualswithschizophrenia.Nat.Genet.43,860–863.
Akkari,Y.,Amaral,M.D.,Berg,J.S.,Biswas,S.,Bowling,K.M., 40. Xu,B.,Ionita-Laza,I.,Roos,J.L.,Boone,B.,Woodrick,S.,Sun,
Conlin, L.K., et al. (2016). Performance of ACMG-AMP Y.,Levy,S.,Gogos,J.A.,andKarayiorgou,M.(2012).Denovo
Variant-Interpretation Guidelines among Nine Laboratories gene mutations highlight patterns of genetic and neural
intheClinicalSequencingExploratoryResearchConsortium. complexityinschizophrenia.Nat.Genet.44,1365–1369.
Am.J.Hum.Genet.98,1067–1076. 41. Gulsuner, S., Walsh, T., Watts, A.C., Lee, M.K., Thornton,
27. Auton, A., Brooks, L.D., Durbin, R.M., Garrison, E.P., Kang, A.M., Casadei, S., Rippey, C., Shahin, H., Nimgaonkar, V.L.,
H.M., Korbel, J.O., Marchini, J.L., McCarthy, S., McVean, Go,R.C.,etal.;ConsortiumontheGeneticsofSchizophrenia
G.A.,Abecasis,G.R.;and1000GenomesProjectConsortium (COGS); and PAARTNERS Study Group (2013). Spatial and
(2015).Aglobalreferenceforhumangeneticvariation.Nature temporal mapping of de novo mutations in schizophrenia
526,68–74. toafetalprefrontalcorticalnetwork.Cell154,518–529.
28. Lek,M.,Karczewski,K.J.,Minikel,E.V.,Samocha,K.E.,Banks, 42. Fromer,M.,Pocklington,A.J.,Kavanagh,D.H.,Williams,H.J.,
E., Fennell, T., O’Donnell-Luria, A.H., Ware, J.S., Hill, A.J., Dwyer,S.,Gormley,P.,Georgieva,L.,Rees,E.,Palta,P.,Ruder-
Cummings, B.B., et al.; Exome Aggregation Consortium fer,D.M.,etal.(2014).Denovomutationsinschizophrenia
(2016). Analysis of protein-coding genetic variation in implicatesynapticnetworks.Nature506,179–184.
60,706humans.Nature536,285–291. 43. Allen,A.S.,Berkovic,S.F.,Cossette,P.,Delanty,N.,Dlugos,D.,
29. Liu,X.,Wu,C.,Li,C.,andBoerwinkle,E.(2016).dbNSFPv3.0: Eichler,E.E.,Epstein,M.P.,Glauser,T.,Goldstein,D.B.,Han,
AOne-StopDatabaseofFunctionalPredictionsandAnnota- Y.,etal.;Epi4KConsortium;andEpilepsyPhenome/Genome
tions for Human Nonsynonymous and Splice-Site SNVs. Project(2013).Denovomutationsinepilepticencephalopa-
Hum.Mutat.37,235–241. thies.Nature501,217–221.
30. Liu,X.,Jian,X.,andBoerwinkle,E.(2011).dbNSFP:alight- 44. Hamdan,F.F.,Srour,M.,Capo-Chichi,J.M.,Daoud,H.,Nassif,
weight database of human nonsynonymous SNPs and their C.,Patry,L.,Massicotte,C.,Ambalavanan,A.,Spiegelman,D.,
functionalpredictions.Hum.Mutat.32,894–899. Diallo, O., et al. (2014). De novo mutations in moderate or
31. Hunter,S.,Jones,P.,Mitchell,A.,Apweiler,R.,Attwood,T.K., severeintellectualdisability.PLoSGenet.10,e1004772.
Bateman,A.,Bernard,T.,Binns,D.,Bork,P.,Burge,S.,etal. 45. Rauch, A., Wieczorek, D., Graf, E., Wieland, T., Endele, S.,
(2012). InterPro in 2011: new developments in the family Schwarzmayr,T.,Albrecht,B.,Bartholdi,D.,Beygo,J.,DiDo-
and domain prediction database. Nucleic Acids Res. 40, nato,N.,etal.(2012).Rangeofgeneticmutationsassociated
D306–D312. with severe non-syndromic sporadic intellectual disability:
32. Jian,X.,Boerwinkle,E.,andLiu,X.(2014).Insilicoprediction anexomesequencingstudy.Lancet380,1674–1682.
of splice-altering single nucleotide variants in the human 46. deLigt,J.,Willemsen,M.H.,vanBon,B.W.,Kleefstra,T.,Yn-
genome.NucleicAcidsRes.42,13534–13544. tema,H.G.,Kroes,T.,Vulto-vanSilfhout,A.T.,Koolen,D.A.,
33. Lewis,B.P.,Green,R.E.,andBrenner,S.E.(2003).Evidencefor de Vries, P., Gilissen, C., et al. (2012). Diagnostic exome
thewidespreadcouplingofalternativesplicingandnonsense- sequencing in persons with severe intellectual disability.
mediatedmRNAdecayinhumans.Proc.Natl.Acad.Sci.USA N.Engl.J.Med.367,1921–1929.
100,189–192. 47. Gilissen, C., Hehir-Kwa, J.Y., Thung, D.T., van de Vorst, M.,
34. Li,M.J.,Liu,Z.,Wang,P.,Wong,M.P.,Nelson,M.R.,Kocher, van Bon, B.W., Willemsen, M.H., Kwint, M., Janssen, I.M.,
J.P.,Yeager,M.,Sham,P.C.,Chanock,S.J.,Xia,Z.,andWang, Hoischen,A.,Schenck,A.,etal.(2014).Genomesequencing
J.(2016).GWASdbv2:anupdatedatabaseforhumangenetic identifiesmajorcausesofsevereintellectualdisability.Nature
variants identified by genome-wide association studies. 511,344–347.
NucleicAcidsRes.44(D1),D869–D876. 48. (2016). Improving databases for human variation. Nat.
35. Malcolmson,J.,Kleyner,R.,Tegay,D.,Adams,W.,Ward,K., Methods13,103.
Coppinger, J., Nelson, L., Meisler, M.H., Wang, K., Robison, 49. MacArthur,D.G.,Manolio,T.A.,Dimmock,D.P.,Rehm,H.L.,
R.,andLyon,G.J.(2016).SCN8Amutationinachildpresent- Shendure,J.,Abecasis,G.R.,Adams,D.R.,Altman,R.B.,Anto-
ingwithseizuresanddevelopmentaldelays.ColdSpringHarb narakis,S.E.,Ashley,E.A.,etal.(2014).Guidelinesforinvesti-
MolCaseStud2,a001073. gating causality of sequence variants in human disease.
36. DeRubeis,S.,He,X.,Goldberg,A.P.,Poultney,C.S.,Samocha, Nature508,469–476.
K.,Cicek,A.E.,Kou,Y.,Liu,L.,Fromer,M.,Walker,S.,etal.; 50. Dorschner, M.O., Amendola, L.M., Turner, E.H., Robertson,
DDD Study; Homozygosity Mapping Collaborative for P.D.,Shirts,B.H.,Gallego,C.J.,Bennett,R.L.,Jones,K.L.,To-
Autism;andUK10KConsortium(2014).Synaptic,transcrip- kita,M.J.,Bennett,J.T.,etal.;NationalHeart,Lung,andBlood
TheAmericanJournalofHumanGenetics100,267–280,February2,2017 279

Institute Grand Opportunity Exome Sequencing Project Deleterious-anddisease-alleleprevalenceinhealthyindivid-
(2013). Actionable, pathogenic incidental findings in 1,000 uals: insights from current predictions, mutation databases,
participants’exomes.Am.J.Hum.Genet.93,631–640. and population-scale resequencing. Am. J. Hum. Genet. 91,
51. Bell, C.J., Dinwiddie, D.L., Miller, N.A., Hateley, S.L., Ganu- 1022–1032.
sova,E.E.,Mudge,J.,Langley,R.J.,Zhang,L.,Lee,C.C.,Schil- 56. Shearer, A.E., Eppsteiner, R.W., Booth, K.T., Ephraim, S.S.,
key, F.D., et al. (2011). Carrier testing for severe childhood Gurrola, J., 2nd, Simpson, A., Black-Ziegelbein, E.A., Joshi,
recessivediseasesbynext-generationsequencing.Sci.Transl. S.,Ravi,H.,Giuffre,A.C.,et al.(2014).Utilizingethnic-spe-
Med.3,65ra4. cificdifferencesinminorallelefrequencytorecategorizere-
52. Shi,L.,Guo,Y.,Dong,C.,Huddleston,J.,Yang,H.,Han,X., ported pathogenic deafness variants. Am. J. Hum. Genet.
Fu, A., Li, Q., Li, N., Gong, S., et al. (2016). Long-read 95,445–453.
sequencing and de novo assembly of a Chinese genome. 57. Tabor,H.K.,Auer,P.L.,Jamal,S.M.,Chong,J.X.,Yu,J.H.,Gor-
Nat.Commun.7,12065. don, A.S., Graubert, T.A., O’Donnell,C.J., Rich,S.S.,Nicker-
53. Green,R.C.,Berg,J.S.,Grody,W.W.,Kalia,S.S.,Korf,B.R.,Mar- son, D.A., Bamshad, M.J.; and NHLBI Exome Sequencing
tin,C.L.,McGuire,A.L.,Nussbaum,R.L.,O’Daniel,J.M.,Or- Project(2014).PathogenicvariantsforMendelianandcom-
mond, K.E., et al.; American College of Medical Genetics plextraitsinexomesof6,517EuropeanandAfricanAmeri-
andGenomics(2013).ACMGrecommendationsforreporting cans:implicationsforthereturnofincidentalresults.Am.J.
of incidental findings in clinical exome and genome Hum.Genet.95,183–193.
sequencing.Genet.Med.15,565–574. 58. Cirulli, E.T., Lasseigne, B.N., Petrovski, S., Sapp, P.C., Dion,
54. Amendola, L.M., Dorschner, M.O., Robertson, P.D., Salama, P.A.,Leblond,C.S.,Couthouis,J.,Lu,Y.F.,Wang,Q.,Krueger,
J.S.,Hart,R.,Shirts,B.H.,Murray,M.L.,Tokita,M.J.,Gallego, B.J., et al.; FALS Sequencing Consortium (2015). Exome
C.J., Kim, D.S., et al. (2015). Actionable exomic incidental sequencing in amyotrophic lateral sclerosis identifies risk
findingsin6503participants:challengesofvariantclassifica- genesandpathways.Science347,1436–1441.
tion.GenomeRes.25,305–315. 59. Guerreiro,R.,Wojtas,A.,Bras,J.,Carrasquillo,M.,Rogaeva,E.,
55. Xue,Y.,Chen,Y., Ayub,Q.,Huang,N.,Ball,E.V., Mort,M., Majounie,E.,Cruchaga,C.,Sassi,C.,Kauwe,J.S.K.,Younkin,
Phillips, A.D., Shaw, K., Stenson, P.D., Cooper, D.N., Tyler- S., et al.; Alzheimer Genetic Analysis Group (2013). TREM2
Smith, C.; and 1000 Genomes Project Consortium (2012). variantsinAlzheimer’sdisease.N.Engl.J.Med.368,117–127.
280 TheAmericanJournalofHumanGenetics100,267–280,February2,2017
