Received:11June2020 | Revised:18July2020 | Accepted:23July2020
DOI:10.1002/humu.24088
RAPID COMMUNICATION
Fitting a naturally scaled point system to the ACMG/AMP
variant classification guidelines
Sean V. Tavtigian1,2 | Steven M. Harrison3 | Kenneth M. Boucher2,4 |
Leslie G. Biesecker5
1DepartmentofOncologicalSciences,
UniversityofUtahSchoolofMedicine,Salt Abstract
LakeCity,Utah
Recently, we demonstrated that the qualitative American College of Medical
2HuntsmanCancerInstituteattheUniversity
ofUtah,SaltLakeCity,Utah GeneticsandGenomics/AssociationforMedicalPathology(ACMG/AMP)guidelines
3BroadInstituteofMITandHarvard, for evaluation of Mendelian disease gene variants are fundamentally compatible
Cambridge,Massachusetts
withaquantitativeBayesianformulation.Here,weshowthattheunderlyingACMG/
4DepartmentofInternalMedicine,Divisionof
Epidemiology,UniversityofUtahSchoolof
AMP“strengthofevidencecategories”canbeabstractedintoapointsystem.These
Medicine,SaltLakeCity,Utah points are proportional to Log(odds), are additive, and produce a system that re-
5MedicalGenomicsandMetabolicGenetics
capitulatestheBayesianformulationoftheACMG/AMPguidelines.Thestrengthsof
Branch,NationalHumanGenomeResearch
Institute,NationalInstitutesofHealth, thissystemareitssimplicityandthattheconnectionbetweenpointvaluesandodds
Bethesda,Maryland
of pathogenicity allows empirical calibration of the strength of evidence for in-
Correspondence dividualdatatypes.Weaknessesincludethatanarrowrangeofpriorprobabilitiesis
SeanV.Tavtigian,DepartmentofOncological
locked in and that the Bayesian nature of the system is inapparent. We conclude
Sciences,UniversityofUtahSchoolof
Medicine,2000CirofHopeDr, thatapoints‐basedsystemhasthepracticalattributeofuser‐friendlinessandcanbe
SaltLakeCity,UT84112.
usefulsolongas theunderlying Bayesianprinciplesareacknowledged.
Email:sean.tavtigian@hci.utah.edu
Fundinginformation KEYWORDS
CanadianInstitutesofHealthResearch, ACMG,Bayesianframework,medicalgenetics,points‐basedclassificationsystem,scoring
Grant/AwardNumber:GP1‐155865;National
metric,unclassifiedvariants,variantclassification,variantsofuncertainsignificance
CancerInstitute,Grant/AwardNumber:P30
CA042014;NationalHumanGenome
ResearchInstitute,Grant/AwardNumber:
HG200359
1 | INTRODUCTION 2 | DERIVATION OF A POINTS SCALE
Recently,wedemonstratedthatthequalitativeAmericanCollege Within the ACMG/AMP variant classification guidelines, thresholds
of Medical Genetics and Genomics/Association for Medical forvariantclassificationaredefinedbyprobabilisticboundariesthat
Pathology (ACMG/AMP) guidelines for the evaluation of Mende- were set by community consensus (Plon et al., 2008; Richards
lian disease gene variants are fundamentally compatible with a etal.,2015).ThesearegiveninTable1.
quantitativeBayesianformulation(Richardsetal.,2015;Tavtigian Withthesecommunityagreementsinplace,thestrengthsofthe
etal.,2018).However,theactualuseofBayesianformulationcan variousACMG/AMPrulesforcombiningevidencecriteria(Richards
bechallengingforsomeusersbecauseoftherequiredcalculations. etal.,2015)canbeexpressedasoddsinfavorofpathogenicityviaa
Through the following brief analysis, we further demonstrate a singleexponentialequation(Tavtigianetal.,2018).Here,wecite“eq.
natural conversion from that Bayesian formulation into a points‐ 5” from that publication, using the same variable definitions from
basedsystem. thatanalysis:
|
1734 ©2020WileyPeriodicalsLLC wileyonlinelibrary.com/journal/humu HumanMutation.2020;41:1734–1737.

 10981004, 2020, 10, Downloaded from https://onlinelibrary.wiley.com/doi/10.1002/humu.24088 by NANYANG TECHNOLOGICAL UNIVERSITY, Wiley Online Library on [13/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
|
| TAVTIGIANETAL. |     |     |     |     |     |     |     |     |     |     |     |     |     | 1735 |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
TABLE 1 Variantclassificationcategoriesandtheirprobabilistic TABLE 2 PointvaluesforACMG/AMPstrengthofevidence
| boundaries |     |     |     |                      |     |     | categories |     |     |     |            |     |     |     |
| ---------- | --- | --- | --- | -------------------- | --- | --- | ---------- | --- | --- | --- | ---------- | --- | --- | --- |
|            |     |     |     | Posteriorprobability |     |     |            |     |     |     | Pointscale |     |     |     |
Evidence
| Category   |     |     |     | (PP)‐basedboundaries |     |     |          |     |     |     |            |     |        |     |
| ---------- | --- | --- | --- | -------------------- | --- | --- | -------- | --- | --- | --- | ---------- | --- | ------ | --- |
|            |     |     |     |                      |     |     | Strength |     |     |     | Pathogenic |     | Benign |     |
| Pathogenic |     |     |     | PP>0.99              |     |     |          |     |     |     |            |     |        |     |
0a
|                  |     |     |     |               |     |     | Indeterminate |     |     |     | 0   |     |     |     |
| ---------------- | --- | --- | --- | ------------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
| LikelyPathogenic |     |     |     | 0.99≥PP>0.90a |     |     |               |     |     |     |     |     |     |     |
−1
|     |     |     |     |     |     |     | Supporting |     |     |     | 1   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
0.10≤PP≤0.90
Uncertain
|              |     |     |     |                |     |     | Moderate   |     |     |     | 2   |     | −2b |     |
| ------------ | --- | --- | --- | -------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| LikelyBenign |     |     |     | 0.001≤PP<0.10a |     |     |            |     |     |     |     |     |     |     |
|              |     |     |     |                |     |     | Strong     |     |     |     | 4   |     | −4  |     |
| Benign       |     |     |     | PP<0.001       |     |     |            |     |     |     |     |     |     |     |
|              |     |     |     |                |     |     | Verystrong |     |     |     | 8   |     | −8b |     |
aNotethattheinequalitiesaresymmetricaroundthebroadUncertain
aNoteismadethatRichardsetal.didnotspecificallyrecognize
category.
indeterminateevidence.Nonetheless,ifonethinksoftheoddsinfavorof
pathogenicityasacontinuousvariable,thereexistsarangethatfalls
(NP NP NP NP NB NB ) b e t w e e n S u p p ortingBenignandSupportingPathogenic.Thisis
|     |      |     | Su+ M+ St+ | VSt−⎡ Su+ | St⎤   |     |      |                |      |     |     |     |     |     |
| --- | ---- | --- | ---------- | --------- | ----- | --- | ---- | -------------- | ---- | --- | --- | --- | --- | --- |
|     | OP=O | 8   | 4 2        | 1 ⎣ 8     | 2 ⎦ , | (1) | In d | e t e rm i n a | te . |     |     |     |     |     |
PVSt
bNoteisalsomadethatRichardsetal.didnotspecifybenignevidenceat
themoderateorverystronglevels.Nevertheless,thepointsystemwould
readilysupporttheadditionofsuchcriteria.
| where | OP is | the calculated | odds | of pathogenicity; | O   | is  |     |     |     |     |     |     |     |     |
| ----- | ----- | -------------- | ---- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
PVSt
theoddsofpathogenicityassignedtothe“verystrong”evidence
of pathogenicity category; N P and N B are the number of OP to obtain a posterior probability of pathogenicity (P 2 ). Two re-
invocations of a specific pathogenic or benign evidence levantexpressionsofBayes'ruleare:
| strength | level, | respectively, | by a | specific classification | rule; | and |     |     |     |     |     |     |     |     |
| -------- | ------ | ------------- | ---- | ----------------------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Su, M, St, and VSt are “supporting,” “moderate,” “strong,” and P 2=(OP×P 1)÷[(OP−1)×P 1+1], (4)
| “very | strong” | strength | of evidence | strength level | categories, |     |     |     |       |        |           |      |     |     |
| ----- | ------- | -------- | ----------- | -------------- | ----------- | --- | --- | --- | ----- | ------ | --------- | ---- | --- | --- |
|       |         |          |             |                |             |     |     |     | OP=[P | 2×(1−P | 1)]÷[(1−P | 2)×P | 1]. | (5) |
respectively.
| Does | Equation | (1) | imply a natural | point system | for | variant |     |     |     |     |     |     |     |     |
| ---- | -------- | --- | --------------- | ------------ | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
classification? TheACMG/AMPclassificationcriteriaspecifythatifnoneofthe
NotingthatbydefinitioninourpreviousworkO PVSt=O 8 ,we criteriaaremet,avariantisofuncertainsignificance(VUS).Thisspe-
P Su
canrewriteEquation(1)as: cification implies that the prior probability falls within the posterior
probabilityrangeforVUS,whichis0.10–0.90.ForBRCA1andBRCA2,
OP=O(1NPSu+2NPM+4NPSt+8NPVSt−[1NBSu+4NBSt]). (2) the empirically measured prior probability for the combination of
PSu
in‐frame
|     |     |     |     |     |     |     | missense | substitutions, |     |     | indels, and | proximal | splice | junction |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | --- | --- | ----------- | -------- | ------ | -------- |
TakingtheLog andthendividingbytheLog (O ),wehave: variants is approximately 0.10 (Abkevich et al., 2004; Easton et al.,
|     |            | 10   |                | 10           | PSu  |     |          |                |                |           |     |             |                 |     |
| --- | ---------- | ---- | -------------- | ------------ | ---- | --- | -------- | -------------- | -------------- | --------- | --- | ----------- | --------------- | --- |
|     |            |      |                |              |      |     | 2007;    | Goldgar        | et al., 2004). | Moreover, | as  | the number  | of biologically |     |
| Log | 10(OP)/Log | 10(O | PSu)=1N PSu+2N | PM+4N PSt+8N |      |     |          |                |                |           |     |             |                 |     |
|     |            |      |                |              | PVSt |     | relevant | susceptibility | genes          | included  | in  | gene panels | increases,      | the |
−[1N BSu+4N Bst]. (3) average number of variants revealed by an individual test increases,
|     |     |     |     |     |     |     | which | lowers | their average | prior | probability. | Yet, | it is important | to  |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------ | ------------- | ----- | ------------ | ---- | --------------- | --- |
Inspectingtheboldedintegers1,2,4,and8thatemergeonthe recognizethatifthegeneralizedpriorprobabilityfallsbelowthelikely
rightsideofEquation(3),itisevidentthattheACMG/AMPstrength benignthreshold,thenunclassifiedsequencevariantsareapriorilikely
ofevidencecategoriescanbeabstractedintoapointsystem,givenin benignunlesstheyarereportedwithevidenceinfavorofpathogenicity.
Table 2. We emphasize that these points are proportional to Log Therefore, we chose to accept the ACMG/AMP assumption, with
threshold‐definingcalculationsbasedonapriorprobabilityof0.10,as
(odds)ratherthanOP,andare,therefore,additive.Indeed,theodds
corresponding to an individual rule for combining evidence criteria before (Tavtigian et al., 2018). With a prior probability of 0.10 and
areeasilyretrieved,becauseOP=O(Points). posteriorprobabilityattheACMG/AMPLikelyPathogenicthresholdof
PSu
0.90,Equation(5)showsthattheOPthresholdforLikelyPathogenicis
|     |            |     |          |        |     |     | >81:1. | With | the posterior | probability | at  | the Pathogenic | threshold | of  |
| --- | ---------- | --- | -------- | ------ | --- | --- | ------ | ---- | ------------- | ----------- | --- | -------------- | --------- | --- |
| 3 | | DERIVATION |     | OF POINT | VALUES | FOR |     |        |      |               |             |     |                |           |     |
0.99,theOPthresholdbecomes>891:1.Similarly,theOPthresholdsfor
CLASSIFICATION THRESHOLDS LikelyBenignandBenignare<1.00:1and<0.00901:1,respectively.
FiveofthesixACMG/AMPLikelyPathogenicCombiningCriteria
WhileframingtheACMG/AMPevidencestrengthasOPexpressesa have strength equivalent to six pieces of supporting pathogenic
Bayesianpointofview,theactualapplicationofBayes'rulearrives evidence (Tavtigian et al., 2018; Table 1). This requirement for
whenaprior probabilityofpathogenicity(P 1 )iscombinedwiththe the equivalent of six of O PSu implies that the exact value of O PSu

 10981004, 2020, 10, Downloaded from https://onlinelibrary.wiley.com/doi/10.1002/humu.24088 by NANYANG TECHNOLOGICAL UNIVERSITY, Wiley Online Library on [13/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
1736 |
TAVTIGIANETAL.
TABLE 3 Point‐basedvariantclassificationcategories data.ThesystemfocusesonseparatingtheACMG/AMPcriteriainto
groupsofcriteriathatarelogicallyindependentofeachother.Then,
| Category   |     |     |     | Pointranges |        |        |            |           |          |     |          |          |      |
| ---------- | --- | --- | --- | ----------- | ------ | ------ | ---------- | --------- | -------- | --- | -------- | -------- | ---- |
|            |     |     |     |             | within | groups | of related | criteria, | building |     | data use | patterns | that |
| Pathogenic |     |     |     | ≥10         |        |        |            |           |          |     |          |          |      |
choosethemostappropriatedatatypeandevidencestrengthwhile
| LikelyPathogenic |     |     |     | 6to9a |          |                 |     |     |                 |     |       |        |        |
| ---------------- | --- | --- | --- | ----- | -------- | --------------- | --- | --- | --------------- | --- | ----- | ------ | ------ |
|                  |     |     |     |       | avoiding | double‐counting |     | on  | non‐independent |     | data. | On the | patho- |
Uncertain 0to5 genicside,thebasicSherlocpointscaleis1,2,3,4,and5.Onepoint
|     |     |     |     | −1to−6a | mostoftencorrespondstoanACMGsupportingpathogeniccriterion, |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
LikelyBenign
|     |     |     |     | ≤−7 | 5pointsalwayscorrespondstoaverystrongpathogeniccriterion,and |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Benign
|     |     |     |     |     | in‐between | there | is a | trend | of increasing | ACMG | evidence |     | strength |
| --- | --- | --- | --- | --- | ---------- | ----- | ---- | ----- | ------------- | ---- | -------- | --- | -------- |
aOperationally,thepriorprobabilityshouldbeunderstoodtobe
correspondingtoincreasedpoints.Thethresholdfordeclaringavariant
infinitesimally>0.10.Thishastwoeffects.First,itmakestheposterior
|     |     |     |     |     | Likely | Pathogenic | is 4 | points | and Pathogenic |     | is 5 points. | Though | the |
| --- | --- | --- | --- | --- | ------ | ---------- | ---- | ------ | -------------- | --- | ------------ | ------ | --- |
probabilityoftheAmericanCollegeofMedicalGenetics(ACMG)Likely
Pathogeniccombiningrulesinfinitesimallygreaterthan0.90,sothatthe Sherlocsystemfocusesontherationaluseoftheavailabledatatoward
LikelyPathogenicrulesworkproperly.Aspecificvalueof0.102would
variantclassification,neitherthederivationofthepointsystemnorthe
havetheaddedbenefitthatsevenpointswouldmeettheIARC
derivationoftheclassificationthresholdsaredescribed.
(InternationalAgencyforResearchonCancer)LikelyPathogenic
thresholdof0.95.Second,itenforcesarequirementforsomeevidenceof Amorerecenteffortinvolvesstandardsfortheinterpretationof
|     |     |     |     |     | copy | number | variants | (Riggs | et al., 2020). | In  | this point | system, | total |
| --- | --- | --- | --- | --- | ---- | ------ | -------- | ------ | -------------- | --- | ---------- | ------- | ----- |
benigneffectforsequencevariantstobeclassifiedasLikelyBenign.One
couldalsoarguethatthepointthresholdforLikelyBenignshouldreally scores of 0.90 and 0.99 are the thresholds for Likely Pathogenicand
be−2.ThiswouldmatchtheACMGrule“LikelyBenign(ii)”ratherthan
|     |     |     |     |     | Pathogenic, | respectively |     | because | “variants | interpreted |     | as pathogenic |     |
| --- | --- | --- | --- | --- | ----------- | ------------ | --- | ------- | --------- | ----------- | --- | ------------- | --- |
thesimplenumericalrequirementthattheposteriorprobabilitybe<0.10.
shouldhavea99%levelofconfidenceandvariantsinterpretedaslikely
pathogenicshouldhavea90%levelofconfidence.”Thatis,Riggsetal.
is 681 =2.0801:1; moreover, the expression OP=O(Points) can considered that their score thresholds resemble probabilities of pa-
PSu
be employed to calculate the number of points required to reach thogenicity. Withinthis point system, individual pieces of evidence in
the classification thresholds as simply Threshold=2.0801(Points). favorofpathogenicityreceivebetween0.10and1.00points,andallof
Roundinguptothenearestintegers,theACMG/AMPthresholdsfor thedataforasingle‐sequencevariantareaddedtogethertoarriveata
Pathogenic and Likely Pathogenic are 10 points and 6 points, scoreforthatvariant.FocusingonthepathogenicsideoftheRiggsetal.
respectively.Roundingdowntothenearestintegers,thethresholds system,wewouldpointoutthreeconsiderations.First,asRiggsetal.
for Likely Benign and Benign are −1 and −7 points, respectively. admit, there is no derived, fitted, trained, or otherwise‐calibrated
Theresultingpoint‐basedcategoricalrangesaregiveninTable3. connectionbetweenevidencetypesandthepointsaccordedtothem
|     |     |     |     |     | (Riggs | et al. | noted that | “these | numbers | have | not been | statistically |     |
| --- | --- | --- | --- | --- | ------ | ------ | ---------- | ------ | ------- | ---- | -------- | ------------- | --- |
derived”).
|     |     |     |     |     |     | This | makes | it difficultto | calibrate | a   | point scale. | Second, | as  |
| --- | --- | --- | --- | --- | --- | ---- | ----- | -------------- | --------- | --- | ------------ | ------- | --- |
4 | STRENGTHS, WEAKNESSES, AND summingacrossthedataforasingle‐sequencevariantcaneasilyresult
| RELEVANCE | TO RECENT |     | LITERATURE |     |     |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
intotalscoresthatexceed1.0,thethresholdsof0.90and0.99cannot
|     |     |     |     |     | be considered |     | as posterior |     | probabilities. | Third, | under | Bayes' | rule |
| --- | --- | --- | --- | --- | ------------- | --- | ------------ | --- | -------------- | ------ | ----- | ------ | ---- |
Theprincipalstrengthofsuchapointsystemisthatusingitrequires (Equation(4)),conditionaloddsof11.0:1arerequiredtomovefroma
posteriorprobabilityof0.90–0.99.Usingthepointsystemthatwede-
| only addition | and subtraction. | The | weakness | is that the Bayesian |     |     |     |     |     |     |     |     |     |
| ------------- | ---------------- | --- | -------- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
natureofthesystemishidden.Specificchoicesofpriorprobability, rived above, bridging that gap—moving from the threshold of Likely
PathogenictoPathogenic—requires4points,thatis,atleastfoursup-
oddsofpathogenicity,andposteriorprobabilityarelockedin,andthe
veryconceptsofprobabilitiesandoddsareremovedfromview.Itis porting,ortwomoderate,ortwosupportingplusonemoderate,orone
importanttoreiterate,however,thatthepointsdescribedhereare strongpieceofpathogenicevidence.Yet,inboththeSherlocandRiggs
intentionally proportional to Log(odds), and simply a shorthand re- etal.system,oneelementofsupportingpathogenicevidencewouldbe
presentationofEquations(1)–(3).Consequently,theoddsofpatho- sufficient. This means that in these two‐points‐based systems, the
genicity can be calculated from any evidence combination, then differencebetweenLikelyPathogenicandPathogenicisverysmall;inall
combinedwithapriorprobabilityusingBayes'rule(i.e.,Equation(4)). likelihood,eithertheLikelyPathogenicboundaryistoostrongorthe
As the strength of evidence increases in either the pathogenic or Pathogenicboundarytooweak.
benigndirections,theresultingposteriorprobabilitieswillasympto- Acommonargumentagainstclassificationbasedonpointscales
ticallyapproach1.00or0.00,respectively. isthatthescalesandclassificationthresholdstendtobearbitrary.Of
course,anarbitrarypoint‐basedclassificationsystem,ifthoughtfully
Weknowofmultipleeffortsthathavedevelopedoraredevel-
oping points‐based systems that are intended to contribute to se- designed, may be operationally satisfactory. Though the qualitative
quencevariantclassification.Oneeffort,“Sherloc”wasdevelopedby
ACMG/AMPvariantclassificationsystemitselfhascomponentsthat
Invitae,Inc.withtheintentiontoimproveupontheprecisionofthe maybeconsideredarbitrary,itwasthoughtfullyenoughdesignedso
ACMG/AMP guidelines (Nykamp et al., 2017). Sherloc captures a thataninternallyconsistentBayesianformulationcouldbefittedto
wide range of data, with scoring ranging from 5 Benign points to it.ThepointsystemderivedhereflowsnaturallyfromthatBayesian
5 Pathogenicpointsand explicitly accords 0points to some(weak) formulation. Indeed, upon examination of the Richards et al.

 10981004, 2020, 10, Downloaded from https://onlinelibrary.wiley.com/doi/10.1002/humu.24088 by NANYANG TECHNOLOGICAL UNIVERSITY, Wiley Online Library on [13/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
|
| TAVTIGIANETAL. |     |     |     |     |     |     |          |              |     |     |     |     |     | 1737 |
| -------------- | --- | --- | --- | --- | --- | --- | -------- | ------------ | --- | --- | --- | --- | --- | ---- |
|                |     |     |     |     |     |     | CONFLICT | OF INTERESTS |     |     |     |     |     |      |
S.V.T.holdsIlluminastockinapersonallymanagedaccount.L.G.B.
|     |     |     |     |     |     |     | being an uncompensated |          | member  | of      | Illumina  | Advisory  | Board | has    |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | -------- | ------- | ------- | --------- | --------- | ----- | ------ |
|     |     |     |     |     |     |     | received in‐kind       | research | support | from    | ArQule    | Inc.      | (now  | wholly |
|     |     |     |     |     |     |     | owned by Merck,        | Inc.)    | and     | Pfizer, | Inc., and | honoraria | from  | Cold   |
SpringHarborPress.
ORCID
|     |     |     |     |     |     |     | SeanV.Tavtigian |     | http://orcid.org/0000-0002-7543-8221 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------------------------ | --- | --- | --- | --- | --- |
REFERENCES
|     |     |     |     |     |     |     | Abkevich, V., | Zharkikh, | A., Deffenbaugh, |     | A.  | M., Frank, | D., | Chen, Y., |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --------- | ---------------- | --- | --- | ---------- | --- | --------- |
Shattuck,D.,…Tavtigian,S.V.(2004).Analysisofmissensevariation
inhumanBRCA1inthecontextofinterspecificsequencevariation.
FIGURE 1 JournalofMedicalGenetics,41(7),492–507.https://doi.org/10.1136/
SchematicrelationshipamongBayes'rule,the
jmg.2003.015867
qualitativeAmericanCollegeofMedicalGeneticsandGenomics/
Easton,D.F.,Deffenbaugh,A.M.,Pruss,D.,Frye,C.,Wenstrup,R.J.,Allen‐
AssociationforMedicalPathology(ACMG/AMP)variant
Brady,K.,…Goldgar,D.E.(2007).Asystematicgeneticassessmentof
classificationguidelines,theBayesianformulationofthose
guidelines,andthepointsystemderivedhere 1,433 sequence variants of unknown clinical significance in the
cancer‐predisposition
|           |              |           |        |          |     |                | BRCA1 and  | BRCA2 | breast    |                 |     |                          | genes. | American |
| --------- | ------------ | --------- | ------ | -------- | --- | -------------- | ---------- | ----- | --------- | --------------- | --- | ------------------------ | ------ | -------- |
|           |              |           |        |          |     |                | Journal of | Human | Genetics, | 81(5), 873–883. |     | https://doi.org/10.1086/ |        |          |
| combining | rules (their | Table 5), | simply | allowing | one | point for each | 521032     |       |           |                 |     |                          |        |          |
invocation of supporting pathogenic evidence, two points for each Goldgar, D. E., Easton, D. F., Deffenbaugh, A. M., Monteiro, A. N.,
Tavtigian,S.V.,&Couch,F.J.(2004).IntegratedevaluationofDNA
invocationofmoderatepathogenicevidence,andsoforth,couldlead
|     |     |     |     |     |     |     | sequence | variants | of unknown | clinical | significance: |     | Application | to  |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | ---------- | -------- | ------------- | --- | ----------- | --- |
onetoproposethispointsystem,withthesamecaveatsaboutthe
|     |     |     |     |     |     |     | BRCA1 and | BRCA2. | American | Journal | of  | Human | Genetics, | 75(4), |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------ | -------- | ------- | --- | ----- | --------- | ------ |
strengthoftherulesLikelyPathogenic(i)andPathogenic(iii)thatwe 535–544.https://doi.org/10.1086/424388
Nykamp,K.,Anderson,M.,Powers,M.,Garcia,J.,Herrera,B.,Ho,Y.Y.,…
notedpreviously(Tavtigianetal.,2018).
In a more abstract sense depicted in Figure 1, the ACMG/AMP Topper, S. (2017). Sherloc: A comprehensive refinement of the
ACMG‐AMPvariantclassificationcriteria.GeneticsinMedicine,19(10),
qualitativeclassificationschemaprovidedascaffoldthatcouldbecom-
1105–1117.https://doi.org/10.1038/gim.2017.37
binedwithBayes'ruletoproduceitsBayesianformulation.Bidirectional
|     |     |     |     |     |     |     | Plon, S. E., Eccles, | D.  | M., Easton, | D., | Foulkes, | W. D., | Genuardi, | M., |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | ----------- | --- | -------- | ------ | --------- | --- |
feedbackbetweenthequalitativeclassificationschemaanditsBayesian Greenblatt, M. S., … Tavtigian, S. V. (2008). Sequence variant
|              |                   |       |     |           |             |        | classification | and | reporting:            | Recommendations |         | for  | improving | the   |
| ------------ | ----------------- | ----- | --- | --------- | ----------- | ------ | -------------- | --- | --------------------- | --------------- | ------- | ---- | --------- | ----- |
| formulation, | with a particular | focus | on  | empirical | measurement | of the |                |     |                       |                 |         |      |           |       |
|              |                   |       |     |           |             |        | interpretation | of  | cancer susceptibility |                 | genetic | test | results.  | Human |
strengthofevidenceattributabletoexistingornewdatatypes,should
Mutation,29(11),1282–1291.https://doi.org/10.1002/humu.20880
steadily improve the rigor of sequence variant classification. The point Richards, S., Aziz, N., Bale, S., Bick, D., Das, S., Gastier‐Foster, J., …
scalederivedhereautomaticallyinheritsthesefeatures. Rehm,H.L.(2015).Standardsandguidelinesfortheinterpretationof
Variantinterpretationisanewandrapidlydevelopingscience.All sequence variants: A joint consensus recommendation of the
|     |     |     |     |     |     |     | American | College | of Medical | Genetics |     | and Genomics |     | and the |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---------- | -------- | --- | ------------ | --- | ------- |
ofusarelearninganddevelopingnovelapproachesatarapidpace.The
|             |                  |              |     |                   |     |            | Association | for | Molecular | Pathology. | Genetics | in  | Medicine, | 17(5), |
| ----------- | ---------------- | ------------ | --- | ----------------- | --- | ---------- | ----------- | --- | --------- | ---------- | -------- | --- | --------- | ------ |
| integration | of mathematical, | statistical, |     | and computational |     | techniques |             |     |           |            |          |     |           |        |
405–423.https://doi.org/10.1038/gim.2015.30
intoour practices will benefittesting laboratories and,ultimately,pa- Riggs, E. R., Andersen, E. F., Cherry, A. M., Kantarci, S., Kearney, H., &
tientcare.Goingforward,werecommendthatdevelopersofallvariant Patel,A.,…ACMG.(2020).Technicalstandardsfortheinterpretation
|     |     |     |     |     |     |     | and reporting | of  | constitutional |     | copy‐number | variants: |     | A joint |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | -------------- | --- | ----------- | --------- | --- | ------- |
evaluationschemesexaminetheirproposedscoringscales,classification
|     |     |     |     |     |     |     | consensus | recommendation |     | of the | American | College | of  | Medical |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | ------ | -------- | ------- | --- | ------- |
thresholds,andunderlyinglogictoseehowwelltheycomportwitha
GeneticsandGenomics(ACMG)andtheClinicalGenomeResource
Bayesianprobabilisticframework.Thisexaminationshouldassesshow (ClinGen). Genetics in Medicine, 22(2), 245–257. https://doi.org/10.
1038/s41436-019-0686-8
naturallytheyflowfromtheparentACMG/AMPvariantclassification
guidelines, which were pioneering and insightful and provide a solid Tavtigian,S.V.,Greenblatt,M.S.,Harrison,S.M.,Nussbaum,R.L.,Prabhu,S.A.,
&Boucher,K.M.,…ClinGenSequenceVariantInterpretationWorking
foundationforfuturedevelopmentefforts.
Group.(2018).ModelingtheACMG/AMPvariantclassificationguidelines
|     |     |     |     |     |     |     | as a Bayesian | classification |     | framework. | Genetics | in  | Medicine, | 20(9), |
| --- | --- | --- | --- | --- | --- | --- | ------------- | -------------- | --- | ---------- | -------- | --- | --------- | ------ |
ACKNOWLEDGMENTS 1054–1060.https://doi.org/10.1038/gim.2017.210
| This study | is not a work | product | of the | ClinGen | Sequence | Variant |     |     |     |     |     |     |     |     |
| ---------- | ------------- | ------- | ------ | ------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
InterpretationWorkingGroup(ClinGenSVI).S.V.Tissupportedin
part by NIH R01 CA121245 and the Canadian PERSPECTIVE I&I Howtocitethisarticle:TavtigianSV,HarrisonSM,Boucher
Project through the Canadian Institutes of Health Research (GP1‐ KM,BieseckerLG.Fittinganaturallyscaledpointsystemtothe
155865).K.M.B.andtheHuntsmanCancerInstitute'sBiostatistics ACMG/AMPvariantclassificationguidelines.HumanMutation.
2020;41:1734–1737.https://doi.org/10.1002/humu.24088
| Core aresupportedinpart |     | byNIH | P30CA042014. |     |     | L. G. B.is sup- |     |     |     |     |     |     |     |     |
| ----------------------- | --- | ----- | ------------ | --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
portedbyNHGRIgrantHG200359.
