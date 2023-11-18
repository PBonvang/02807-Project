# %% Imports
import pandas as pd
from pathlib import Path

# %% Settings
data_path = Path('data')
BBR_path = data_path / Path('BBR/BBR_BuildingList.csv')
VUR_path = data_path / Path('VUR/VUR_joined.csv')
DAR_path = data_path / Path('DAR/DAR_joined.csv')

# %% Load data
BBR = pd.read_csv(BBR_path, delimiter=';', index_col=0)
VUR = pd.read_csv(VUR_path, delimiter=';')
DAR = pd.read_csv(DAR_path, delimiter=';')
# %% Rename BBR columns
BBR.rename(columns={
    "byg021BygningensAnvendelse" : "buildingUsageType",
     "byg026Opførelsesår" : "constructionYear",
     "byg027OmTilbygningsår" : "reconstructionOrExtensionYear",
     "byg030Vandforsyning" : "waterSupplyType",
     "byg031Afløbsforhold" : "drainageType",
     "byg032YdervæggensMateriale" : "outerWallMaterialType",
     "byg033Tagdækningsmateriale" : "roofMaterialType",
     "byg034SupplerendeYdervæggensMateriale" : "supplementOuterWallMaterialType",
     "byg035SupplerendeTagdækningsMateriale" : "supplementRoofMaterialType",
     "byg036AsbestholdigtMateriale" : "asbestosHoldingMaterialType",
     "byg038SamletBygningsareal" : "totalBuildingArea",
     "byg038SamletBygningsareal" : "totalResidenceArea",
     "byg038SamletBygningsareal" : "totalIndustrialArea",
     "byg041BebyggetAreal"  : "builtArea",
     "byg042ArealIndbyggetGarage"  : "areaOfBuiltInGarage",
     "byg043ArealIndbyggetCarport"  : "areaOfBuiltInCarport",
     "byg044ArealIndbyggetUdhus"  : "areaOfBuiltInShed",
     "byg045ArealIndbyggetUdestueEllerLign"  : "areaOfBuiltInConservatoryOrSimilar",
     "byg046SamletArealAfLukkedeOverdækningerPåBygningen"  : "totalAreaOfClosedCoveringsOnTheBuilding",
     "byg047ArealAfAffaldsrumITerrænniveau"  : "areaOfWasteRoomAtGroundLevel",
     "byg048AndetAreal"  : "otherArea",
     "byg049ArealAfOverdækketAreal"  : "areaOfCoveredArea",
     "byg051Adgangsareal"  : "accessArea",
     "byg054AntalEtager"  : "numberOfFloors",
     "byg055AfvigendeEtager"  : "deviantFloors",
     "byg056Varmeinstallation"  : "heatingInstallation",
     "byg057Opvarmningsmiddel"  : "heatingMedium",
     "byg058SupplerendeVarme" : "supplementaryHeating",
     "byg069Sikringsrumpladser"  : "shelterSpaces",
     "byg070Fredning"  : "preservation",
     "byg111StormrådetsOversvømmelsesSelvrisiko": "stormCouncilsFloodSelfRisk",
     "byg130ArealAfUdvendigEfterisolering"  : "areaOfExternalInsulation",
        "byg136PlaceringPåSøterritorie"  :     "locationOnLakeTerritory",
}, inplace=True)

BBR.columns